"""
Database models using SQLAlchemy ORM
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, CheckConstraint, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid


Base = declarative_base()


class User(Base):
    """User model with UUID primary key and role-based access"""
    __tablename__ = "users"
    
    # New User API fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=True)
    mobile = Column(String(20), unique=True, index=True, nullable=True)
    email = Column(String(255), nullable=True)
    password_hash = Column(Text, nullable=True)
    role = Column(String(50), nullable=False, default='patient')  # patient, doctor, admin, vendor
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Legacy authentication fields (for backward compatibility with existing auth.py)
    username = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("role IN ('patient', 'doctor', 'admin', 'vendor')", name='valid_role'),
    )


class Doctor(Base):
    """Doctor model with verification status"""
    __tablename__ = "doctors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    specialization = Column(String(255), nullable=False)
    experience = Column(Integer, nullable=False, default=0)  # Years of experience
    consultation_fee = Column(Numeric(10, 2), nullable=False)  # Decimal for currency
    verification_status = Column(String(50), nullable=False, default='pending')  # pending, approved, rejected
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("verification_status IN ('pending', 'approved', 'rejected')", name='valid_verification_status'),
    )


class DoctorDocument(Base):
    """Doctor documents model for storing doctor credentials and certifications"""
    __tablename__ = "doctor_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False, index=True)
    document_type = Column(String(255), nullable=False)  # e.g., license, degree, certification
    file_url = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Drug(Base):
    """Drug/Medicine model for pharmacy management"""
    __tablename__ = "drugs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)  # Brand name
    generic_name = Column(String(255), nullable=False, index=True)  # Generic/chemical name
    manufacturer = Column(String(255), nullable=False)  # Manufacturer name
    price = Column(Numeric(10, 2), nullable=False)  # Price per unit
    stock_quantity = Column(Integer, nullable=False, default=0)  # Available quantity
    expiry_date = Column(Date, nullable=False)  # Expiry date
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StockTransaction(Base):
    """Stock transaction model for tracking inventory changes"""
    __tablename__ = "stock_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    drug_id = Column(UUID(as_uuid=True), ForeignKey("drugs.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)  # Quantity added/removed
    type = Column(String(10), nullable=False)  # 'IN' or 'OUT'
    source = Column(String(255), nullable=False)  # vendor/prescription/adjustment
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        CheckConstraint("type IN ('IN','OUT')", name='valid_transaction_type'),
    )


class Vendor(Base):
    """Vendor model for managing pharmaceutical vendors/suppliers"""
    __tablename__ = "vendors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VendorOrder(Base):
    """Vendor order model for tracking purchase orders"""
    __tablename__ = "vendor_orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    total_amount = Column(Numeric(12, 2), nullable=False)  # Total order amount
    status = Column(String(50), nullable=False, default='pending')  # pending, confirmed, shipped, delivered, cancelled
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')", name='valid_order_status'),
    )


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
