from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.auto import partition


class DocumentInput(BaseModel):
    document: str = Field(..., description="Useful to parse text from Resume")

class ResumeParserToolUnstructured(BaseTool):
    name: str = "Parse text from Resume"
    description: str = "Useful to parse text from Resume"
    args_schema: type[BaseModel] = DocumentInput

    def _run(self, document: str) -> str:
        try:    
            # Parse the document using unstructured library
            elements = partition(document)
            # Convert the parsed elements to a string representation
            parsed_text = "\n".join([str(element) for element in elements])
            return parsed_text
        except Exception as e:
            return f"Error while processing document: {str(e)}"
    
    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented")