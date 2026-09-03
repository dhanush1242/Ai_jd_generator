from fastapi import FastAPI

from app.api.recruiter import router as recruiter_router
from app.api.jobs import router as jobs_router
from app.api.job_description import router as jd_router
from app.api.candidate import router as candidate_router
from app.api.admin import router as admin_router


app = FastAPI(
    title="AI JD Generator API",
    version="1.0.0",
)


app.include_router(
    recruiter_router,
    prefix="/api",
)

app.include_router(
    jobs_router,
    prefix="/api",
)

app.include_router(
    jd_router,
    prefix="/api",
)

app.include_router(
    candidate_router,
    prefix="/api",
)

app.include_router(
    admin_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "AI JD Generator API is running"
    }