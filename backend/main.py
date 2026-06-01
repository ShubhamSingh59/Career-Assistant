from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
from agents.resumeAnalyzer import ResumeAnalyzer
from agents.jobFinder import JobFinder
from agents.companyResearcher import CompanyResearcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = ResumeAnalyzer()
job_finder = JobFinder()
company_researcher = CompanyResearcher()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/upload")
async def uploadResume(resume: UploadFile = File(...)):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    resume_content = await resume.read()

    try:
        pdf_reader = PdfReader(io.BytesIO(resume_content))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + "\n"
    except Exception as e:
        return {"error": f"Failed to read PDF: {str(e)}"}

    analysis_result = analyzer.analyze_resume(resume_text)
    job_title = analysis_result.get("predicted_job_titles", [None])[0]
    # print(job_title)

    if job_title:
        jobs = job_finder.find_jobs(job_title, location="India")
        job_listings = jobs

    else:
        job_listings = []

    return {"analysis": analysis_result, "job_listings": job_listings}

@app.get("/api/company-research")
async def company_research(company_name: str):
    result = company_researcher.research_company(company_name)
    return {"company_summary": result}