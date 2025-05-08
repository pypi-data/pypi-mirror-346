import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_docling import DoclingLoader
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM

print("Script started...")

loader = DoclingLoader(file_path="https://www.indeed.com/q-full-time-l-madison,-wi-jobs.html?vjk=7e9e47e09fbadf45")
#loader = DoclingLoader(file_path="F:/AgenticAI/Resume_ATS/index.pdf")
#loader = DoclingLoader(file_path="https://cloudresumechallenge.dev/halloffame/")

docs = loader.load()
# Convert the parsed elements to a string representation
#parsed_text = "\n".join([str(element) for element in docs])
parsed_text = "\n".join([doc.page_content for doc in docs if hasattr(doc, 'page_content')])

print("Parsed text:")
print(parsed_text)