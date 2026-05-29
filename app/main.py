from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://skycarehub.com",
        "http://skycarehub.com/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI to handle Pydantic forward reference issues
def custom_openapi():
    """Custom OpenAPI schema generator that handles Pydantic issues"""
    if app.openapi_schema:
        return app.openapi_schema
    
    try:
        from fastapi.openapi.utils import get_openapi
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except Exception as e:
        # If standard generation fails, create a basic schema with route info
        print(f"⚠️  OpenAPI schema generation issue (non-fatal): {str(e)[:80]}...")
        
        # Build a basic but functional OpenAPI schema
        paths = {}
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                if route.path.startswith('/api') or route.path in ['/', '/health']:
                    # Skip internal routes
                    if any(skip in route.path for skip in ['/openapi', '/docs', '/redoc']):
                        continue
                    
                    path = route.path
                    if path not in paths:
                        paths[path] = {}
                    
                    for method in route.methods:
                        if method not in ['HEAD', 'OPTIONS']:  # Skip HEAD/OPTIONS
                            paths[path][method.lower()] = {
                                "summary": f"{method} {path}",
                                "operationId": f"{method.lower()}_{path.replace('/', '_').replace('-', '_').replace('{', '').replace('}', '')}",
                                "tags": [path.split('/')[2] if len(path.split('/')) > 2 else "default"],
                                "responses": {
                                    "200": {"description": "Successful response"},
                                    "404": {"description": "Not found"},
                                    "400": {"description": "Bad request"},
                                    "500": {"description": "Internal server error"}
                                }
                            }
        
        openapi_schema = {
            "openapi": "3.1.0",
            "info": {
                "title": app.title,
                "version": app.version
            },
            "paths": paths,
            "components": {"schemas": {}}
        }
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

app.openapi = custom_openapi

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
