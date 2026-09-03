from app.db.session import SessionLocal

def get_db_session():
    """
    Create and return a database session
    for MCP tools.
    """
    return SessionLocal()
