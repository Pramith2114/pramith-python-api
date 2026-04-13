"""
Database models using SQLAlchemy ORM
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    """User model with authentication support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)  # Nullable for mobile-only users
    username = Column(String(255), unique=True, index=True, nullable=False)
    mobile_number = Column(String(20), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=True)  # For username/password auth
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Email/Mobile verification status
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OTP(Base):
    """OTP model for mobile number based authentication"""
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String(20), index=True, nullable=False)
    otp_code = Column(String(6), nullable=False)  # 6-digit OTP
    is_verified = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)  # Failed verification attempts
    max_attempts = Column(Integer, default=5)  # Maximum allowed attempts
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # OTP expiration time
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Item(Base):
    """Item model example"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
