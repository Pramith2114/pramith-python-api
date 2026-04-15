"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    role: str = Field(default="patient", description="User role: patient, doctor, admin, vendor")


class UserCreate(BaseModel):
    """Schema for creating a user (supports both new and legacy fields)"""
    # New User API fields
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    role: str = Field(default="patient", description="User role: patient, doctor, admin, vendor")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    
    # Legacy authentication fields
    username: Optional[str] = None
    mobile_number: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: UUID
    is_verified: bool
    created_at: datetime
    # Legacy fields for backward compatibility
    username: Optional[str] = None
    is_active: bool = True
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """Schema for user in database (includes password hash)"""
    password_hash: Optional[str] = None
    
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


class UserOTPSignup(BaseModel):
    """Schema for OTP-based user signup"""
    mobile_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$", description="Valid mobile number")
    email: Optional[EmailStr] = None
    username: Optional[str] = None


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


# ============================================================
# Doctor Schemas (new)
# ============================================================

class DoctorBase(BaseModel):
    """Base doctor schema"""
    specialization: str
    experience: int = Field(..., ge=0, description="Years of experience (non-negative)")
    consultation_fee: float = Field(..., gt=0, description="Consultation fee (must be positive)")


class DoctorCreate(DoctorBase):
    """Schema for creating a doctor profile"""
    user_id: int


class DoctorUpdate(BaseModel):
    """Schema for updating a doctor profile"""
    specialization: Optional[str] = None
    experience: Optional[int] = Field(None, ge=0, description="Years of experience (non-negative)")
    consultation_fee: Optional[float] = Field(None, gt=0, description="Consultation fee (must be positive)")


class DoctorVerificationUpdate(BaseModel):
    """Schema for updating doctor verification status"""
    verification_status: str = Field(..., description="Status: pending, approved, rejected")
    
    class Config:
        validate_assignment = True


class DoctorResponse(DoctorBase):
    """Schema for doctor response"""
    id: UUID
    user_id: int
    verification_status: str
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DoctorDetailResponse(DoctorResponse):
    """Extended doctor response with user details"""
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# ============================================================
# Doctor Document Schemas (new)
# ============================================================

class DoctorDocumentBase(BaseModel):
    """Base doctor document schema"""
    document_type: str = Field(..., description="Type of document (e.g., license, degree, certification)")
    file_url: str = Field(..., description="URL to the uploaded document file")


class DoctorDocumentCreate(DoctorDocumentBase):
    """Schema for uploading a doctor document"""
    doctor_id: UUID = Field(..., description="UUID of the doctor")


class DoctorDocumentUpdate(BaseModel):
    """Schema for updating a doctor document"""
    document_type: Optional[str] = None
    file_url: Optional[str] = None


class DoctorDocumentVerify(BaseModel):
    """Schema for verifying a doctor document"""
    verified: bool = Field(..., description="Verification status")


class DoctorDocumentResponse(DoctorDocumentBase):
    """Schema for doctor document response"""
    id: UUID
    doctor_id: UUID
    verified: bool
    uploaded_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Drug Schemas (new)
# ============================================================

class DrugBase(BaseModel):
    """Base drug schema"""
    name: str = Field(..., description="Brand name of the drug")
    generic_name: str = Field(..., description="Generic/chemical name of the drug")
    manufacturer: str = Field(..., description="Drug manufacturer")
    price: float = Field(..., gt=0, description="Price per unit (must be positive)")
    stock_quantity: int = Field(..., ge=0, description="Available stock quantity (non-negative)")


class DrugCreate(BaseModel):
    """Schema for creating a drug"""
    name: str = Field(..., description="Brand name of the drug")
    generic_name: str = Field(..., description="Generic/chemical name of the drug")
    manufacturer: str = Field(..., description="Drug manufacturer")
    price: float = Field(..., gt=0, description="Price per unit (must be positive)")
    stock_quantity: int = Field(..., ge=0, description="Available stock quantity (non-negative)")
    expiry_date: str = Field(..., description="Drug expiry date (YYYY-MM-DD)")


class DrugUpdate(BaseModel):
    """Schema for updating a drug"""
    name: Optional[str] = None
    generic_name: Optional[str] = None
    manufacturer: Optional[str] = None
    price: Optional[float] = Field(None, gt=0, description="Price per unit (must be positive)")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Stock quantity (non-negative)")
    expiry_date: Optional[str] = None


class DrugResponse(DrugBase):
    """Schema for drug response"""
    id: UUID
    expiry_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Stock Transaction Schemas (new)
# ============================================================

class StockTransactionBase(BaseModel):
    """Base stock transaction schema"""
    drug_id: UUID = Field(..., description="UUID of the drug")
    quantity: int = Field(..., gt=0, description="Quantity (must be positive)")
    type: str = Field(..., description="Transaction type: 'IN' or 'OUT'")
    source: str = Field(..., description="Source of transaction (e.g., vendor, prescription, adjustment)")


class StockTransactionCreate(StockTransactionBase):
    """Schema for creating a stock transaction"""
    pass


class StockTransactionUpdate(BaseModel):
    """Schema for updating a stock transaction"""
    quantity: Optional[int] = Field(None, gt=0, description="Quantity (must be positive)")
    source: Optional[str] = None


class StockTransactionResponse(StockTransactionBase):
    """Schema for stock transaction response"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockTransactionDetailResponse(StockTransactionResponse):
    """Extended stock transaction response with drug details"""
    drug: Optional[DrugBase] = None
    
    class Config:
        from_attributes = True


# ============================================================
# Vendor Schemas (new)
# ============================================================

class VendorBase(BaseModel):
    """Base vendor schema"""
    name: str = Field(..., description="Vendor/supplier name")
    contact_number: str = Field(..., description="Vendor contact number")
    email: str = Field(..., description="Vendor email address")
    address: str = Field(..., description="Vendor address")


class VendorCreate(VendorBase):
    """Schema for creating a vendor"""
    pass


class VendorUpdate(BaseModel):
    """Schema for updating a vendor"""
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class VendorResponse(VendorBase):
    """Schema for vendor response"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Vendor Order Schemas (new)
# ============================================================

class VendorOrderBase(BaseModel):
    """Base vendor order schema"""
    vendor_id: UUID = Field(..., description="UUID of the vendor")
    total_amount: float = Field(..., gt=0, description="Total order amount (must be positive)")
    status: str = Field(..., description="Order status: pending, confirmed, shipped, delivered, cancelled")


class VendorOrderCreate(BaseModel):
    """Schema for creating a vendor order"""
    vendor_id: UUID = Field(..., description="UUID of the vendor")
    total_amount: float = Field(..., gt=0, description="Total order amount (must be positive)")
    status: str = Field(default="pending", description="Order status (default: pending)")


class VendorOrderUpdate(BaseModel):
    """Schema for updating a vendor order"""
    total_amount: Optional[float] = Field(None, gt=0, description="Total order amount (must be positive)")
    status: Optional[str] = None


class VendorOrderResponse(VendorOrderBase):
    """Schema for vendor order response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True



class VendorOrderDetailResponse(VendorOrderResponse):
    """Extended vendor order response with vendor details"""
    vendor: Optional[VendorResponse] = None
    
    class Config:
        from_attributes = True


# ============================================================
# Appointment Schemas (new)
# ============================================================

class AppointmentBase(BaseModel):
    """Base appointment schema"""
    patient_id: UUID = Field(..., description="UUID of the patient")
    doctor_id: UUID = Field(..., description="UUID of the doctor")
    appointment_date: str = Field(..., description="Appointment date (YYYY-MM-DD)")
    time_slot: str = Field(..., description="Time slot (e.g., 09:00-09:30)")
    status: str = Field(..., description="Appointment status: scheduled, completed, cancelled, no-show, rescheduled")
    notes: Optional[str] = Field(None, description="Additional notes about appointment")


class AppointmentCreate(BaseModel):
    """Schema for creating an appointment"""
    patient_id: UUID = Field(..., description="UUID of the patient")
    doctor_id: UUID = Field(..., description="UUID of the doctor")
    appointment_date: str = Field(..., description="Appointment date (YYYY-MM-DD)")
    time_slot: str = Field(..., description="Time slot (e.g., 09:00-09:30)")
    status: str = Field(default="scheduled", description="Appointment status (default: scheduled)")
    notes: Optional[str] = Field(None, description="Additional notes about appointment")


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment"""
    appointment_date: Optional[str] = None
    time_slot: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AppointmentDetailResponse(AppointmentResponse):
    """Extended appointment response with patient and doctor details"""
    patient: Optional[UserResponse] = None
    doctor: Optional[DoctorResponse] = None
    
    class Config:
        from_attributes = True


# ============================================================
# Prescription Schemas
# ============================================================

class PrescriptionItemBase(BaseModel):
    """Base prescription item schema"""
    drug_id: UUID = Field(..., description="UUID of the drug")
    dosage: str = Field(..., description="Drug dosage (e.g., 500mg, 10ml)")
    duration: str = Field(..., description="Duration (e.g., 7 days, 2 weeks)")
    instructions: Optional[str] = Field(None, description="Usage instructions")


class PrescriptionItemCreate(BaseModel):
    """Schema for creating a prescription item"""
    drug_id: UUID = Field(..., description="UUID of the drug")
    dosage: str = Field(..., description="Drug dosage (e.g., 500mg, 10ml)")
    duration: str = Field(..., description="Duration (e.g., 7 days, 2 weeks)")
    instructions: Optional[str] = Field(None, description="Usage instructions")


class PrescriptionItemResponse(PrescriptionItemBase):
    """Schema for prescription item response"""
    id: UUID
    prescription_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PrescriptionBase(BaseModel):
    """Base prescription schema"""
    appointment_id: UUID = Field(..., description="UUID of the appointment")
    doctor_id: UUID = Field(..., description="UUID of the doctor")
    patient_id: UUID = Field(..., description="UUID of the patient")
    notes: Optional[str] = Field(None, description="Additional prescription notes")


class PrescriptionCreate(BaseModel):
    """Schema for creating a prescription"""
    appointment_id: UUID = Field(..., description="UUID of the appointment")
    doctor_id: UUID = Field(..., description="UUID of the doctor")
    patient_id: UUID = Field(..., description="UUID of the patient")
    notes: Optional[str] = Field(None, description="Additional prescription notes")
    items: Optional[list[PrescriptionItemCreate]] = Field(None, description="Prescription items")


class PrescriptionUpdate(BaseModel):
    """Schema for updating a prescription"""
    notes: Optional[str] = None


class PrescriptionResponse(PrescriptionBase):
    """Schema for prescription response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PrescriptionDetailResponse(PrescriptionResponse):
    """Extended prescription response with related items and details"""
    items: Optional[list[PrescriptionItemResponse]] = None
    
    class Config:
        from_attributes = True


# ============================================================
# Medical Records Schemas
# ============================================================

class MedicalRecordBase(BaseModel):
    """Base medical record schema"""
    patient_id: UUID = Field(..., description="UUID of the patient")
    file_url: str = Field(..., description="URL to the medical record file")
    record_type: str = Field(..., description="Type of record (lab_report, x_ray, prescription, discharge_summary, etc.)")
    description: Optional[str] = Field(None, description="Description or notes about the record")


class MedicalRecordCreate(BaseModel):
    """Schema for creating a medical record"""
    patient_id: UUID = Field(..., description="UUID of the patient")
    file_url: str = Field(..., description="URL to the medical record file")
    record_type: str = Field(..., description="Type of record (lab_report, x_ray, prescription, discharge_summary, etc.)")
    description: Optional[str] = Field(None, description="Description or notes about the record")


class MedicalRecordUpdate(BaseModel):
    """Schema for updating a medical record"""
    file_url: Optional[str] = None
    record_type: Optional[str] = None
    description: Optional[str] = None


class MedicalRecordResponse(MedicalRecordBase):
    """Schema for medical record response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PAYMENT SCHEMAS ====================

class PaymentBase(BaseModel):
    """Base schema for payment"""
    user_id: UUID = Field(..., description="UUID of the user making the payment")
    amount: Decimal = Field(..., description="Payment amount")
    payment_method: str = Field(..., description="Payment method (credit_card, debit_card, upi, bank_transfer, etc.)")
    payment_status: str = Field(default='pending', description="Payment status (pending, completed, failed, refunded)")
    transaction_id: str = Field(..., description="Unique transaction identifier")


class PaymentCreate(BaseModel):
    """Schema for creating a payment"""
    user_id: UUID = Field(..., description="UUID of the user making the payment")
    amount: Decimal = Field(..., description="Payment amount")
    payment_method: str = Field(..., description="Payment method (credit_card, debit_card, upi, bank_transfer, etc.)")
    transaction_id: str = Field(..., description="Unique transaction identifier")


class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""
    payment_status: Optional[str] = None
    amount: Optional[Decimal] = None
    payment_method: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Schema for payment response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== INVOICE SCHEMAS ====================

class InvoiceItemBase(BaseModel):
    """Base schema for invoice item"""
    item_type: str = Field(..., description="Type of item (drug, consultation, service, etc.)")
    item_id: UUID = Field(..., description="UUID of the specific item")
    quantity: int = Field(default=1, description="Quantity of items")
    price: Decimal = Field(..., description="Unit price of item")


class InvoiceItemCreate(BaseModel):
    """Schema for creating an invoice item"""
    item_type: str = Field(..., description="Type of item (drug, consultation, service, etc.)")
    item_id: UUID = Field(..., description="UUID of the specific item")
    quantity: int = Field(default=1, description="Quantity of items")
    price: Decimal = Field(..., description="Unit price of item")


class InvoiceItemUpdate(BaseModel):
    """Schema for updating an invoice item"""
    item_type: Optional[str] = None
    item_id: Optional[UUID] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None


class InvoiceItemResponse(InvoiceItemBase):
    """Schema for invoice item response"""
    id: UUID
    invoice_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    """Base schema for invoice"""
    user_id: UUID = Field(..., description="UUID of the user")
    total_amount: Decimal = Field(..., description="Total invoice amount")
    status: str = Field(default='draft', description="Invoice status (draft, issued, paid, overdue, cancelled)")


class InvoiceCreate(BaseModel):
    """Schema for creating an invoice"""
    user_id: UUID = Field(..., description="UUID of the user")
    total_amount: Decimal = Field(..., description="Total invoice amount")


class InvoiceUpdate(BaseModel):
    """Schema for updating an invoice"""
    status: Optional[str] = None
    total_amount: Optional[Decimal] = None


class InvoiceResponse(InvoiceBase):
    """Schema for invoice response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceDetailResponse(InvoiceBase):
    """Schema for detailed invoice response with items"""
    id: UUID
    items: list[InvoiceItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    """Base schema for notification"""
    user_id: UUID = Field(..., description="UUID of the user")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message content")
    type: str = Field(..., description="Notification type (alert, info, warning, success, error)")


class NotificationCreate(NotificationBase):
    """Schema for creating a notification"""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: UUID
    is_read: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SearchLogBase(BaseModel):
    """Base schema for search log"""
    user_id: UUID = Field(..., description="UUID of the user")
    query: str = Field(..., description="Search query text")
    results_count: int = Field(default=0, description="Number of results returned")


class SearchLogCreate(SearchLogBase):
    """Schema for creating a search log"""
    pass


class SearchLogUpdate(BaseModel):
    """Schema for updating a search log"""
    results_count: Optional[int] = None


class SearchLogResponse(SearchLogBase):
    """Schema for search log response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SymptomCheckerBase(BaseModel):
    """Base schema for symptom checker"""
    symptoms: str = Field(..., description="Comma-separated symptoms or symptom description")
    suggested_disease: str = Field(..., description="Disease suggestion based on symptoms")
    confidence_score: Decimal = Field(..., description="Confidence score (0.00-1.00)")


class SymptomCheckerCreate(SymptomCheckerBase):
    """Schema for creating a symptom checker record"""
    pass


class SymptomCheckerUpdate(BaseModel):
    """Schema for updating a symptom checker record"""
    symptoms: Optional[str] = None
    suggested_disease: Optional[str] = None
    confidence_score: Optional[Decimal] = None


class SymptomCheckerResponse(SymptomCheckerBase):
    """Schema for symptom checker response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


