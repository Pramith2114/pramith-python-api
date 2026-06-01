"""
API routes for users, doctors, items, and drugs
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import bcrypt

from app.database import get_db
from app.models import User, Item, Doctor, DoctorDocument, DoctorCategory, Drug, StockTransaction, Vendor, VendorOrder, Appointment, Prescription, PrescriptionItem, MedicalRecord, Payment, Invoice, InvoiceItem, Notification, SearchLog, SymptomChecker, OTPVerification
from app.schemas import (
    UserCreate, UserResponse, UserUpdate, UserInDB, 
    ItemCreate, ItemResponse,
    DoctorCreate, DoctorResponse, DoctorUpdate, DoctorDetailResponse, DoctorWithUserInfoResponse, DoctorVerificationUpdate,
    DoctorDocumentCreate, DoctorDocumentResponse, DoctorDocumentUpdate, DoctorDocumentVerify,
    DoctorCategoryCreate, DoctorCategoryResponse,
    DrugCreate, DrugResponse, DrugUpdate,
    StockTransactionCreate, StockTransactionResponse, StockTransactionUpdate, StockTransactionDetailResponse,
    VendorCreate, VendorResponse, VendorUpdate,
    VendorOrderCreate, VendorOrderResponse, VendorOrderUpdate, VendorOrderDetailResponse,
    AppointmentCreate, AppointmentResponse, AppointmentUpdate, AppointmentDetailResponse,
    PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate, PrescriptionDetailResponse,
    PrescriptionItemCreate, PrescriptionItemResponse,
    MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate,
    PaymentCreate, PaymentResponse, PaymentUpdate,
    InvoiceCreate, InvoiceResponse, InvoiceUpdate, InvoiceDetailResponse,
    InvoiceItemCreate, InvoiceItemResponse, InvoiceItemUpdate,
    NotificationCreate, NotificationResponse, NotificationUpdate,
    SearchLogCreate, SearchLogResponse, SearchLogUpdate,
    SymptomCheckerCreate, SymptomCheckerResponse, SymptomCheckerUpdate,
    OTPVerificationCreate, OTPVerificationResponse, OTPVerificationUpdate, OTPVerificationRequest, OTPVerificationCheckRequest, OTPVerificationCheckResponse
)

# ============================================================
# User Router
# ============================================================

user_router = APIRouter(prefix="/api/users", tags=["users"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user
    
    - **name**: User's full name (optional)
    - **mobile**: User's mobile number (unique)
    - **email**: User's email (optional)
    - **password**: User's password (minimum 6 characters)
    - **role**: User's role (patient, doctor, admin, vendor)
    """
    # Check if user already exists by mobile or email
    if user.mobile:
        existing_user = db.query(User).filter(User.mobile == user.mobile).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already registered"
            )
    
    if user.email:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Hash password
    password_hash = hash_password(user.password)
    
    # Create user
    db_user = User(
        name=user.name,
        mobile=user.mobile,
        email=user.email,
        password_hash=password_hash,
        role=user.role,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    role: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all users with optional filtering
    
    - **skip**: Number of users to skip (default: 0)
    - **limit**: Maximum number of users to return (default: 10)
    - **role**: Filter by role (optional)
    """
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    return users


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.get("/mobile/{mobile}", response_model=UserResponse)
async def get_user_by_mobile(
    mobile: str,
    db: Session = Depends(get_db),
):
    """Get a user by mobile number"""
    user = db.query(User).filter(User.mobile == mobile).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a user
    
    - **name**: Update user's name (optional)
    - **email**: Update user's email (optional)
    - **role**: Update user's role (optional)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check if email is being updated and if it's already in use
    if user_update.email and user_update.email != user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update fields
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.role is not None:
        user.role = user_update.role
    
    db.commit()
    db.refresh(user)
    return user


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()


@user_router.post("/{user_id}/verify", response_model=UserResponse)
async def verify_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Mark a user as verified"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


# ============================================================
# Item Router (existing)
# ============================================================

item_router = APIRouter(prefix="/api/items", tags=["items"])


@item_router.post("", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    """Create a new item in the database"""
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@item_router.get("", response_model=list[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get all active items from the database"""
    items = db.query(Item).filter(Item.is_active == True).offset(skip).limit(limit).all()
    return items


@item_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific item by ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ============================================================
# Doctor Router (new)
# ============================================================

doctor_router = APIRouter(prefix="/api/doctors", tags=["doctors"])


@doctor_router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new doctor profile
    
    - **user_id**: UUID of existing user (must have role='doctor')
    - **specialization**: Medical specialization (e.g., Cardiology, Pediatrics)
    - **profile_picture**: URL to doctor's profile picture
    - **address**: Clinic or practice address
    - **city**: Clinic city
    - **state**: Clinic state
    - **country**: Clinic country
    - **about_me**: Doctor biography or description
    - **working_time**: Working hours or schedule
    - **experience**: Years of experience (non-negative integer)
    - **consultation_fee**: Consultation fee (positive decimal)
    - **patients**: Number of patients seen
    - **rating**: Average patient rating (0-5)
    - **reviews**: Number of reviews
    """
    try:
        # Log incoming payload for debugging
        try:
            print("[doctors.create] incoming:", doctor_data.model_dump() if hasattr(doctor_data, 'model_dump') else dict(doctor_data))
        except Exception:
            print("[doctors.create] incoming: <could not serialize>")

        # Check if user exists
        user = db.query(User).filter(User.id == doctor_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Optionally check if user has doctor role
        if (user.role or '').lower() != 'doctor':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must have 'doctor' role"
            )

        # Check if doctor profile already exists
        existing_doctor = db.query(Doctor).filter(Doctor.user_id == doctor_data.user_id).first()
        if existing_doctor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor profile already exists for this user"
            )

        # Normalize/validate numeric fields
        experience_val = int(doctor_data.experience)
        consultation_fee_val = float(doctor_data.consultation_fee)
        patients_val = int(doctor_data.patients or 0)
        rating_val = float(doctor_data.rating or 0.0)
        reviews_val = int(doctor_data.reviews or 0)

        # Create doctor profile
        db_doctor = Doctor(
            user_id=doctor_data.user_id,
            specialization=doctor_data.specialization,
            profile_picture=doctor_data.profile_picture,
            address=doctor_data.address,
            city=doctor_data.city,
            state=doctor_data.state,
            country=doctor_data.country,
            about_me=doctor_data.about_me,
            working_time=doctor_data.working_time,
            experience=experience_val,
            consultation_fee=consultation_fee_val,
            patients=patients_val,
            rating=rating_val,
            reviews=reviews_val,
            verification_status='pending'
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)

        # If document info provided in create payload, create a DoctorDocument record
        try:
            if getattr(doctor_data, 'file_url', None):
                doc_type = getattr(doctor_data, 'document_type', None) or 'document'
                db_document = DoctorDocument(
                    doctor_id=db_doctor.id,
                    document_type=doc_type,
                    file_url=doctor_data.file_url,
                    verified=False
                )
                db.add(db_document)
                db.commit()
                db.refresh(db_document)
                # Attach to response object
                db_doctor.document_type = db_document.document_type
                db_doctor.file_url = db_document.file_url
        except Exception:
            # Non-fatal: continue returning created doctor
            pass

        # Attach latest document info if exists (if none created above)
        try:
            if not getattr(db_doctor, 'file_url', None):
                latest_doc = db.query(DoctorDocument).filter(DoctorDocument.doctor_id == db_doctor.id).order_by(DoctorDocument.uploaded_at.desc()).first()
                if latest_doc:
                    db_doctor.document_type = latest_doc.document_type
                    db_doctor.file_url = latest_doc.file_url
        except Exception:
            pass

        return db_doctor
    except HTTPException:
        raise
    except Exception as e:
        print(f"[doctors.create] unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@doctor_router.get("", response_model=list[DoctorWithUserInfoResponse])
async def get_all_doctors(
    skip: int = 0,
    limit: int = 10,
    verification_status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all doctors with optional filtering and flattened user information
    
    - **skip**: Number of doctors to skip (default: 0)
    - **limit**: Maximum number of doctors to return (default: 10)
    - **verification_status**: Filter by status (pending, approved, rejected)
    
    Returns doctor details with user information (name, email, mobile, role) flattened at the same level
    """
    query = db.query(Doctor).join(User, Doctor.user_id == User.id)
    
    if verification_status:
        query = query.filter(Doctor.verification_status == verification_status)
    
    doctors = query.offset(skip).limit(limit).all()
    
    # Build response with flattened user details and document info
    result = []
    for d in doctors:
        # Fetch user information
        user = db.query(User).filter(User.id == d.user_id).first()
        
        # Attach latest document info for each doctor
        try:
            latest_doc = db.query(DoctorDocument).filter(DoctorDocument.doctor_id == d.id).order_by(DoctorDocument.uploaded_at.desc()).first()
            if latest_doc:
                d.document_type = latest_doc.document_type
                d.file_url = latest_doc.file_url
        except Exception:
            d.document_type = None
            d.file_url = None
        
        # Flatten user information onto doctor object
        if user:
            d.name = user.name
            d.email = user.email
            d.mobile = user.mobile
            d.role = user.role
        
        result.append(d)
    
    return result


@doctor_router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific doctor by ID"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    # Attach latest document info
    try:
        latest_doc = db.query(DoctorDocument).filter(DoctorDocument.doctor_id == doctor.id).order_by(DoctorDocument.uploaded_at.desc()).first()
        if latest_doc:
            doctor.document_type = latest_doc.document_type
            doctor.file_url = latest_doc.file_url
    except Exception:
        doctor.document_type = None
        doctor.file_url = None
    return doctor


@doctor_router.get("/user/{user_id}", response_model=DoctorResponse)
async def get_doctor_by_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Get doctor profile by user ID"""
    doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found for this user"
        )
    # Attach latest document info
    try:
        latest_doc = db.query(DoctorDocument).filter(DoctorDocument.doctor_id == doctor.id).order_by(DoctorDocument.uploaded_at.desc()).first()
        if latest_doc:
            doctor.document_type = latest_doc.document_type
            doctor.file_url = latest_doc.file_url
    except Exception:
        doctor.document_type = None
        doctor.file_url = None
    return doctor


@doctor_router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: UUID,
    doctor_update: DoctorUpdate,
    db: Session = Depends(get_db),
):
    """
    Update doctor profile information
    
    - **specialization**: Update specialization (optional)
    - **experience**: Update years of experience (optional)
    - **consultation_fee**: Update consultation fee (optional)
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Update fields
    if doctor_update.specialization is not None:
        doctor.specialization = doctor_update.specialization
    if doctor_update.profile_picture is not None:
        doctor.profile_picture = doctor_update.profile_picture
    if doctor_update.address is not None:
        doctor.address = doctor_update.address
    if doctor_update.city is not None:
        doctor.city = doctor_update.city
    if doctor_update.state is not None:
        doctor.state = doctor_update.state
    if doctor_update.country is not None:
        doctor.country = doctor_update.country
    if doctor_update.about_me is not None:
        doctor.about_me = doctor_update.about_me
    if doctor_update.working_time is not None:
        doctor.working_time = doctor_update.working_time
    if doctor_update.experience is not None:
        doctor.experience = doctor_update.experience
    if doctor_update.consultation_fee is not None:
        doctor.consultation_fee = doctor_update.consultation_fee
    if doctor_update.patients is not None:
        doctor.patients = doctor_update.patients
    if doctor_update.rating is not None:
        doctor.rating = doctor_update.rating
    if doctor_update.reviews is not None:
        doctor.reviews = doctor_update.reviews
    
    db.commit()
    db.refresh(doctor)
    return doctor


@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a doctor profile by ID"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    db.delete(doctor)
    db.commit()


@doctor_router.post("/{doctor_id}/verify", response_model=DoctorResponse)
async def verify_doctor(
    doctor_id: UUID,
    verification_data: DoctorVerificationUpdate,
    db: Session = Depends(get_db),
):
    """
    Update doctor verification status
    
    - **verification_status**: Status (pending, approved, rejected)
    
    When approved, sets verified_at timestamp automatically
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Validate status
    valid_statuses = ['pending', 'approved', 'rejected']
    if verification_data.verification_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    doctor.verification_status = verification_data.verification_status
    
    # Set verified_at timestamp if approved
    if verification_data.verification_status == 'approved':
        doctor.verified_at = datetime.utcnow()
    else:
        doctor.verified_at = None
    
    db.commit()
    db.refresh(doctor)
    return doctor


@doctor_router.post("/{doctor_id}/approve", response_model=DoctorResponse)
async def approve_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
):
    """Approve a doctor (shorthand endpoint)"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    doctor.verification_status = 'approved'
    doctor.verified_at = datetime.utcnow()
    db.commit()
    db.refresh(doctor)
    return doctor


@doctor_router.post("/{doctor_id}/reject", response_model=DoctorResponse)
async def reject_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
):
    """Reject a doctor (shorthand endpoint)"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    doctor.verification_status = 'rejected'
    doctor.verified_at = None
    db.commit()
    db.refresh(doctor)
    return doctor

# ============================================================
# Doctor documents under `/api/doctors`
# ============================================================


@doctor_router.post("/documents", response_model=DoctorDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_document(
    document: DoctorDocumentCreate,
    db: Session = Depends(get_db),
):
    """
    Upload a new doctor document under the doctors API

    - **doctor_id**: UUID of the doctor
    - **document_type**: Type of document (e.g., license, degree, certification)
    - **file_url**: URL to the uploaded file
    """
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == document.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    # Ensure associated user is a doctor
    user = db.query(User).filter(User.id == doctor.user_id).first()
    if (user.role or '').lower() != 'doctor':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Associated user must have 'doctor' role")

    db_document = DoctorDocument(
        doctor_id=document.doctor_id,
        document_type=document.document_type,
        file_url=document.file_url,
        verified=False
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@doctor_router.get("/documents", response_model=list[DoctorDocumentResponse])
async def list_doctor_documents(
    skip: int = 0,
    limit: int = 10,
    doctor_id: UUID = None,
    verified: bool = None,
    db: Session = Depends(get_db),
):
    """List doctor documents with optional filters"""
    query = db.query(DoctorDocument)
    if doctor_id:
        query = query.filter(DoctorDocument.doctor_id == doctor_id)
    if verified is not None:
        query = query.filter(DoctorDocument.verified == verified)
    documents = query.offset(skip).limit(limit).all()
    return documents


@doctor_router.get("/documents/{document_id}", response_model=DoctorDocumentResponse)
async def get_doctor_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@doctor_router.get("/{doctor_id}/documents", response_model=list[DoctorDocumentResponse])
async def get_documents_for_doctor(
    doctor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    documents = db.query(DoctorDocument).filter(DoctorDocument.doctor_id == doctor_id).offset(skip).limit(limit).all()
    return documents


@doctor_router.put("/documents/{document_id}", response_model=DoctorDocumentResponse)
async def update_doctor_document(
    document_id: UUID,
    document_update: DoctorDocumentUpdate,
    db: Session = Depends(get_db),
):
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if document_update.document_type is not None:
        document.document_type = document_update.document_type
    if document_update.file_url is not None:
        document.file_url = document_update.file_url
    db.commit()
    db.refresh(document)
    return document


@doctor_router.post("/documents/{document_id}/verify", response_model=DoctorDocumentResponse)
async def verify_doctor_document(
    document_id: UUID,
    verification: DoctorDocumentVerify,
    db: Session = Depends(get_db),
):
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    document.verified = verification.verified
    db.commit()
    db.refresh(document)
    return document


@doctor_router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    db.delete(document)
    db.commit()


# ============================================================

# ============================================================
# Doctor Categories Router
# ============================================================

doctor_categories_router = APIRouter(prefix="/api/doctor-categories", tags=["doctor-categories"])


@doctor_categories_router.post("/bulk", response_model=list[DoctorCategoryResponse], status_code=status.HTTP_201_CREATED)
async def bulk_create_doctor_categories(
    categories: list[DoctorCategoryCreate],
    db: Session = Depends(get_db),
):
    """Create or update multiple doctor categories in bulk"""
    created = []
    for cat in categories:
        try:
            # Try find by id first if provided
            existing = None
            if getattr(cat, 'id', None):
                existing = db.query(DoctorCategory).filter(DoctorCategory.id == cat.id).first()
            if not existing:
                existing = db.query(DoctorCategory).filter(DoctorCategory.label == cat.label).first()

            if existing:
                existing.icon = cat.icon
                existing.color = cat.color
                db.commit()
                db.refresh(existing)
                created.append(existing)
            else:
                new_cat = DoctorCategory(
                    id=cat.id if getattr(cat, 'id', None) else None,
                    label=cat.label,
                    icon=cat.icon,
                    color=cat.color
                )
                db.add(new_cat)
                db.commit()
                db.refresh(new_cat)
                created.append(new_cat)
        except Exception:
            db.rollback()
            continue

    return created


@doctor_categories_router.get("", response_model=list[DoctorCategoryResponse])
async def list_doctor_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(DoctorCategory).offset(skip).limit(limit).all()
    return query

# ============================================================



drugs_router = APIRouter(prefix="/api/drugs", tags=["drugs"])


@drugs_router.post("", response_model=DrugResponse, status_code=status.HTTP_201_CREATED)
async def create_drug(
    drug: DrugCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new drug/medicine record
    
    - **name**: Brand name of the drug
    - **generic_name**: Generic/chemical name
    - **manufacturer**: Drug manufacturer
    - **price**: Price per unit (must be positive)
    - **stock_quantity**: Available stock (non-negative)
    - **expiry_date**: Expiry date (YYYY-MM-DD format)
    """
    # Parse expiry_date string to date object
    try:
        from datetime import datetime as dt
        expiry_date = dt.strptime(drug.expiry_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid expiry_date format. Expected YYYY-MM-DD"
        )
    
    # Create drug record
    db_drug = Drug(
        name=drug.name,
        generic_name=drug.generic_name,
        manufacturer=drug.manufacturer,
        price=drug.price,
        stock_quantity=drug.stock_quantity,
        expiry_date=expiry_date
    )
    db.add(db_drug)
    db.commit()
    db.refresh(db_drug)
    return db_drug


@drugs_router.get("", response_model=list[DrugResponse])
async def get_all_drugs(
    skip: int = 0,
    limit: int = 10,
    name: str = None,
    manufacturer: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all drugs with optional filtering and pagination
    
    - **skip**: Number of drugs to skip (default: 0)
    - **limit**: Maximum number of drugs to return (default: 10)
    - **name**: Filter by drug name (partial match, optional)
    - **manufacturer**: Filter by manufacturer (optional)
    """
    query = db.query(Drug)
    
    if name:
        query = query.filter(Drug.name.ilike(f"%{name}%"))
    
    if manufacturer:
        query = query.filter(Drug.manufacturer.ilike(f"%{manufacturer}%"))
    
    drugs = query.offset(skip).limit(limit).all()
    return drugs


@drugs_router.get("/{drug_id}", response_model=DrugResponse)
async def get_drug(
    drug_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific drug by ID"""
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    return drug


@drugs_router.put("/{drug_id}", response_model=DrugResponse)
async def update_drug(
    drug_id: UUID,
    drug_update: DrugUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a drug record
    
    - **name**: Update drug name (optional)
    - **generic_name**: Update generic name (optional)
    - **manufacturer**: Update manufacturer (optional)
    - **price**: Update price (optional)
    - **stock_quantity**: Update stock quantity (optional)
    - **expiry_date**: Update expiry date (optional)
    """
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    # Update fields
    if drug_update.name is not None:
        drug.name = drug_update.name
    if drug_update.generic_name is not None:
        drug.generic_name = drug_update.generic_name
    if drug_update.manufacturer is not None:
        drug.manufacturer = drug_update.manufacturer
    if drug_update.price is not None:
        drug.price = drug_update.price
    if drug_update.stock_quantity is not None:
        drug.stock_quantity = drug_update.stock_quantity
    if drug_update.expiry_date is not None:
        try:
            from datetime import datetime as dt
            expiry_date = dt.strptime(drug_update.expiry_date, "%Y-%m-%d").date()
            drug.expiry_date = expiry_date
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid expiry_date format. Expected YYYY-MM-DD"
            )
    
    db.commit()
    db.refresh(drug)
    return drug


@drugs_router.delete("/{drug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drug(
    drug_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a drug record by ID"""
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    db.delete(drug)
    db.commit()


# ============================================================
# Stock Transactions Router (new)
# ============================================================

stock_transactions_router = APIRouter(prefix="/api/stock-transactions", tags=["stock-transactions"])


@stock_transactions_router.post("", response_model=StockTransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_stock_transaction(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new stock transaction
    
    - **drug_id**: UUID of the drug
    - **quantity**: Quantity added/removed (must be positive)
    - **type**: Transaction type ('IN' for stock in, 'OUT' for stock out)
    - **source**: Source of transaction (e.g., vendor, prescription, adjustment)
    """
    # Check if drug exists
    drug = db.query(Drug).filter(Drug.id == transaction.drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    # Validate transaction type
    valid_types = ['IN', 'OUT']
    if transaction.type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type must be one of: {', '.join(valid_types)}"
        )
    
    # Create transaction
    db_transaction = StockTransaction(
        drug_id=transaction.drug_id,
        quantity=transaction.quantity,
        type=transaction.type,
        source=transaction.source
    )
    db.add(db_transaction)
    
    # Update drug stock_quantity based on transaction type
    if transaction.type == 'IN':
        drug.stock_quantity += transaction.quantity
    else:  # OUT
        if drug.stock_quantity < transaction.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {drug.stock_quantity}, Requested: {transaction.quantity}"
            )
        drug.stock_quantity -= transaction.quantity
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@stock_transactions_router.get("", response_model=list[StockTransactionResponse])
async def get_all_transactions(
    skip: int = 0,
    limit: int = 10,
    drug_id: UUID = None,
    type: str = None,
    source: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all stock transactions with optional filtering
    
    - **skip**: Number of transactions to skip (default: 0)
    - **limit**: Maximum number of transactions to return (default: 10)
    - **drug_id**: Filter by specific drug (optional)
    - **type**: Filter by transaction type ('IN' or 'OUT', optional)
    - **source**: Filter by source (optional)
    """
    query = db.query(StockTransaction)
    
    if drug_id:
        query = query.filter(StockTransaction.drug_id == drug_id)
    
    if type:
        if type not in ['IN', 'OUT']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type must be 'IN' or 'OUT'"
            )
        query = query.filter(StockTransaction.type == type)
    
    if source:
        query = query.filter(StockTransaction.source.ilike(f"%{source}%"))
    
    transactions = query.order_by(StockTransaction.created_at.desc()).offset(skip).limit(limit).all()
    return transactions


@stock_transactions_router.get("/{transaction_id}", response_model=StockTransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific stock transaction by ID"""
    transaction = db.query(StockTransaction).filter(StockTransaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock transaction not found"
        )
    return transaction


@stock_transactions_router.get("/drug/{drug_id}", response_model=list[StockTransactionResponse])
async def get_drug_transactions(
    drug_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get all stock transactions for a specific drug"""
    # Check if drug exists
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    transactions = db.query(StockTransaction).filter(
        StockTransaction.drug_id == drug_id
    ).order_by(StockTransaction.created_at.desc()).offset(skip).limit(limit).all()
    
    return transactions


@stock_transactions_router.put("/{transaction_id}", response_model=StockTransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_update: StockTransactionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a stock transaction
    
    - **quantity**: Update quantity (optional)
    - **source**: Update source (optional)
    
    Note: Cannot change drug_id or type after creation
    """
    transaction = db.query(StockTransaction).filter(StockTransaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock transaction not found"
        )
    
    # If quantity is being updated, adjust drug stock accordingly
    if transaction_update.quantity is not None and transaction_update.quantity != transaction.quantity:
        drug = db.query(Drug).filter(Drug.id == transaction.drug_id).first()
        quantity_diff = transaction_update.quantity - transaction.quantity
        
        if transaction.type == 'IN':
            drug.stock_quantity += quantity_diff
        else:  # OUT
            if drug.stock_quantity < quantity_diff:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for the adjustment. Available: {drug.stock_quantity}, Requested change: {quantity_diff}"
                )
            drug.stock_quantity -= quantity_diff
        
        transaction.quantity = transaction_update.quantity
    
    # Update source if provided
    if transaction_update.source is not None:
        transaction.source = transaction_update.source
    
    db.commit()
    db.refresh(transaction)
    return transaction


@stock_transactions_router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a stock transaction by ID"""
    transaction = db.query(StockTransaction).filter(StockTransaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock transaction not found"
        )
    
    # Reverse the stock adjustment when deleting transaction
    drug = db.query(Drug).filter(Drug.id == transaction.drug_id).first()
    if transaction.type == 'IN':
        drug.stock_quantity -= transaction.quantity
    else:  # OUT
        drug.stock_quantity += transaction.quantity
    
    db.delete(transaction)
    db.commit()


# ============================================================
# Vendor Router (new)
# ============================================================

vendor_router = APIRouter(prefix="/api/vendors", tags=["vendors"])


@vendor_router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new vendor/supplier
    
    - **name**: Vendor/supplier name
    - **contact_number**: Vendor contact number
    - **email**: Vendor email address
    - **address**: Vendor address
    """
    # Check if vendor with same email already exists
    existing_vendor = db.query(Vendor).filter(Vendor.email == vendor.email).first()
    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor with this email already exists"
        )
    
    # Create vendor
    db_vendor = Vendor(
        name=vendor.name,
        contact_number=vendor.contact_number,
        email=vendor.email,
        address=vendor.address,
        is_active=True
    )
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


@vendor_router.get("", response_model=list[VendorResponse])
async def get_all_vendors(
    skip: int = 0,
    limit: int = 10,
    is_active: bool = None,
    db: Session = Depends(get_db),
):
    """
    Get all vendors with optional filtering
    
    - **skip**: Number of vendors to skip (default: 0)
    - **limit**: Maximum number of vendors to return (default: 10)
    - **is_active**: Filter by active status (optional)
    """
    query = db.query(Vendor)
    
    if is_active is not None:
        query = query.filter(Vendor.is_active == is_active)
    
    vendors = query.offset(skip).limit(limit).all()
    return vendors


@vendor_router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(
    vendor_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific vendor by ID"""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    return vendor


@vendor_router.put("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    vendor_id: UUID,
    vendor_update: VendorUpdate,
    db: Session = Depends(get_db),
):
    """
    Update vendor information
    
    - **name**: Vendor name (optional)
    - **contact_number**: Contact number (optional)
    - **email**: Email address (optional)
    - **address**: Address (optional)
    - **is_active**: Active status (optional)
    """
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Check if new email already exists (if email is being updated)
    if vendor_update.email and vendor_update.email != vendor.email:
        existing = db.query(Vendor).filter(Vendor.email == vendor_update.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vendor with this email already exists"
            )
    
    # Update fields
    if vendor_update.name is not None:
        vendor.name = vendor_update.name
    if vendor_update.contact_number is not None:
        vendor.contact_number = vendor_update.contact_number
    if vendor_update.email is not None:
        vendor.email = vendor_update.email
    if vendor_update.address is not None:
        vendor.address = vendor_update.address
    if vendor_update.is_active is not None:
        vendor.is_active = vendor_update.is_active
    
    db.commit()
    db.refresh(vendor)
    return vendor


@vendor_router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(
    vendor_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a vendor by ID"""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    db.delete(vendor)
    db.commit()


# ============================================================
# Vendor Orders Router (new)
# ============================================================

vendor_orders_router = APIRouter(prefix="/api/vendor-orders", tags=["vendor-orders"])


@vendor_orders_router.post("", response_model=VendorOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor_order(
    order: VendorOrderCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new vendor order
    
    - **vendor_id**: UUID of the vendor
    - **total_amount**: Total order amount (must be positive)
    - **status**: Order status (default: pending)
    """
    # Check if vendor exists
    vendor = db.query(Vendor).filter(Vendor.id == order.vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Validate status if provided
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    if order.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    # Create order
    db_order = VendorOrder(
        vendor_id=order.vendor_id,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@vendor_orders_router.get("", response_model=list[VendorOrderResponse])
async def get_all_vendor_orders(
    skip: int = 0,
    limit: int = 10,
    vendor_id: UUID = None,
    status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all vendor orders with optional filtering
    
    - **skip**: Number of orders to skip (default: 0)
    - **limit**: Maximum number of orders to return (default: 10)
    - **vendor_id**: Filter by vendor ID (optional)
    - **status**: Filter by order status (optional)
    """
    query = db.query(VendorOrder)
    
    if vendor_id:
        query = query.filter(VendorOrder.vendor_id == vendor_id)
    
    if status:
        query = query.filter(VendorOrder.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@vendor_orders_router.get("/{order_id}", response_model=VendorOrderDetailResponse)
async def get_vendor_order(
    order_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific vendor order by ID with vendor details"""
    order = db.query(VendorOrder).filter(VendorOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor order not found"
        )
    return order


@vendor_orders_router.get("/vendor/{vendor_id}", response_model=list[VendorOrderResponse])
async def get_vendor_orders_by_vendor(
    vendor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all orders for a specific vendor
    
    - **vendor_id**: UUID of the vendor
    - **skip**: Number of orders to skip (default: 0)
    - **limit**: Maximum number of orders to return (default: 10)
    - **status**: Filter by order status (optional)
    """
    # Check if vendor exists
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    query = db.query(VendorOrder).filter(VendorOrder.vendor_id == vendor_id)
    
    if status:
        query = query.filter(VendorOrder.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@vendor_orders_router.put("/{order_id}", response_model=VendorOrderResponse)
async def update_vendor_order(
    order_id: UUID,
    order_update: VendorOrderUpdate,
    db: Session = Depends(get_db),
):
    """
    Update vendor order information
    
    - **total_amount**: Total order amount (optional, must be positive)
    - **status**: Order status (optional)
    """
    order = db.query(VendorOrder).filter(VendorOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor order not found"
        )
    
    # Validate status if provided
    if order_update.status:
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if order_update.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )
    
    # Update fields
    if order_update.total_amount is not None:
        order.total_amount = order_update.total_amount
    if order_update.status is not None:
        order.status = order_update.status
    
    db.commit()
    db.refresh(order)
    return order


@vendor_orders_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor_order(
    order_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a vendor order by ID"""
    order = db.query(VendorOrder).filter(VendorOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor order not found"
        )
    
    db.delete(order)
    db.commit()


# ============================================================
# Appointments Router (new)
# ============================================================

appointment_router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@appointment_router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new appointment
    
    - **patient_id**: UUID of the patient
    - **doctor_id**: UUID of the doctor
    - **appointment_date**: Appointment date (YYYY-MM-DD)
    - **time_slot**: Time slot (e.g., 09:00-09:30)
    - **status**: Appointment status (default: scheduled)
    - **notes**: Additional notes (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Validate status
    valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled']
    if appointment.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    # Create appointment
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        time_slot=appointment.time_slot,
        status=appointment.status,
        notes=appointment.notes
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@appointment_router.get("", response_model=list[AppointmentResponse])
async def get_all_appointments(
    skip: int = 0,
    limit: int = 10,
    patient_id: UUID = None,
    doctor_id: UUID = None,
    status: str = None,
    appointment_date: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments with optional filtering
    
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **patient_id**: Filter by patient ID (optional)
    - **doctor_id**: Filter by doctor ID (optional)
    - **status**: Filter by status (optional)
    - **appointment_date**: Filter by date (YYYY-MM-DD) (optional)
    """
    query = db.query(Appointment)
    
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.get("/{appointment_id}", response_model=AppointmentDetailResponse)
async def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific appointment by ID with patient and doctor details"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return appointment


@appointment_router.get("/patient/{patient_id}", response_model=list[AppointmentResponse])
async def get_patient_appointments(
    patient_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments for a specific patient
    
    - **patient_id**: UUID of the patient
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **status**: Filter by status (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    query = db.query(Appointment).filter(Appointment.patient_id == patient_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.get("/doctor/{doctor_id}", response_model=list[AppointmentResponse])
async def get_doctor_appointments(
    doctor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    appointment_date: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments for a specific doctor
    
    - **doctor_id**: UUID of the doctor
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **status**: Filter by status (optional)
    - **appointment_date**: Filter by date (YYYY-MM-DD) (optional)
    """
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: UUID,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update appointment information
    
    - **appointment_date**: New appointment date (optional)
    - **time_slot**: New time slot (optional)
    - **status**: New status (optional)
    - **notes**: Additional notes (optional)
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Validate status if provided
    if appointment_update.status:
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled']
        if appointment_update.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )
    
    # Update fields
    if appointment_update.appointment_date is not None:
        appointment.appointment_date = appointment_update.appointment_date
    if appointment_update.time_slot is not None:
        appointment.time_slot = appointment_update.time_slot
    if appointment_update.status is not None:
        appointment.status = appointment_update.status
    if appointment_update.notes is not None:
        appointment.notes = appointment_update.notes
    
    db.commit()
    db.refresh(appointment)
    return appointment


@appointment_router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an appointment by ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.delete(appointment)
    db.commit()


@appointment_router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Cancel an appointment (shorthand endpoint)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    appointment.status = 'cancelled'
    db.commit()
    db.refresh(appointment)
    return appointment


@appointment_router.post("/{appointment_id}/complete", response_model=AppointmentResponse)
async def complete_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Mark an appointment as completed (shorthand endpoint)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    appointment.status = 'completed'
    db.commit()
    db.refresh(appointment)
    return appointment


    db.delete(order)
    db.commit()


# ============================================================
# Appointments Router (new)
# ============================================================

appointment_router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@appointment_router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new appointment
    
    - **patient_id**: UUID of the patient
    - **doctor_id**: UUID of the doctor
    - **appointment_date**: Appointment date (YYYY-MM-DD)
    - **time_slot**: Time slot (e.g., 09:00-09:30)
    - **status**: Appointment status (default: scheduled)
    - **notes**: Additional notes (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Validate status
    valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled']
    if appointment.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    # Create appointment
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        time_slot=appointment.time_slot,
        status=appointment.status,
        notes=appointment.notes
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@appointment_router.get("", response_model=list[AppointmentResponse])
async def get_all_appointments(
    skip: int = 0,
    limit: int = 10,
    patient_id: UUID = None,
    doctor_id: UUID = None,
    status: str = None,
    appointment_date: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments with optional filtering
    
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **patient_id**: Filter by patient ID (optional)
    - **doctor_id**: Filter by doctor ID (optional)
    - **status**: Filter by status (optional)
    - **appointment_date**: Filter by date (YYYY-MM-DD) (optional)
    """
    query = db.query(Appointment)
    
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.get("/{appointment_id}", response_model=AppointmentDetailResponse)
async def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific appointment by ID with patient and doctor details"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return appointment


@appointment_router.get("/patient/{patient_id}", response_model=list[AppointmentResponse])
async def get_patient_appointments(
    patient_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments for a specific patient
    
    - **patient_id**: UUID of the patient
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **status**: Filter by status (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    query = db.query(Appointment).filter(Appointment.patient_id == patient_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.get("/doctor/{doctor_id}", response_model=list[AppointmentResponse])
async def get_doctor_appointments(
    doctor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    appointment_date: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments for a specific doctor
    
    - **doctor_id**: UUID of the doctor
    - **skip**: Number of appointments to skip (default: 0)
    - **limit**: Maximum number of appointments to return (default: 10)
    - **status**: Filter by status (optional)
    - **appointment_date**: Filter by date (YYYY-MM-DD) (optional)
    """
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@appointment_router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: UUID,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update appointment information
    
    - **appointment_date**: New appointment date (optional)
    - **time_slot**: New time slot (optional)
    - **status**: New status (optional)
    - **notes**: Additional notes (optional)
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Validate status if provided
    if appointment_update.status:
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled']
        if appointment_update.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )
    
    # Update fields
    if appointment_update.appointment_date is not None:
        appointment.appointment_date = appointment_update.appointment_date
    if appointment_update.time_slot is not None:
        appointment.time_slot = appointment_update.time_slot
    if appointment_update.status is not None:
        appointment.status = appointment_update.status
    if appointment_update.notes is not None:
        appointment.notes = appointment_update.notes
    
    db.commit()
    db.refresh(appointment)
    return appointment


@appointment_router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an appointment by ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.delete(appointment)
    db.commit()


@appointment_router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Cancel an appointment (shorthand endpoint)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    appointment.status = 'cancelled'
    db.commit()
    db.refresh(appointment)
    return appointment


@appointment_router.post("/{appointment_id}/complete", response_model=AppointmentResponse)
async def complete_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Mark an appointment as completed (shorthand endpoint)"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    appointment.status = 'completed'
    db.commit()
    db.refresh(appointment)
    return appointment


# ============================================================
# Prescriptions Router (new)
# ============================================================

prescription_router = APIRouter(prefix="/api/prescriptions", tags=["prescriptions"])


@prescription_router.post("", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new prescription
    
    - **appointment_id**: UUID of the appointment
    - **doctor_id**: UUID of the doctor
    - **patient_id**: UUID of the patient
    - **notes**: Additional prescription notes (optional)
    - **items**: List of prescription items (optional)
    """
    # Check if appointment exists
    appointment = db.query(Appointment).filter(Appointment.id == prescription.appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == prescription.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Check if patient exists
    patient = db.query(User).filter(User.id == prescription.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Create prescription
    db_prescription = Prescription(
        appointment_id=prescription.appointment_id,
        doctor_id=prescription.doctor_id,
        patient_id=prescription.patient_id,
        notes=prescription.notes
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    
    # Add prescription items if provided
    if prescription.items:
        for item in prescription.items:
            # Check if drug exists
            drug = db.query(Drug).filter(Drug.id == item.drug_id).first()
            if not drug:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Drug not found: {item.drug_id}"
                )
            
            db_item = PrescriptionItem(
                prescription_id=db_prescription.id,
                drug_id=item.drug_id,
                dosage=item.dosage,
                duration=item.duration,
                instructions=item.instructions
            )
            db.add(db_item)
        db.commit()
    
    return db_prescription


@prescription_router.get("", response_model=list[PrescriptionResponse])
async def get_all_prescriptions(
    skip: int = 0,
    limit: int = 10,
    patient_id: UUID = None,
    doctor_id: UUID = None,
    appointment_id: UUID = None,
    db: Session = Depends(get_db),
):
    """
    Get all prescriptions with optional filtering
    
    - **skip**: Number of prescriptions to skip (default: 0)
    - **limit**: Maximum number of prescriptions to return (default: 10)
    - **patient_id**: Filter by patient ID (optional)
    - **doctor_id**: Filter by doctor ID (optional)
    - **appointment_id**: Filter by appointment ID (optional)
    """
    query = db.query(Prescription)
    
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    
    if doctor_id:
        query = query.filter(Prescription.doctor_id == doctor_id)
    
    if appointment_id:
        query = query.filter(Prescription.appointment_id == appointment_id)
    
    prescriptions = query.order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
    return prescriptions


@prescription_router.get("/{prescription_id}", response_model=PrescriptionDetailResponse)
async def get_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific prescription by ID with all items"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Fetch prescription items
    items = db.query(PrescriptionItem).filter(PrescriptionItem.prescription_id == prescription_id).all()
    prescription.items = items
    
    return prescription


@prescription_router.get("/patient/{patient_id}", response_model=list[PrescriptionResponse])
async def get_patient_prescriptions(
    patient_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get all prescriptions for a specific patient
    
    - **patient_id**: UUID of the patient
    - **skip**: Number of prescriptions to skip (default: 0)
    - **limit**: Maximum number of prescriptions to return (default: 10)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    prescriptions = db.query(Prescription).filter(
        Prescription.patient_id == patient_id
    ).order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
    
    return prescriptions


@prescription_router.get("/doctor/{doctor_id}", response_model=list[PrescriptionResponse])
async def get_doctor_prescriptions(
    doctor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get all prescriptions issued by a specific doctor
    
    - **doctor_id**: UUID of the doctor
    - **skip**: Number of prescriptions to skip (default: 0)
    - **limit**: Maximum number of prescriptions to return (default: 10)
    """
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    prescriptions = db.query(Prescription).filter(
        Prescription.doctor_id == doctor_id
    ).order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
    
    return prescriptions


@prescription_router.get("/appointment/{appointment_id}", response_model=list[PrescriptionResponse])
async def get_appointment_prescriptions(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all prescriptions for a specific appointment"""
    # Check if appointment exists
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    prescriptions = db.query(Prescription).filter(
        Prescription.appointment_id == appointment_id
    ).all()
    
    return prescriptions


@prescription_router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    prescription_id: UUID,
    prescription_update: PrescriptionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update prescription information
    
    - **notes**: Update prescription notes (optional)
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Update fields
    if prescription_update.notes is not None:
        prescription.notes = prescription_update.notes
    
    db.commit()
    db.refresh(prescription)
    return prescription


@prescription_router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a prescription and its items by ID"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Delete associated prescription items
    db.query(PrescriptionItem).filter(PrescriptionItem.prescription_id == prescription_id).delete()
    
    # Delete prescription
    db.delete(prescription)
    db.commit()


# ============================================================
# Prescription Items Router (new)
# ============================================================

prescription_items_router = APIRouter(prefix="/api/prescription-items", tags=["prescription-items"])


@prescription_items_router.post("", response_model=PrescriptionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_prescription_item(
    prescription_id: UUID = None,
    item: PrescriptionItemCreate = None,
    db: Session = Depends(get_db),
):
    """
    Add a drug item to a prescription
    
    Query parameter:
    - **prescription_id**: UUID of the prescription
    
    Body:
    - **drug_id**: UUID of the drug
    - **dosage**: Drug dosage (e.g., 500mg)
    - **duration**: Duration (e.g., 7 days)
    - **instructions**: Usage instructions (optional)
    """
    if not prescription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="prescription_id query parameter is required"
        )
    
    # Check if prescription exists
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Check if drug exists
    drug = db.query(Drug).filter(Drug.id == item.drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    # Create prescription item
    db_item = PrescriptionItem(
        prescription_id=prescription_id,
        drug_id=item.drug_id,
        dosage=item.dosage,
        duration=item.duration,
        instructions=item.instructions
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@prescription_items_router.get("/prescription/{prescription_id}", response_model=list[PrescriptionItemResponse])
async def get_prescription_items(
    prescription_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all items in a specific prescription"""
    # Check if prescription exists
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    items = db.query(PrescriptionItem).filter(PrescriptionItem.prescription_id == prescription_id).all()
    return items


@prescription_items_router.get("/{item_id}", response_model=PrescriptionItemResponse)
async def get_prescription_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific prescription item by ID"""
    item = db.query(PrescriptionItem).filter(PrescriptionItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found"
        )
    return item


@prescription_items_router.get("/drug/{drug_id}", response_model=list[PrescriptionItemResponse])
async def get_items_by_drug(
    drug_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all prescription items for a specific drug"""
    # Check if drug exists
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )
    
    items = db.query(PrescriptionItem).filter(PrescriptionItem.drug_id == drug_id).all()
    return items


@prescription_items_router.put("/{item_id}", response_model=PrescriptionItemResponse)
async def update_prescription_item(
    item_id: UUID,
    item_update: PrescriptionItemCreate,
    db: Session = Depends(get_db),
):
    """
    Update a prescription item
    
    - **drug_id**: Update drug (optional)
    - **dosage**: Update dosage (optional)
    - **duration**: Update duration (optional)
    - **instructions**: Update instructions (optional)
    """
    item = db.query(PrescriptionItem).filter(PrescriptionItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found"
        )
    
    # Check if drug exists (if being changed)
    if item_update.drug_id != item.drug_id:
        drug = db.query(Drug).filter(Drug.id == item_update.drug_id).first()
        if not drug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drug not found"
            )
        item.drug_id = item_update.drug_id
    
    # Update fields
    item.dosage = item_update.dosage
    item.duration = item_update.duration
    item.instructions = item_update.instructions
    
    db.commit()
    db.refresh(item)
    return item


@prescription_items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a prescription item by ID"""
    item = db.query(PrescriptionItem).filter(PrescriptionItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found"
        )
    
    db.delete(item)
    db.commit()


# ============================================================
# Medical Records Router (new)
# ============================================================

medical_records_router = APIRouter(prefix="/api/medical-records", tags=["medical-records"])


@medical_records_router.post("", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new medical record
    
    - **patient_id**: UUID of the patient
    - **file_url**: URL to the medical record file
    - **record_type**: Type of record (lab_report, x_ray, prescription, discharge_summary, etc.)
    - **description**: Description or notes about the record (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == record.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Create medical record
    db_record = MedicalRecord(
        patient_id=record.patient_id,
        file_url=record.file_url,
        record_type=record.record_type,
        description=record.description
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@medical_records_router.get("", response_model=list[MedicalRecordResponse])
async def get_all_medical_records(
    skip: int = 0,
    limit: int = 10,
    patient_id: UUID = None,
    record_type: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all medical records with optional filtering
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **patient_id**: Filter by patient ID (optional)
    - **record_type**: Filter by record type (optional)
    """
    query = db.query(MedicalRecord)
    
    if patient_id:
        query = query.filter(MedicalRecord.patient_id == patient_id)
    
    if record_type:
        query = query.filter(MedicalRecord.record_type == record_type)
    
    records = query.order_by(MedicalRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records


@medical_records_router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(
    record_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific medical record by ID"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    return record


@medical_records_router.get("/patient/{patient_id}", response_model=list[MedicalRecordResponse])
async def get_patient_medical_records(
    patient_id: UUID,
    skip: int = 0,
    limit: int = 10,
    record_type: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all medical records for a specific patient
    
    - **patient_id**: UUID of the patient
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **record_type**: Filter by record type (optional)
    """
    # Check if patient exists
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    query = db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id)
    
    if record_type:
        query = query.filter(MedicalRecord.record_type == record_type)
    
    records = query.order_by(MedicalRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records


@medical_records_router.get("/type/{record_type}", response_model=list[MedicalRecordResponse])
async def get_records_by_type(
    record_type: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get all records of a specific type
    
    - **record_type**: Type of record (lab_report, x_ray, prescription, etc.)
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    records = db.query(MedicalRecord).filter(
        MedicalRecord.record_type == record_type
    ).order_by(MedicalRecord.created_at.desc()).offset(skip).limit(limit).all()
    
    return records


@medical_records_router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_medical_record(
    record_id: UUID,
    record_update: MedicalRecordUpdate,
    db: Session = Depends(get_db),
):
    """
    Update medical record information
    
    - **file_url**: Update file URL (optional)
    - **record_type**: Update record type (optional)
    - **description**: Update description (optional)
    """
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    # Update fields
    if record_update.file_url is not None:
        record.file_url = record_update.file_url
    if record_update.record_type is not None:
        record.record_type = record_update.record_type
    if record_update.description is not None:
        record.description = record_update.description
    
    db.commit()
    db.refresh(record)
    return record


@medical_records_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(
    record_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a medical record by ID"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    db.delete(record)
    db.commit()


# ==================== PAYMENTS ROUTER ====================

payments_router = APIRouter(prefix="/api/payments", tags=["payments"])


@payments_router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate = Body(...),
    db: Session = Depends(get_db),
):
    """
    Create a new payment transaction
    
    - **user_id**: UUID of the user making the payment
    - **amount**: Payment amount (with 2 decimal places)
    - **payment_method**: Payment method (credit_card, debit_card, upi, bank_transfer, etc.)
    - **transaction_id**: Unique transaction identifier (must be unique)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == payment.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if transaction_id already exists
    existing = db.query(Payment).filter(Payment.transaction_id == payment.transaction_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction ID already exists"
        )
    
    # Create payment
    db_payment = Payment(
        user_id=payment.user_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        payment_status='pending',
        transaction_id=payment.transaction_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@payments_router.get("", response_model=list[PaymentResponse])
async def get_all_payments(
    skip: int = 0,
    limit: int = 10,
    user_id: UUID = None,
    payment_status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all payments with optional filtering
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **user_id**: Filter by user ID (optional)
    - **payment_status**: Filter by payment status (optional)
    """
    query = db.query(Payment)
    
    if user_id:
        query = query.filter(Payment.user_id == user_id)
    
    if payment_status:
        query = query.filter(Payment.payment_status == payment_status)
    
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return payments


@payments_router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single payment by ID"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment


@payments_router.get("/user/{user_id}", response_model=list[PaymentResponse])
async def get_user_payments(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    payment_status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all payments for a specific user
    
    - **user_id**: User identifier
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **payment_status**: Filter by status (optional)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    query = db.query(Payment).filter(Payment.user_id == user_id)
    
    if payment_status:
        query = query.filter(Payment.payment_status == payment_status)
    
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return payments


@payments_router.get("/status/{status}", response_model=list[PaymentResponse])
async def get_payments_by_status(
    status: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get all payments by payment status
    
    - **status**: Payment status (pending, completed, failed, refunded)
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    payments = db.query(Payment).filter(
        Payment.payment_status == status
    ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return payments


@payments_router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: UUID,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a payment record
    
    Update payment status, amount, or payment method as needed
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Update fields if provided
    if payment_update.payment_status is not None:
        payment.payment_status = payment_update.payment_status
    
    if payment_update.amount is not None:
        payment.amount = payment_update.amount
    
    if payment_update.payment_method is not None:
        payment.payment_method = payment_update.payment_method
    
    payment.updated_at = datetime.utcnow()
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@payments_router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a payment record by ID"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    db.delete(payment)
    db.commit()


# ==================== INVOICES ROUTER ====================

invoices_router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@invoices_router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new invoice
    
    - **user_id**: UUID of the user
    - **total_amount**: Total invoice amount
    """
    # Check if user exists
    user = db.query(User).filter(User.id == invoice.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create invoice
    db_invoice = Invoice(
        user_id=invoice.user_id,
        total_amount=invoice.total_amount,
        status='draft'
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@invoices_router.get("", response_model=list[InvoiceResponse])
async def get_all_invoices(
    skip: int = 0,
    limit: int = 10,
    user_id: UUID = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all invoices with optional filtering
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **user_id**: Filter by user ID (optional)
    - **status_filter**: Filter by status (optional)
    """
    query = db.query(Invoice)
    
    if user_id:
        query = query.filter(Invoice.user_id == user_id)
    
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    return invoices


@invoices_router.get("/{invoice_id}", response_model=InvoiceDetailResponse)
async def get_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single invoice with all its items"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Get invoice items
    items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()
    invoice.items = items
    return invoice


@invoices_router.get("/user/{user_id}", response_model=list[InvoiceResponse])
async def get_user_invoices(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status_filter: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all invoices for a specific user
    
    - **user_id**: User identifier
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **status_filter**: Filter by status (optional)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    query = db.query(Invoice).filter(Invoice.user_id == user_id)
    
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    return invoices


@invoices_router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: UUID,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an invoice
    
    Update status or total amount as needed
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Update fields if provided
    if invoice_update.status is not None:
        invoice.status = invoice_update.status
    
    if invoice_update.total_amount is not None:
        invoice.total_amount = invoice_update.total_amount
    
    invoice.updated_at = datetime.utcnow()
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@invoices_router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an invoice and all its items"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Delete associated invoice items (cascade)
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
    
    # Delete invoice
    db.delete(invoice)
    db.commit()


# ==================== INVOICE ITEMS ROUTER ====================

invoice_items_router = APIRouter(prefix="/api/invoice-items", tags=["invoice-items"])


@invoice_items_router.post("", response_model=InvoiceItemResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice_item(
    item: InvoiceItemCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new invoice item
    
    - **invoice_id**: UUID of the invoice (query param)
    - **item_type**: Type of item (drug, consultation, service, etc.)
    - **item_id**: UUID of the specific item
    - **quantity**: Quantity of items
    - **price**: Unit price of item
    """
    # Get invoice_id from query or body
    invoice_id = None
    if hasattr(item, 'invoice_id'):
        invoice_id = item.invoice_id
    
    if not invoice_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invoice_id is required"
        )
    
    # Check if invoice exists
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Create invoice item
    db_item = InvoiceItem(
        invoice_id=invoice_id,
        item_type=item.item_type,
        item_id=item.item_id,
        quantity=item.quantity,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@invoice_items_router.get("", response_model=list[InvoiceItemResponse])
async def get_all_invoice_items(
    skip: int = 0,
    limit: int = 10,
    invoice_id: UUID = None,
    item_type: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all invoice items with optional filtering
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    - **invoice_id**: Filter by invoice ID (optional)
    - **item_type**: Filter by item type (optional)
    """
    query = db.query(InvoiceItem)
    
    if invoice_id:
        query = query.filter(InvoiceItem.invoice_id == invoice_id)
    
    if item_type:
        query = query.filter(InvoiceItem.item_type == item_type)
    
    items = query.order_by(InvoiceItem.created_at.desc()).offset(skip).limit(limit).all()
    return items


@invoice_items_router.get("/{item_id}", response_model=InvoiceItemResponse)
async def get_invoice_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single invoice item"""
    item = db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )
    return item


@invoice_items_router.get("/invoice/{invoice_id}", response_model=list[InvoiceItemResponse])
async def get_invoice_items(
    invoice_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get all items for a specific invoice
    
    - **invoice_id**: Invoice identifier
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    # Check if invoice exists
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    items = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice_id
    ).order_by(InvoiceItem.created_at.desc()).offset(skip).limit(limit).all()
    return items


@invoice_items_router.put("/{item_id}", response_model=InvoiceItemResponse)
async def update_invoice_item(
    item_id: UUID,
    item_update: InvoiceItemUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an invoice item
    
    Update quantity, price, or item details as needed
    """
    item = db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )
    
    # Update fields if provided
    if item_update.item_type is not None:
        item.item_type = item_update.item_type
    
    if item_update.item_id is not None:
        item.item_id = item_update.item_id
    
    if item_update.quantity is not None:
        item.quantity = item_update.quantity
    
    if item_update.price is not None:
        item.price = item_update.price
    
    item.updated_at = datetime.utcnow()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@invoice_items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an invoice item"""
    item = db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice item not found"
        )
    
    db.delete(item)
    db.commit()


# ============================================================
# Notifications Router
# ============================================================

notifications_router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@notifications_router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    """Create a new notification"""
    # Validate user exists
    user = db.query(User).filter(User.id == notification.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@notifications_router.get("", response_model=list[NotificationResponse])
async def get_all_notifications(
    skip: int = 0,
    limit: int = 10,
    user_id: UUID = None,
    type: str = None,
    is_read: bool = None,
    db: Session = Depends(get_db),
):
    """Get all notifications with optional filters"""
    query = db.query(Notification)
    
    if user_id:
        query = query.filter(Notification.user_id == user_id)
    if type:
        query = query.filter(Notification.type == type)
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


@notifications_router.get("/{id}", response_model=NotificationResponse)
async def get_notification(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single notification by ID"""
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification


@notifications_router.get("/user/{user_id}", response_model=list[NotificationResponse])
async def get_user_notifications(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    type: str = None,
    is_read: bool = None,
    db: Session = Depends(get_db),
):
    """Get notifications for a specific user"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if type:
        query = query.filter(Notification.type == type)
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


@notifications_router.get("/user/{user_id}/unread", response_model=list[NotificationResponse])
async def get_user_unread_notifications(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get unread notifications for a specific user"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


@notifications_router.put("/{id}", response_model=NotificationResponse)
async def update_notification(
    id: UUID,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
):
    """Update a notification"""
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    update_data = notification_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(notification, key, value)
    
    db.commit()
    db.refresh(notification)
    return notification


@notifications_router.put("/{id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


@notifications_router.put("/user/{user_id}/read-all", response_model=dict)
async def mark_all_user_notifications_as_read(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Mark all notifications for a user as read"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    
    db.commit()
    return {"message": f"Marked {updated_count} notification(s) as read"}


@notifications_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a notification"""
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()


@notifications_router.delete("/user/{user_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_user_notifications(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete all notifications for a user"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.query(Notification).filter(Notification.user_id == user_id).delete()
    db.commit()


# ============================================================
# Search Logs Router
# ============================================================

search_logs_router = APIRouter(prefix="/api/search-logs", tags=["search-logs"])


@search_logs_router.post("", response_model=SearchLogResponse, status_code=status.HTTP_201_CREATED)
async def create_search_log(
    search_log: SearchLogCreate,
    db: Session = Depends(get_db),
):
    """Create a new search log"""
    # Validate user exists
    user = db.query(User).filter(User.id == search_log.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_search_log = SearchLog(**search_log.dict())
    db.add(db_search_log)
    db.commit()
    db.refresh(db_search_log)
    return db_search_log


@search_logs_router.get("", response_model=list[SearchLogResponse])
async def get_all_search_logs(
    skip: int = 0,
    limit: int = 10,
    user_id: UUID = None,
    db: Session = Depends(get_db),
):
    """Get all search logs with optional user filter"""
    query = db.query(SearchLog)
    
    if user_id:
        query = query.filter(SearchLog.user_id == user_id)
    
    return query.order_by(SearchLog.created_at.desc()).offset(skip).limit(limit).all()


@search_logs_router.get("/{id}", response_model=SearchLogResponse)
async def get_search_log(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single search log by ID"""
    search_log = db.query(SearchLog).filter(SearchLog.id == id).first()
    if not search_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search log not found"
        )
    return search_log


@search_logs_router.get("/user/{user_id}", response_model=list[SearchLogResponse])
async def get_user_search_logs(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get search logs for a specific user"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db.query(SearchLog).filter(SearchLog.user_id == user_id).order_by(SearchLog.created_at.desc()).offset(skip).limit(limit).all()


@search_logs_router.put("/{id}", response_model=SearchLogResponse)
async def update_search_log(
    id: UUID,
    search_log_update: SearchLogUpdate,
    db: Session = Depends(get_db),
):
    """Update a search log"""
    search_log = db.query(SearchLog).filter(SearchLog.id == id).first()
    if not search_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search log not found"
        )
    
    update_data = search_log_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(search_log, key, value)
    
    db.commit()
    db.refresh(search_log)
    return search_log


@search_logs_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_log(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a search log"""
    search_log = db.query(SearchLog).filter(SearchLog.id == id).first()
    if not search_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search log not found"
        )
    
    db.delete(search_log)
    db.commit()


@search_logs_router.delete("/user/{user_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_search_logs(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete all search logs for a user"""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.query(SearchLog).filter(SearchLog.user_id == user_id).delete()
    db.commit()


# ============================================================
# Symptom Checker Router
# ============================================================

symptom_checkers_router = APIRouter(prefix="/api/symptom-checkers", tags=["symptom-checkers"])


@symptom_checkers_router.post("", response_model=SymptomCheckerResponse, status_code=status.HTTP_201_CREATED)
async def create_symptom_checker(
    symptom_checker: SymptomCheckerCreate,
    db: Session = Depends(get_db),
):
    """Create a new symptom checker record"""
    # Validate confidence score is between 0 and 1
    if symptom_checker.confidence_score < 0 or symptom_checker.confidence_score > 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Confidence score must be between 0.00 and 1.00"
        )
    
    db_symptom_checker = SymptomChecker(**symptom_checker.dict())
    db.add(db_symptom_checker)
    db.commit()
    db.refresh(db_symptom_checker)
    return db_symptom_checker


@symptom_checkers_router.get("", response_model=list[SymptomCheckerResponse])
async def get_all_symptom_checkers(
    skip: int = 0,
    limit: int = 10,
    min_confidence: float = None,
    db: Session = Depends(get_db),
):
    """Get all symptom checker records with optional filtering"""
    query = db.query(SymptomChecker)
    
    if min_confidence is not None:
        if min_confidence < 0 or min_confidence > 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Confidence score must be between 0.00 and 1.00"
            )
        query = query.filter(SymptomChecker.confidence_score >= min_confidence)
    
    return query.order_by(SymptomChecker.created_at.desc()).offset(skip).limit(limit).all()


@symptom_checkers_router.get("/{id}", response_model=SymptomCheckerResponse)
async def get_symptom_checker(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single symptom checker record by ID"""
    symptom_checker = db.query(SymptomChecker).filter(SymptomChecker.id == id).first()
    if not symptom_checker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom checker record not found"
        )
    return symptom_checker


@symptom_checkers_router.get("/search/by-symptoms", response_model=list[SymptomCheckerResponse])
async def search_symptom_checkers(
    symptoms: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Search symptom checker records by symptoms"""
    # Using LIKE for case-insensitive partial matching
    return db.query(SymptomChecker).filter(
        SymptomChecker.symptoms.ilike(f"%{symptoms}%")
    ).order_by(SymptomChecker.created_at.desc()).offset(skip).limit(limit).all()


@symptom_checkers_router.get("/search/by-disease", response_model=list[SymptomCheckerResponse])
async def search_by_disease(
    disease: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Search symptom checker records by disease"""
    # Using LIKE for case-insensitive partial matching
    return db.query(SymptomChecker).filter(
        SymptomChecker.suggested_disease.ilike(f"%{disease}%")
    ).order_by(SymptomChecker.created_at.desc()).offset(skip).limit(limit).all()


@symptom_checkers_router.put("/{id}", response_model=SymptomCheckerResponse)
async def update_symptom_checker(
    id: UUID,
    symptom_checker_update: SymptomCheckerUpdate,
    db: Session = Depends(get_db),
):
    """Update a symptom checker record"""
    symptom_checker = db.query(SymptomChecker).filter(SymptomChecker.id == id).first()
    if not symptom_checker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom checker record not found"
        )
    
    # Validate confidence score if provided
    if symptom_checker_update.confidence_score is not None:
        if symptom_checker_update.confidence_score < 0 or symptom_checker_update.confidence_score > 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Confidence score must be between 0.00 and 1.00"
            )
    
    update_data = symptom_checker_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(symptom_checker, key, value)
    
    db.commit()
    db.refresh(symptom_checker)
    return symptom_checker


@symptom_checkers_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_symptom_checker(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a symptom checker record"""
    symptom_checker = db.query(SymptomChecker).filter(SymptomChecker.id == id).first()
    if not symptom_checker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom checker record not found"
        )
    
    db.delete(symptom_checker)
    db.commit()


# ============================================================
# OTP Verification Router
# ============================================================

otp_verification_router = APIRouter(prefix="/api/otp-verification", tags=["otp_verification"])


@otp_verification_router.post("", response_model=OTPVerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_otp_verification(
    otp_data: OTPVerificationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new OTP verification record
    
    - **mobile**: Mobile phone number
    - **otp**: One-time password
    - **expires_at**: OTP expiration timestamp
    """
    # Check if there's already an active OTP for this mobile
    existing_otp = db.query(OTPVerification).filter(
        OTPVerification.mobile == otp_data.mobile,
        OTPVerification.expires_at > datetime.utcnow()
    ).first()
    
    if existing_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An active OTP already exists for this mobile number"
        )
    
    # Create new OTP verification
    db_otp = OTPVerification(
        mobile=otp_data.mobile,
        otp=otp_data.otp,
        expires_at=otp_data.expires_at,
        is_verified=False
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp


@otp_verification_router.get("", response_model=list[OTPVerificationResponse])
async def get_all_otp_verifications(
    skip: int = 0,
    limit: int = 10,
    mobile: str = None,
    is_verified: bool = None,
    db: Session = Depends(get_db),
):
    """
    Get all OTP verification records with optional filtering
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **mobile**: Filter by mobile number
    - **is_verified**: Filter by verification status
    """
    query = db.query(OTPVerification)
    
    if mobile:
        query = query.filter(OTPVerification.mobile == mobile)
    
    if is_verified is not None:
        query = query.filter(OTPVerification.is_verified == is_verified)
    
    return query.order_by(OTPVerification.created_at.desc()).offset(skip).limit(limit).all()


@otp_verification_router.post("/verify", response_model=OTPVerificationCheckResponse)
async def verify_otp(
    verify_request: OTPVerificationCheckRequest,
    db: Session = Depends(get_db),
):
    """
    Verify an OTP for a given mobile number
    
    - **mobile**: Mobile phone number
    - **otp**: One-time password to verify
    """
    # Find the OTP record for this mobile
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.mobile == verify_request.mobile
    ).order_by(OTPVerification.created_at.desc()).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No OTP record found for this mobile number"
        )
    
    # Check if OTP has expired
    if otp_record.expires_at <= datetime.utcnow():
        return OTPVerificationCheckResponse(
            success=False,
            message="OTP has expired",
            is_verified=False
        )
    
    # Check if OTP matches
    if otp_record.otp != verify_request.otp:
        return OTPVerificationCheckResponse(
            success=False,
            message="Invalid OTP",
            is_verified=False
        )
    
    # Mark OTP as verified
    otp_record.is_verified = True
    db.commit()
    db.refresh(otp_record)
    
    return OTPVerificationCheckResponse(
        success=True,
        message="OTP verified successfully",
        is_verified=True
    )


@otp_verification_router.get("/by-mobile/{mobile}", response_model=list[OTPVerificationResponse])
async def get_otp_by_mobile(
    mobile: str,
    db: Session = Depends(get_db),
):
    """Get all OTP verification records for a specific mobile number"""
    otp_records = db.query(OTPVerification).filter(
        OTPVerification.mobile == mobile
    ).order_by(OTPVerification.created_at.desc()).all()
    
    if not otp_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No OTP records found for this mobile number"
        )
    
    return otp_records


@otp_verification_router.get("/{id}", response_model=OTPVerificationResponse)
async def get_otp_verification(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific OTP verification record by ID"""
    otp_verification = db.query(OTPVerification).filter(OTPVerification.id == id).first()
    if not otp_verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP verification record not found"
        )
    return otp_verification


@otp_verification_router.put("/{id}", response_model=OTPVerificationResponse)
async def update_otp_verification(
    id: UUID,
    otp_update: OTPVerificationUpdate,
    db: Session = Depends(get_db),
):
    """Update an OTP verification record"""
    otp_verification = db.query(OTPVerification).filter(OTPVerification.id == id).first()
    if not otp_verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP verification record not found"
        )
    
    update_data = otp_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(otp_verification, key, value)
    
    db.commit()
    db.refresh(otp_verification)
    return otp_verification


@otp_verification_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_otp_verification(
    id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an OTP verification record"""
    otp_verification = db.query(OTPVerification).filter(OTPVerification.id == id).first()
    if not otp_verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP verification record not found"
        )
    
    db.delete(otp_verification)
    db.commit()


router = APIRouter()
router.include_router(user_router)
router.include_router(item_router)
router.include_router(doctor_router)
router.include_router(doctor_categories_router)
router.include_router(drugs_router)
router.include_router(stock_transactions_router)
router.include_router(vendor_router)
router.include_router(vendor_orders_router)
router.include_router(appointment_router)
router.include_router(prescription_router)
router.include_router(prescription_items_router)
router.include_router(medical_records_router)
router.include_router(payments_router)
router.include_router(invoices_router)
router.include_router(invoice_items_router)
router.include_router(notifications_router)
router.include_router(search_logs_router)
router.include_router(symptom_checkers_router)
router.include_router(otp_verification_router)
