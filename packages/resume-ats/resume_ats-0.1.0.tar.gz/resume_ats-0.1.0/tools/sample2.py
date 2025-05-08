import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tika import parser
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM

print("Script started...")

#filepath = "F:/AgenticAI/Resume_ATS/resume.docx"
#filepath = "F:/AgenticAI/Resume_ATS/index.pdf"
filepath = "https://www.linkedin.com/jobs/collections/hiring-in-network/?currentJobId=4204537595"

print("Parsed text:")
parsed = parser.from_file(filepath)
print (parsed["content"])
