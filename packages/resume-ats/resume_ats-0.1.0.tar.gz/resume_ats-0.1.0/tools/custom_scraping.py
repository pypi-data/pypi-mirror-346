from crewai.tools import BaseTool
from pydantic import BaseModel, Field, HttpUrl
from crewai_tools import ScrapeWebsiteTool
from typing import Union, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
from datetime import datetime

class WebsiteInput(BaseModel):
    """Schema for web scraping input"""
    document: Union[str, Dict] = Field(
        ...,
        description="URL to scrape or dictionary containing URL"
    )

class WebParserTool(BaseTool):
    name: str = "Web Scraping Tool"
    description: str = "Scraping the content from websites"
    args_schema: BaseModel = WebsiteInput

    def _run(self, document: Union[str, Dict]) -> str:
        try:
            # Extract URL from input
            url = self._extract_url(document)
            if not url:
                return "Error: Could not extract valid URL from input"

            # Validate URL
            if not self._is_valid_url(url):
                return "Error: Invalid URL format"

            # Handle LinkedIn URLs
            if "linkedin.com" in url.lower():
                return self._scrape_linkedin(url)

            # Default web scraping for other URLs
            return self._default_scrape(url)

        except Exception as e:
            return f"Error while processing document: {str(e)}"

    def _extract_url(self, document: Union[str, Dict]) -> str:
        """Extract URL from input document"""
        if isinstance(document, str):
            return document
        if isinstance(document, dict):
            # Try different common keys
            for key in ['url', 'description', 'document']:
                if key in document and isinstance(document[key], str):
                    return document[key]
            # Try first string value if no known keys found
            for value in document.values():
                if isinstance(value, str):
                    return value
        return ""

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _scrape_linkedin(self, url: str) -> str:
        """Enhanced LinkedIn job post scraping"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.linkedin.com/',
            'Origin': 'https://www.linkedin.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        try:
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Updated CSS selectors for LinkedIn job posts
            selectors = {
                'title': ['h1.job-title', 'h1.topcard__title'],
                'company': ['a.company-link', 'span.topcard__org-name-link'],
                'location': ['span.location', 'span.topcard__flavor--bullet'],
                'description': ['div.description__text', 'div.show-more-less-html__markup'],
                'requirements': ['div.job-requirements', 'div.description__job-criteria-list'],
                'skills': ['ul.job-requirements__skills', 'ul.job-requirements__list']
            }
            
            job_info = {}
            for key, selector_list in selectors.items():
                for selector in selector_list:
                    content = self._extract_text(soup, selector)
                    if content:
                        job_info[key] = content
                        break
                if key not in job_info:
                    job_info[key] = ""

            # Structure the output
            return json.dumps({
                "job_details": job_info,
                "source": "LinkedIn",
                "scraped_at": datetime.now().isoformat(),
                "success": any(value for value in job_info.values())
            }, indent=2)

        except Exception as e:
            return f"Error scraping LinkedIn: {str(e)}"

    def _extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text from HTML element"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else ""

    def _default_scrape(self, url: str) -> str:
        """Default scraping for non-LinkedIn URLs"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            
            return soup.get_text(separator='\n', strip=True)
            
        except Exception as e:
            return f"Error scraping URL: {str(e)}"

    async def _arun(self, document: Union[str, Dict]) -> str:
        """Async implementation defaults to sync version"""
        return self._run(document)