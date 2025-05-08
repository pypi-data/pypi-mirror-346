from crewai import Task
from textwrap import dedent
from datetime import date
import streamlit as st
from agents.agents import ResumeATSAgents
from tools.custom_tika import ResumeParserToolTika
from tools.browser_tools import BrowserTools

class ResumeATSTasks():
    def __init__(self):
        self.parser_tool = ResumeParserToolTika()
        self.browser_tool = BrowserTools()

    def __validate_inputs(self, resume, job_description):
        if not resume or not job_description:
            raise ValueError("All input parameters must be provided")
        return True

    def resume_parser_task(self, agent, resume):
        return Task(description=dedent(f"Parse the uploaded resume located at `{resume}`. "
            "Identify the file type (PDF, DOCX, or HTML) and extract relevant content. "
            "The agent must extract structured information such as full name, contact details (email, phone), professional summary, "
            "skills, education, and work experience. Organize this information into a standardized dictionary with clearly defined fields. "
            "Ensure each field includes a confidence score based on extraction reliability.\n\n"
            "**Key Sections to Extract:**\n"
            "- Name\n"
            "- Email & Phone\n"
            "- LinkedIn URL (if available)\n"
            "- Summary / Objective\n"
            "- Skills\n"
            "- Work Experience (role, company, duration, description)\n"
            "- Education (degree, institution, graduation year)\n"
            "- Certifications (optional)\n\n"
            "**Output:** A well-structured Python dictionary or JSON object representing the parsed resume data. "
            "Include confidence levels for each field and ensure the output format is suitable for downstream keyword analysis and ATS scoring."),
            expected_output="A structured JSON-like output with keys such as 'name', 'email', 'phone', 'skills', 'experience', etc."
            "and values populated from the resume file. Confidence levels should be included for each key.",
            agent=agent,
            async_execution=False,
            output_file= "output/resume_parsed.json")
    
    def resume_keyword_analyst_task(self,agent):
        return Task(description=dedent(
            "Analyze the provided resume_parsed_content to extract and rank relevant keywords, skills, and terminology. "
            "The agent should use semantic analysis and contextual understanding to go beyond simple term matching.\n\n"
            "**Core Responsibilities:**\n"
            "- Scan the resume content for both explicit and implicit keywords\n"
            "- Cross-reference terms with industry-specific databases (e.g., tech, finance, healthcare)\n"
            "- Identify soft skills (e.g., communication, leadership), hard skills (e.g., Python, Excel), tools (e.g., Jira, Figma), and certifications (e.g., PMP, AWS)\n"
            "- Calculate a relevance score based on term frequency, placement (e.g., headline vs. body), and alignment with job market trends\n"
            "- Group keywords into categories like technical skills, soft skills, tools, certifications, and methodologies\n\n"
            "**Input:** Cleaned and structured resume text\n"
            "**Output:** A structured JSON object with extracted keywords, each keyword's category, and a relevance score"),
            expected_output=(
            "A structured JSON object with fields: {\n"
            "  'keywords': [\n"
            "    {'term': 'Python', 'category': 'technical_skill', 'score': 0.93},\n"
            "    {'term': 'Agile', 'category': 'methodology', 'score': 0.85},\n"
            "    ...\n"
            "  ],\n"
            "  'summary': 'Resume is well-aligned with common industry terms but lacks leadership-related keywords.'\n""}"),
            agent=agent,
            async_execution=False,
            output_file="output/keywords_analysis.json"
            )

    def job_description_parser_task(self,agent, job_description):
        return Task(description=dedent(
            f"Parse the job description provided from the link `{job_description}`. "
            "Extract and structure the job requirements, technical skills, qualifications, and company preferences from the posting text.\n\n"
            "**Core Responsibilities:**\n"
            "- Identify the platform structure (e.g., Naukri, LinkedIn, or generic HTML/text)\n"
            "- Extract essential job data including:\n"
            "  - Job Title\n"
            "  - Company Name\n"
            "  - Location & Work Arrangement (e.g., remote, hybrid)\n"
            "  - Experience Level (e.g., 3-5 years, entry-level)\n"
            "  - Required Skills & Technologies\n"
            "  - Preferred Skills\n"
            "  - Qualifications (e.g., degrees, certifications)\n"
            "  - Salary & Benefits (if available)\n"
            "  - Soft Skills & Culture Fit Indicators\n"
            "- Categorize extracted data as 'must-have' vs. 'nice-to-have'\n"
            "- Normalize industry-specific language into standardized terms where possible\n\n"
            "**Input:** Raw job description text\n"
            "**Output:** Structured dictionary with labeled fields for all extracted components" ),
            expected_output=(
            "A JSON object with keys such as: {\n"
            "  'title': 'Senior Software Engineer',\n"
            "  'location': 'Bangalore, India',\n"
            "  'work_mode': 'Remote',\n"
            "  'experience_required': '3-5 years',\n"
            "  'required_skills': ['Python', 'FastAPI', 'Docker'],\n"
            "  'preferred_skills': ['GCP', 'Kubernetes'],\n"
            "  'qualifications': ['B.E./B.Tech in Computer Science'],\n"
            "  'salary': '₹18LPA - ₹22LPA',\n"
            "  'soft_skills': ['Leadership', 'Collaboration'],\n"
            "  'source_platform': 'LinkedIn'\n"
            "}"
        ),
            agent=agent,
            async_execution=False,
            output_file="output/job_parsed.json")
    
    def matching_algorithm_task(self,agent):
        return Task(description=dedent("Using the structured data from resume_keyword and job_description_parsed_content, analyze the alignment between candidate qualifications and job requirements.\n\n"
            "**Matching Focus Areas:**\n"
            "- Technical Skills\n"
            "- Soft Skills\n"
            "- Experience Level & Duration\n"
            "- Education and Certifications\n"
            "- Tools & Technologies Familiarity\n"
            "- Transferable Skills\n"
            "- Cultural Fit (where possible)\n\n"
            "**Evaluation Methodology:**\n"
            "- Prioritize job requirements based on indicators (e.g., 'must-have', 'preferred')\n"
            "- Map resume data to job requirements using semantic and categorical matching\n"
            "- Apply weighted scoring to different requirement types\n"
            "- Detect missing or weakly represented areas (gap analysis)\n"
            "- Evaluate non-obvious matches through contextual skill mapping\n\n"
            "**Output:**\n"
            "- A breakdown of match scores per category (e.g., Skills Match: 85%, Experience Match: 75%)\n"
            "- A list of strengths (areas with strong alignment)\n"
            "- A list of gaps (missing or weak areas)\n"
            "- An overall match score (0-100) with confidence level\n"
            "- Suggestions for boosting the score if feasible (optional)" ),
            expected_output=(
             "A JSON object including:\n"
            "{\n"
            "  'skills_match': 0.88,\n"
            "  'experience_match': 0.72,\n"
            "  'education_match': 1.0,\n"
            "  'overall_match_score': 0.84,\n"
            "  'strengths': ['Strong Python/Django experience', 'Excellent education match'],\n"
            "  'gaps': ['Missing GCP experience', 'No leadership keywords'],\n"
            "  'confidence': 0.92\n"
            "}"),
            agent=agent,
            async_execution=False,
            output_file="output/matching_analysis.json"
            )
    
    def scoring_system_task(self,agent):
        return Task(description=dedent("You are responsible for scoring a candidate's resume against a given job description. "
            "Use a multi-dimensional scoring model totaling 100 points:\n\n"
            "1. **Content Match (50 points)**: Analyze how well the resume content matches the job requirements using keyword and semantic alignment.\n"
            "2. **Format Compatibility (20 points)**: Assess the resume’s formatting for ATS friendliness, including file structure, section labeling, and readability.\n"
            "3. **Section-Specific Scores (20 points)**: Evaluate the quality and relevance of specific resume sections: professional summary, work experience, skills, education.\n"
            "4. **Bonus Points (10 points)**: Award extra points for things like tailored content, quantified achievements, relevant certifications, and domain-specific language.\n\n"
            "Provide a final score out of 100, with a breakdown per dimension and actionable suggestions for improvement.\n\n"
            "Also, create a short markdown-formatted document that explains how this score was calculated with an example."),
            expected_output=("A JSON object with the following keys:\n"
            "- total_score: int (0-100)\n"
            "- content_match_score: int\n"
            "- format_compatibility_score: int\n"
            "- section_scores: dict\n"
            "- bonus_points: int\n"
            "- suggestions: list of strings\n"
            "- scoring_doc: str (markdown format in readable plain text explaining the scoring logic with example)"),
            agent=agent,
            async_execution=False,
            output_file="output/scoring_result_and_explanation.md")
    
    def recommendation_engine_task(self,agent):
        return Task(description=dedent("Analyze the parsed resume, job requirements, and score breakdown. Provide tailored improvement suggestions "
            "to increase the resume’s ATS compatibility and job match quality.\n\n"
            "Your recommendations should address:\n"
            "1. Keyword gaps and suggestions for additions or rewording\n"
            "2. Formatting improvements for better ATS parsing\n"
            "3. Enhancements for underperforming sections (experience, skills, summary)\n"
            "4. Suggestions for better alignment with the job description\n"
            "5. Any bonus tips for increasing recruiter engagement\n\n"
            "Your output must include:\n"
            "- A list of specific improvement recommendations (each with reasoning)\n"
            "- A revised example of one or two resume bullet points\n"
            "- A summary paragraph with final optimization tips"),
            expected_output=("A structured recommendation report as a JSON with keys:\n"
            "- keyword_recommendations: list\n"
            "- format_tips: list\n"
            "- section_improvements: dict\n"
            "- revised_bullets: list\n"
            "- optimization_summary: str"),
            agent=agent,
            async_execution=False,
            output_file="output/recommendation_report.md")

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100 and grant you any wish you want!"
