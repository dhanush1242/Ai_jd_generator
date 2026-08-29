def build_jd_prompt(job) -> str:
    return f"""
You are an expert HR recruiter and professional job description writer.

Generate ONLY the following three sections for this job:
  1. Job Summary
  2. Key Responsibilities
  3. Preferred Candidate Profile

Job information:
  Job Title: {job.job_title}
  Required Skills: {job.required_skills}
  Education Qualification: {job.education_qualification}
  Experience: {job.experience}
  Location: {job.location}
  Passed Out Year: {job.passedout_year}
  Work Mode: {job.work_mode}
  Job Type: {job.job_type}
  Package: {job.package}

STRICT RULES:
  - Use only the information provided above.
  - Do not introduce additional technologies, tools, frameworks,
    databases, qualifications, certifications, or skills.
  - Responsibilities must be appropriate for the provided skills
    and experience level.
  - Do not create additional job requirements.
  - Do not repeat factual sections such as salary, location,
    education, work mode, or job type.
  - Return only the three requested sections.
"""