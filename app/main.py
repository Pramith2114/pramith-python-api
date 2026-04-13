from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, create_all_tables
from app.routes import router
from app.auth import auth_router

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

# Include routes
app.include_router(router)
app.include_router(auth_router)


# Initialize database tables on startup
@app.on_event("startup")
async def startup():
    """Create all database tables on application startup"""
    try:
        create_all_tables()
        print("✓ Database tables created")
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {str(e)}")
        print("   Ensure IAM authentication is enabled on your RDS instance")


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with database connection"""
    try:
        # Simple database query to verify connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}
