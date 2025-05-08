import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.auto import partition
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM

print("Script started...")

elements = partition("F:/AgenticAI/Resume_ATS/resume.docx")
#elements = partition("F:/AgenticAI/Resume_ATS/index.pdf")
#elements = partition("https://cloudresumechallenge.dev/halloffame/")

# Convert the parsed elements to a string representation
parsed_text = "\n".join([str(element) for element in elements])
print("Parsed text:")
print(parsed_text)