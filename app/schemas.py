"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    email: Optional[EmailStr] = None
    username: str


class UserCreate(UserBase):
    """Schema for creating a user with username/password"""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    mobile_number: Optional[str] = None


class UserOTPSignup(BaseModel):
    """Schema for OTP-based user signup"""
    mobile_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$", description="Valid mobile number")
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    mobile_number: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Authentication Schemas
# ============================================================

class LoginRequest(BaseModel):
    """Schema for username/password login"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class OTPRequest(BaseModel):
    """Schema for requesting OTP"""
    mobile_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$", description="Valid mobile number")


class OTPResponse(BaseModel):
    """Schema for OTP response"""
    message: str
    mobile_number: str
    expires_in_seconds: int


class OTPVerifyRequest(BaseModel):
    """Schema for OTP verification"""
    mobile_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$", description="Valid mobile number")
    otp_code: str = Field(..., pattern=r"^\d{6}$", description="6-digit OTP code")


class OTPVerifyResponse(BaseModel):
    """Schema for OTP verification response"""
    message: str
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    old_password: str
    new_password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


# ============================================================
# Item Schemas (existing)
# ============================================================

class ItemBase(BaseModel):
    """Base item schema"""
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating an item"""
    pass


class ItemResponse(ItemBase):
    """Schema for item response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
