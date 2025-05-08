from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_docling import DoclingLoader

class DocumentInput(BaseModel):
    document: str = Field(..., description="Useful to parse text from Resume")

class ResumeParserToolDocling(BaseTool):
    name: str = "Parse text from Resume"
    description: str = "Useful to parse text from Resume"
    args_schema: type[BaseModel] = DocumentInput

    def _run(self, document: str) -> str:
        try:    
            # Parse the document using unstructured library
            loader = DoclingLoader(file_path="F:/AgenticAI/Resume_ATS/resume.docx")
            #loader = DoclingLoader(file_path="F:/AgenticAI/Resume_ATS/index.pdf")
            #loader = DoclingLoader(file_path="https://cloudresumechallenge.dev/halloffame/")

            docs = loader.load()
            # Convert the parsed elements to a string representation
            #parsed_text = "\n".join([str(element) for element in docs])
            parsed_text = "\n".join([doc.page_content for doc in docs if hasattr(doc, 'page_content')])         
            return parsed_text
        except Exception as e:
            return f"Error while processing document: {str(e)}"
    
    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented")