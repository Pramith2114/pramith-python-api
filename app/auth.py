"""
Authentication routes for username/password and OTP-based authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, OTP
from app.schemas import (
    UserCreate, UserResponse, LoginRequest, LoginResponse,
    OTPRequest, OTPResponse, OTPVerifyRequest, OTPVerifyResponse,
    ChangePasswordRequest, MessageResponse, UserOTPSignup
)
from app.utils import (
    hash_password, verify_password, generate_otp, 
    create_access_token, get_otp_expiry_time,
    OTP_EXPIRE_MINUTES, validate_mobile_number
)


auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


# ============================================================
# Username/Password Authentication Routes
# ============================================================

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user with username and password
    
    - **username**: Unique username (required)
    - **email**: Valid email address (required)
    - **password**: Password (minimum 6 characters)
    - **mobile_number**: Optional mobile number
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered"
        )
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        mobile=user_data.mobile_number,
        password_hash=hash_password(user_data.password),
        is_verified=True  # Mark as verified for username/password auth
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.post("/login", response_model=LoginResponse)
async def login_user(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with username and password
    
    - **username**: Registered username
    - **password**: User password
    
    Returns access token for API requests
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@auth_router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    user: User = Depends(lambda db=Depends(get_db): db),  # Would need middleware for this
    db: Session = Depends(get_db)
):
    """
    Change user password (requires authentication)
    """
    # In a real app, you'd extract user from JWT token
    # This is a simplified version
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Requires JWT middleware implementation"
    )


# ============================================================
# OTP-Based Authentication Routes
# ============================================================

@auth_router.post("/otp/send", response_model=OTPResponse)
async def send_otp(
    request: OTPRequest,
    db: Session = Depends(get_db)
):
    """
    Send OTP to mobile number
    
    - **mobile_number**: Valid mobile number (9-15 digits, optional +)
    
    Generates and sends a 6-digit OTP. OTP is valid for 5 minutes.
    """
    if not validate_mobile_number(request.mobile_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid mobile number format"
        )
    
    # Generate OTP
    otp_code = generate_otp()
    expiry_time = get_otp_expiry_time()
    
    # Check if OTP already exists for this number
    existing_otp = db.query(OTP).filter(
        (OTP.mobile_number == request.mobile_number) & 
        (OTP.is_verified == False) &
        (OTP.expires_at > datetime.utcnow())
    ).first()
    
    if existing_otp:
        # Update existing OTP
        existing_otp.otp_code = otp_code
        existing_otp.expires_at = expiry_time
        existing_otp.attempts = 0
    else:
        # Create new OTP record
        new_otp = OTP(
            mobile_number=request.mobile_number,
            otp_code=otp_code,
            expires_at=expiry_time
        )
        db.add(new_otp)
    
    db.commit()
    
    # TODO: Integrate with SMS service (Twilio, AWS SNS, etc.)
    # For now, log the OTP
    print(f"📱 OTP for {request.mobile_number}: {otp_code}")
    
    return {
        "message": f"OTP sent to {request.mobile_number}",
        "mobile_number": request.mobile_number,
        "expires_in_seconds": OTP_EXPIRE_MINUTES * 60
    }


@auth_router.post("/otp/verify", response_model=OTPVerifyResponse)
async def verify_otp(
    request: OTPVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify OTP and authenticate/register user
    
    - **mobile_number**: Mobile number that received OTP
    - **otp_code**: 6-digit OTP code
    
    If user exists, returns access token. If new user, creates account.
    """
    # Find valid OTP
    otp_record = db.query(OTP).filter(
        (OTP.mobile_number == request.mobile_number) &
        (OTP.is_verified == False) &
        (OTP.expires_at > datetime.utcnow())
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found or expired. Request a new OTP."
        )
    
    # Check if max attempts exceeded
    if otp_record.attempts >= otp_record.max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Maximum OTP verification attempts exceeded. Request a new OTP."
        )
    
    # Verify OTP code
    if otp_record.otp_code != request.otp_code:
        otp_record.attempts += 1
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid OTP. Attempts remaining: {otp_record.max_attempts - otp_record.attempts}"
        )
    
    # Mark OTP as verified
    otp_record.is_verified = True
    db.commit()
    
    # Check if user exists
    user = db.query(User).filter(User.mobile == request.mobile_number).first()
    
    if not user:
        # Create new user with mobile number (no email required)
        mobile_clean = request.mobile_number.replace('+', '').replace('-', '')
        user = User(
            mobile_number=request.mobile_number,
            username=f"mobile_user_{mobile_clean}",
            email=None,  # No email for mobile-only users
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Ensure user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "mobile": request.mobile_number})
    
    return {
        "message": "OTP verified successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# ============================================================
# Utility Routes
# ============================================================

@auth_router.get("/health")
async def auth_health_check():
    """Health check endpoint for authentication service"""
    return {
        "status": "healthy",
        "service": "authentication",
        "timestamp": datetime.utcnow()
    }
