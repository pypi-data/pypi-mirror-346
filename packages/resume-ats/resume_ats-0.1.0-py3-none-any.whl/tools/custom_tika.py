from crewai.tools import BaseTool
from tika import parser
import requests
import tempfile
from pydantic import BaseModel, Field
import os
import json

class Filepath(BaseModel):
    filepath: str = Field(..., description="filepath of resume to parse")

class ResumeParserToolTika(BaseTool):
    name: str = "Resume Parser Tool"
    description: str = "Parses resume content from various file formats using Apache Tika"

    def _run(self, filepath: str) -> str:
        try:
            # Handle JSON input
            if isinstance(filepath, str) and filepath.strip().startswith("{"):
                try:
                    data = json.loads(filepath)
                    filepath = data.get("filepath", filepath)
                except Exception:
                    pass

            # If input is a URL, download and parse
            if filepath.startswith(('http://', 'https://')):
                return self._process_url(filepath)
            # If input is a file path, parse the file
            elif os.path.exists(filepath):
                return self._process_file(filepath)
            # Otherwise, treat as raw text and save to temp file
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as temp_file:
                    temp_file.write(filepath)
                    temp_file_path = temp_file.name
                return self._process_file(temp_file_path)
        except Exception as e:
            return f"Error parsing resume: {str(e)}"

    async def _arun(self, filepath: str) -> str:
        return self._run(filepath)

    def _process_file(self, filepath: str) -> str:
        parsed = parser.from_file(filepath)
        return parsed.get("content", "No content found")

    def _process_url(self, url: str) -> str:
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
            temp_file.write(response.content)
            return self._process_file(temp_file.name)