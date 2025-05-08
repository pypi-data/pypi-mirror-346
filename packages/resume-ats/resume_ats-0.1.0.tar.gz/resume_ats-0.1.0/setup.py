from setuptools import setup, find_packages

setup(
    name="resume_ats",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "langchain-openai",
        "langchain_groq",
        "unstructured[docx]",
        "unstructured[pdf]",
        "langchain-docling",
        "tika",
        "crewai_tools",
        "litellm",
        "scrapfly-sdk"
    ],
    entry_points={
        "console_scripts": [
            "resume-ats=api_app:app",
        ],
    },
)