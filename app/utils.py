"""
Authentication and utility functions
"""
import os
import random
import string
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext


# Password hashing configuration
# Using multiple algorithms with bcrypt as primary for better compatibility
pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    deprecated="pbkdf2_sha256"
)

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-please-change-this!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES", "5"))


# ============================================================
# Password Hashing Functions
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# OTP Generation Functions
# ============================================================

def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP code
    
    Args:
        length: Length of OTP (default 6 digits)
        
    Returns:
        Random OTP code as string
    """
    return ''.join(random.choices(string.digits, k=length))


def get_otp_expiry_time(minutes: int = OTP_EXPIRE_MINUTES) -> datetime:
    """
    Get OTP expiration time
    
    Args:
        minutes: Minutes until expiration (default from config)
        
    Returns:
        Datetime of OTP expiration
    """
    return datetime.utcnow() + timedelta(minutes=minutes)


# ============================================================
# JWT Token Functions
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Custom expiration time
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token data
        
    Raises:
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


# ============================================================
# Validation Functions
# ============================================================

def validate_mobile_number(mobile_number: str) -> bool:
    """
    Basic mobile number validation
    
    Args:
        mobile_number: Mobile number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove any non-digit characters except leading +
    cleaned = mobile_number.lstrip('+')
    return cleaned.isdigit() and len(cleaned) >= 9 and len(cleaned) <= 15
