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
    role = Column(String(50), nullable=False, default='patient')  # patient, doctor, admin, vendor, medical
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Legacy authentication fields (for backward compatibility with existing auth.py)
    username = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("role IN ('patient', 'doctor', 'admin', 'vendor', 'medical')", name='valid_role'),
    )


class Doctor(Base):
    """Doctor model with verification status"""
    __tablename__ = "doctors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    specialization = Column(String(255), nullable=False)
    profile_picture = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    about_me = Column(Text, nullable=True)
    working_time = Column(String(255), nullable=True)
    experience = Column(Integer, nullable=False, default=0)  # Years of experience
    consultation_fee = Column(Numeric(10, 2), nullable=False)  # Decimal for currency
    patients = Column(Integer, nullable=False, default=0)
    rating = Column(Numeric(3, 2), nullable=False, default=0.0)
    reviews = Column(Integer, nullable=False, default=0)
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


class DoctorCategory(Base):
    """Doctor category lookup table (e.g., Cardiology, Pediatrics)"""
    __tablename__ = "doctor_categories"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), nullable=False, unique=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


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


class Appointment(Base):
    """Appointment model for managing patient-doctor appointments"""
    __tablename__ = "appointments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False, index=True)
    appointment_date = Column(Date, nullable=False, index=True)
    time_slot = Column(String(50), nullable=False)  # e.g., 09:00-09:30, 10:00-10:30
    status = Column(String(50), nullable=False, default='scheduled')  # scheduled, completed, cancelled, no-show, rescheduled
    notes = Column(Text, nullable=True)  # Additional notes about appointment
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled')", name='valid_appointment_status'),
    )


class Prescription(Base):
    """Prescription model for managing drug prescriptions"""
    __tablename__ = "prescriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=False, index=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    notes = Column(Text, nullable=True)  # Additional prescription notes
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PrescriptionItem(Base):
    """Prescription items model for storing individual drugs in a prescription"""
    __tablename__ = "prescription_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    prescription_id = Column(UUID(as_uuid=True), ForeignKey("prescriptions.id"), nullable=False, index=True)
    drug_id = Column(UUID(as_uuid=True), ForeignKey("drugs.id"), nullable=False, index=True)
    dosage = Column(String(100), nullable=False)  # e.g., "500mg", "10ml"
    duration = Column(String(100), nullable=False)  # e.g., "7 days", "2 weeks"
    instructions = Column(Text, nullable=True)  # e.g., "Take twice daily after meals"
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MedicalRecord(Base):
    """Medical records model for storing patient medical documents"""
    __tablename__ = "medical_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    file_url = Column(Text, nullable=False)  # URL to the uploaded file
    record_type = Column(String(100), nullable=False, index=True)  # e.g., lab_report, x_ray, prescription, discharge_summary
    description = Column(Text, nullable=True)  # Description or notes about the record
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    """Payment model for managing payment transactions"""
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)  # Payment amount with 2 decimal places
    payment_method = Column(String(50), nullable=False, index=True)  # credit_card, debit_card, upi, bank_transfer, etc.
    payment_status = Column(String(50), nullable=False, default='pending', index=True)  # pending, completed, failed, refunded
    transaction_id = Column(String(255), unique=True, nullable=False, index=True)  # Unique transaction ID
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("payment_status IN ('pending', 'completed', 'failed', 'refunded')", name='valid_payment_status'),
    )


class Invoice(Base):
    """Invoice model for managing invoices"""
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Numeric(12, 2), nullable=False)  # Total invoice amount with 2 decimal places
    status = Column(String(50), nullable=False, default='draft', index=True)  # draft, issued, paid, overdue, cancelled
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('draft', 'issued', 'paid', 'overdue', 'cancelled')", name='valid_invoice_status'),
    )


class InvoiceItem(Base):
    """Invoice items model for line items in invoices"""
    __tablename__ = "invoice_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True)
    item_type = Column(String(50), nullable=False)  # drug, consultation, service, etc.
    item_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # UUID reference to the actual item
    quantity = Column(Integer, nullable=False, default=1)  # Quantity of items
    price = Column(Numeric(12, 2), nullable=False)  # Unit price of item
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Notification(Base):
    """Notification model for managing user notifications"""
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)  # Notification title
    message = Column(Text, nullable=False)  # Notification message content
    type = Column(String(50), nullable=False, index=True)  # alert, info, warning, success, error
    is_read = Column(Boolean, default=False, index=True)  # Read status
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("type IN ('alert', 'info', 'warning', 'success', 'error')", name='valid_notification_type'),
    )


class SearchLog(Base):
    """Search logs model for tracking user searches"""
    __tablename__ = "search_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    query = Column(Text, nullable=False)  # Search query text
    results_count = Column(Integer, nullable=False, default=0)  # Number of results returned
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SymptomChecker(Base):
    """Symptom checker model for tracking symptoms and suggested diseases"""
    __tablename__ = "symptom_checkers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symptoms = Column(Text, nullable=False)  # Comma-separated symptoms
    suggested_disease = Column(Text, nullable=False)  # Disease suggestion
    confidence_score = Column(Numeric(3, 2), nullable=False)  # Confidence 0.00-1.00
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OTPVerification(Base):
    """OTP Verification model for managing one-time passwords"""
    __tablename__ = "otp_verifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile = Column(String(20), nullable=False, index=True)  # Mobile phone number
    otp = Column(String(10), nullable=False)  # One-time password
    expires_at = Column(DateTime, nullable=False, index=True)  # Expiration timestamp
    is_verified = Column(Boolean, default=False, index=True)  # Verification status
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
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
