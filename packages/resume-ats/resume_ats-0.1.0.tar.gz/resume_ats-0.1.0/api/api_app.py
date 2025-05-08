import sys
from pathlib import Path

# Add the project root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(root_dir)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from crewai import Crew, LLM
from agents.agents import ResumeATSAgents
from tasks.tasks import ResumeATSTasks
import os
from dotenv import load_dotenv
from functools import lru_cache
import os
from utils.logger import get_logger

logger = get_logger(__name__)

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
os.environ.pop("SSL_CERT_FILE", None)

# Load environment variables
load_dotenv()

from api.routes import router

app = FastAPI(
    title="ResumeATS Score API",
    description="AI-powered Resume ATS Scorer API using CrewAI",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeATSRequest(BaseModel):
    resme_filepath: str = Field(..., 
        example="F:/AgenticAI/Resume_ATS/resume.docx",
        description="Resume file path")
    job_description_filepath: str = Field(..., 
        example="https://www.naukri.com/job-listings-restaurant-manager-kfc-bengaluru-5-to-10-years-240425011574?src=jobsearchDesk&sid=17465538852965374_2&xp=2&px=1&nignbevent_src=jobsearchDeskGNB",
        #example="https://www.indeed.com/q-full-time-l-madison,-wi-jobs.html?vjk=7e9e47e09fbadf45",
        description="Job description file path")


class ResumeATSResponse(BaseModel):
    status: str
    message: str
    resume_ats_score: Optional[str] = None
    error: Optional[str] = None

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        #self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        #self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")

@lru_cache()
def get_settings():
    return Settings()

def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'GEMINI_API_KEY': settings.GEMINI_API_KEY
        #'SERPER_API_KEY': settings.SERPER_API_KEY,
        #'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )
    return settings

class ResumeATSCrew:
    def __init__(self, resume, job_description):
        self.resume = resume
        self.job_description = job_description
        self.llm = LLM(model="gemini/gemini-2.0-flash")
        #self.llm = LLM

    def run(self):
        try:
            agents = ResumeATSAgents(llm=self.llm)
            tasks = ResumeATSTasks()

            resume_parser_agent = agents.resume_parser_agent()
            resume_keyword_analyst_agent = agents.resume_keyword_analyst_agent()
            job_description_parser_agent = agents.job_description_parser_agent()
            matching_algorithm_agent = agents.matching_algorithm_agent()
            scoring_system_agent = agents.scoring_system_agent()
            recommendation_engine_agent = agents.recommendation_engine_agent()


            print("Parsing resume...")
            resume_parser_task = tasks.resume_parser_task(
                agent = resume_parser_agent,
                resume = self.resume
            )

            print("Analyzing keywords...")
            resume_keyword_analyst_task = tasks.resume_keyword_analyst_task(
                agent = resume_keyword_analyst_agent
            )

            print("Parsing job description...")
            job_description_parser_task = tasks.job_description_parser_task(
                agent = job_description_parser_agent,
                job_description=self.job_description
            )

            print("Running matching algorithm...")
            matching_algorithm_task = tasks.matching_algorithm_task(
                agent = matching_algorithm_agent,

            )

            print("Generating ATS score...")
            scoring_system_task = tasks.scoring_system_task(
                agent = scoring_system_agent,

            )

            print("Generating recommendation report..")
            recommendation_engine_task = tasks.recommendation_engine_task(
                agent = recommendation_engine_agent,

            )
            crew = Crew(
                agents=[
                    resume_parser_agent, resume_keyword_analyst_agent, job_description_parser_agent,
                    matching_algorithm_agent, scoring_system_agent, recommendation_engine_agent
                ],
                tasks=[resume_parser_task, resume_keyword_analyst_task, job_description_parser_task,
                       matching_algorithm_task, scoring_system_task, recommendation_engine_task],
                verbose=True
            )

            result = crew.kickoff()
            # Convert CrewOutput to string and ensure it's properly formatted
            return result.raw if hasattr(result, 'raw') else str(result)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.get("/")
async def root():
    return {
        "message": "Welcome to Resume ATS Scorer API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.post("/api/v1/resume-ats", response_model=ResumeATSResponse)
async def resume_ats(
    resume_ats_request: ResumeATSRequest,
    settings: Settings = Depends(validate_api_keys)
):
    # # Validate dates
    # if trip_request.end_date <= trip_request.start_date:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="End date must be after start date"
    #     )

    # # Format date range
    # date_range = f"{trip_request.start_date} to {trip_request.end_date}"

    try:
        resume_Crew = ResumeATSCrew(
            resume_ats_request.resme_filepath,
            resume_ats_request.job_description_filepath
        )
        
        resume_ats_score = resume_Crew.run()
        
        # Ensure resume ats score is a string
        if not isinstance(resume_ats_score, str):
            resume_ats_score = str(resume_ats_score)
            
        return ResumeATSResponse(
            status="success",
            message="Resume ATS Score generated successfully",
            resume_ats_score=resume_ats_score
        )
    
    except Exception as e:
        return ResumeATSResponse(
            status="error",
            message="Failed to generate Resume ATS Score",
            error=str(e)
        )

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)