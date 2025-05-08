import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM

class WebsiteInput(BaseModel):
    website: str = Field(..., description="The website URL to scrape")

class BrowserTools(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> str:
        try:
            url = f"https://chrome.browserless.io/content?token=S4U9BDqYa2grWd9aeb50713daf123a4ed9479f8a38"
            payload = json.dumps({"url": website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            
            if response.status_code != 200:
                return f"Error: Failed to fetch website content. Status code: {response.status_code}"
            
            elements = partition_html(text=response.text)
            content = "\n\n".join([str(el) for el in elements])
            content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            return content
        except Exception as e:
            return f"Error while processing website: {str(e)}"

    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented")
