"""
Database connection and session management
"""
import os
import ssl
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings


def get_database_url():
    """
    Construct database URL with support for both standard PostgreSQL and AWS RDS IAM auth.
    
    For standard PostgreSQL:
        Uses DATABASE_URL from environment
        
    For AWS RDS with IAM Authentication:
        Generates temporary credentials using aws rds generate-db-auth-token
    """
    
    # If DATABASE_URL is explicitly provided, use it
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # Use AWS RDS with IAM authentication
    if settings.USE_AWS_RDS and settings.USE_IAM_AUTH:
        try:
            import boto3
            
            # Generate IAM authentication token (valid for 15 minutes)
            client = boto3.client("rds", region_name=settings.AWS_REGION)
            token = client.generate_db_auth_token(
                DBHostname=settings.RDS_HOST,
                Port=settings.RDS_PORT,
                DBUsername=settings.RDS_USERNAME,
            )
            
            # Build connection string with IAM token as password
            database_url = (
                f"postgresql://{settings.RDS_USERNAME}:{token}"
                f"@{settings.RDS_HOST}:{settings.RDS_PORT}/{settings.RDS_DATABASE}"
            )
            return database_url
            
        except ImportError:
            raise ImportError("boto3 is required for AWS RDS IAM authentication. Install with: pip install boto3")
        except Exception as e:
            raise Exception(f"Failed to generate AWS RDS auth token: {str(e)}")
    
    # Use AWS RDS with standard password authentication
    elif settings.USE_AWS_RDS:
        if not settings.RDS_PASSWORD:
            raise ValueError("RDS_PASSWORD environment variable is required when USE_IAM_AUTH is False")
        
        database_url = (
            f"postgresql://{settings.RDS_USERNAME}:{settings.RDS_PASSWORD}"
            f"@{settings.RDS_HOST}:{settings.RDS_PORT}/{settings.RDS_DATABASE}"
        )
        return database_url
    
    else:
        raise ValueError("Either DATABASE_URL or USE_AWS_RDS must be set")


def get_ssl_context():
    """
    Create SSL context for secure RDS connections.
    AWS RDS requires SSL/TLS by default.
    """
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    # Use custom certificate path if provided
    if settings.RDS_SSL_CERT_PATH and os.path.exists(settings.RDS_SSL_CERT_PATH):
        ssl_context.load_verify_locations(settings.RDS_SSL_CERT_PATH)
    
    return ssl_context


# Create database URL
database_url = get_database_url()

# Create database engine
engine = create_engine(
    database_url,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,
    max_overflow=20,
    connect_args={
        "sslmode": "require",  # Required for AWS RDS
        "connect_timeout": 10,
    },
)


@event.listens_for(engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    """Apply SSL context when establishing connection"""
    if settings.USE_AWS_RDS:
        dbapi_connection.set_isolation_level(0)


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    Dependency to get database session for FastAPI routes.
    
    Usage in routes:
        @app.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Create all database tables based on defined models"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all database tables (use with caution)"""
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
