import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.recruiter import router as recruiter_router
from app.api.jobs import router as jobs_router
from app.api.job_description import router as jd_router
from app.api.candidate import router as candidate_router

app = FastAPI(title="AI JD Generator API", version="1.0.0",)

# Ensure uploads directory exists and mount it for serving static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"],)

app.include_router(recruiter_router, prefix="/api",)

app.include_router(jobs_router, prefix="/api",)

app.include_router(jd_router, prefix="/api",)

app.include_router(candidate_router, prefix="/api",)

@app.get("/")
def root(): return {"message": "AI JD Generator API is running"}