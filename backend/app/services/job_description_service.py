from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from fastapi import HTTPException, status

from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription
from app.models.recruiter import Recruiter
from app.dto.job_description import JobDescriptionUpdate
from app.core.llm import client
from app.prompts.jd_prompts import build_jd_prompt

def generate_jd(db: Session, job_id: int, recruiter: Recruiter) -> JobDescription:
    # Verify the job belongs to the recruiter
    job = db.query(JobParameter).filter(
        JobParameter.job_id == job_id,
        JobParameter.recruiter_id == recruiter.recruiter_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
        
    # Get the latest version number for this job
    latest_jd = db.query(JobDescription).filter(
        JobDescription.job_id == job_id
    ).order_by(desc(JobDescription.version_number)).first()
    
    version_number = (1 if not latest_jd else latest_jd.version_number + 1)
    
    # Generate JD logic placeholder - replace with actual LLM generation
    prompt = build_jd_prompt(job)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert HR recruiter "
                    "and professional job description writer."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    ai_content = response.choices[0].message.content

    generated_text = f"""
    # {job.job_title}

    {ai_content}

    ## Required Skills
    {job.required_skills}

    ## Educational Qualification
    {job.education_qualification}

    ## Experience Required
    {job.experience}

    ## Location
    {job.location}

    ## Passed Out Year
    {job.passedout_year}

    ## Work Mode
    {job.work_mode}

    ## Job Type
    {job.job_type}

    ## Compensation
    {job.package}
    """.strip()

    new_jd = JobDescription(
        job_id=job_id,
        version_number=version_number,
        generated_jd=generated_text
    )
    
    db.add(new_jd)
    db.commit()
    db.refresh(new_jd)
    
    return new_jd


def regenerate_jd(db: Session, job_id: int, recruiter: Recruiter) -> JobDescription:
    # Logic might differ in the future, but for now it's just generating a new version
    return generate_jd(db, job_id, recruiter)


def get_jd_versions(db: Session, job_id: int, recruiter: Recruiter) -> list[JobDescription]:
    job = db.query(JobParameter).filter(
        JobParameter.job_id == job_id,
        JobParameter.recruiter_id == recruiter.recruiter_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
        
    return db.query(JobDescription).filter(
        JobDescription.job_id == job_id
    ).order_by(desc(JobDescription.version_number)).all()


def update_jd_version(
    db: Session,
    job_id: int,
    version_id: int,
    update_data: JobDescriptionUpdate,
    recruiter: Recruiter
) -> JobDescription:
    job = db.query(JobParameter).filter(
        JobParameter.job_id == job_id,
        JobParameter.recruiter_id == recruiter.recruiter_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
        
    jd = db.query(JobDescription).filter(
        JobDescription.job_id == job_id,
        JobDescription.version_number == version_id
    ).first()
    
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JD version not found"
        )
        
    jd.updated_jd = update_data.updated_jd
    db.commit()
    db.refresh(jd)
    
    return jd


def publish_jd_version(db: Session, job_id: int, version_id: int, recruiter: Recruiter) -> JobDescription:
    job = db.query(JobParameter).filter(
        JobParameter.job_id == job_id,
        JobParameter.recruiter_id == recruiter.recruiter_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
        
    jd = db.query(JobDescription).filter(
        JobDescription.job_id == job_id,
        JobDescription.version_number == version_id
    ).first()
    
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JD version not found"
        )
        
    # Unpublish all other versions for this job
    db.query(JobDescription).filter(
        JobDescription.job_id == job_id,
        JobDescription.is_published == True
    ).update({"is_published": False}, synchronize_session=False)
    
    jd.is_published = True
    jd.published_at = func.now()
    
    db.commit()
    db.refresh(jd)
    
    return jd
