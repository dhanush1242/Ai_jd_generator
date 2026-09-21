from mcp.server import MCPServer
from mcp_server.tools.candidate_tools import (search_jobs, get_my_applications, get_application_status,)
from mcp_server.tools.recruiter_tools import (get_recruiter_jobs, get_job_applications, get_application_notes,)

mcp = MCPServer("AI JD Generator MCP Server")

@mcp.tool()
def search_jobs_tool(location: str | None = None, experience: str | None = None, skills: str | None = None,) -> list[dict]:
    """
    Search published jobs using optional
    location, experience, and skills filters.
    """
    return search_jobs(location=location, experience=experience, skills=skills,)

@mcp.tool()
def get_my_applications_tool(candidate_id: int,) -> list[dict]:
    """
    Get all job applications for a candidate,
    including job details and application status.
    """
    return get_my_applications(candidate_id=candidate_id,)

@mcp.tool()
def get_application_status_tool(candidate_id: int, job_title: str,) -> dict:
    """
    Get the application status for a candidate
    using the job title.
    """
    return get_application_status(candidate_id=candidate_id, job_title=job_title,)

@mcp.tool()
def get_recruiter_jobs_tool(recruiter_id: int,) -> list[dict]:
    """
    Get all jobs created by a recruiter.
    """
    return get_recruiter_jobs(recruiter_id=recruiter_id,)

@mcp.tool()
def get_job_applications_tool(recruiter_id: int, job_id: int,) -> list[dict] | dict:
    """
    Get applications for a recruiter-owned job.
    """
    return get_job_applications(recruiter_id=recruiter_id, job_id=job_id,)

@mcp.tool()
def get_application_notes_tool(recruiter_id: int, application_id: int,) -> list[dict] | dict:
    """
    Get recruiter notes for an application.
    """
    return get_application_notes(recruiter_id=recruiter_id, application_id=application_id,)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9000,)
