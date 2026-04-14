"""
API routes for users, doctors, items, and drugs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import bcrypt

from app.database import get_db
from app.models import User, Item, Doctor, DoctorDocument, Drug, StockTransaction, Vendor, VendorOrder
from app.schemas import (
    UserCreate, UserResponse, UserUpdate, UserInDB, 
    ItemCreate, ItemResponse,
    DoctorCreate, DoctorResponse, DoctorUpdate, DoctorDetailResponse, DoctorVerificationUpdate,
    DoctorDocumentCreate, DoctorDocumentResponse, DoctorDocumentUpdate, DoctorDocumentVerify,
    DrugCreate, DrugResponse, DrugUpdate,
    StockTransactionCreate, StockTransactionResponse, StockTransactionUpdate, StockTransactionDetailResponse
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
    - **experience**: Years of experience (non-negative integer)
    - **consultation_fee**: Consultation fee (positive decimal)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == doctor_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Optionally check if user has doctor role
    if user.role != 'doctor':
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
    
    # Create doctor profile
    db_doctor = Doctor(
        user_id=doctor_data.user_id,
        specialization=doctor_data.specialization,
        experience=doctor_data.experience,
        consultation_fee=doctor_data.consultation_fee,
        verification_status='pending'
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@doctor_router.get("", response_model=list[DoctorResponse])
async def get_all_doctors(
    skip: int = 0,
    limit: int = 10,
    verification_status: str = None,
    db: Session = Depends(get_db),
):
    """
    Get all doctors with optional filtering
    
    - **skip**: Number of doctors to skip (default: 0)
    - **limit**: Maximum number of doctors to return (default: 10)
    - **verification_status**: Filter by status (pending, approved, rejected)
    """
    query = db.query(Doctor)
    
    if verification_status:
        query = query.filter(Doctor.verification_status == verification_status)
    
    doctors = query.offset(skip).limit(limit).all()
    return doctors


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
    if doctor_update.experience is not None:
        doctor.experience = doctor_update.experience
    if doctor_update.consultation_fee is not None:
        doctor.consultation_fee = doctor_update.consultation_fee
    
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
# Doctor Documents Router (new)
# ============================================================

doctor_documents_router = APIRouter(prefix="/api/doctor-documents", tags=["doctor-documents"])


@doctor_documents_router.post("", response_model=DoctorDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_doctor_document(
    document: DoctorDocumentCreate,
    db: Session = Depends(get_db),
):
    """
    Upload a new doctor document
    
    - **doctor_id**: UUID of the doctor
    - **document_type**: Type of document (e.g., license, degree, certification)
    - **file_url**: URL to the uploaded file
    """
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == document.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Check if user associated with doctor has doctor role
    user = db.query(User).filter(User.id == doctor.user_id).first()
    if user.role != 'doctor':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Associated user must have 'doctor' role"
        )
    
    # Create document record
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


@doctor_documents_router.get("", response_model=list[DoctorDocumentResponse])
async def get_all_documents(
    skip: int = 0,
    limit: int = 10,
    doctor_id: UUID = None,
    verified: bool = None,
    db: Session = Depends(get_db),
):
    """
    Get all doctor documents with optional filtering
    
    - **skip**: Number of documents to skip (default: 0)
    - **limit**: Maximum number of documents to return (default: 10)
    - **doctor_id**: Filter by specific doctor (optional)
    - **verified**: Filter by verification status (optional)
    """
    query = db.query(DoctorDocument)
    
    if doctor_id:
        query = query.filter(DoctorDocument.doctor_id == doctor_id)
    
    if verified is not None:
        query = query.filter(DoctorDocument.verified == verified)
    
    documents = query.offset(skip).limit(limit).all()
    return documents


@doctor_documents_router.get("/{document_id}", response_model=DoctorDocumentResponse)
async def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific document by ID"""
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document


@doctor_documents_router.get("/doctor/{doctor_id}", response_model=list[DoctorDocumentResponse])
async def get_doctor_documents(
    doctor_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get all documents for a specific doctor"""
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    documents = db.query(DoctorDocument).filter(
        DoctorDocument.doctor_id == doctor_id
    ).offset(skip).limit(limit).all()
    
    return documents


@doctor_documents_router.put("/{document_id}", response_model=DoctorDocumentResponse)
async def update_document(
    document_id: UUID,
    document_update: DoctorDocumentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a doctor document
    
    - **document_type**: Update document type (optional)
    - **file_url**: Update file URL (optional)
    """
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Update fields
    if document_update.document_type is not None:
        document.document_type = document_update.document_type
    if document_update.file_url is not None:
        document.file_url = document_update.file_url
    
    db.commit()
    db.refresh(document)
    return document


@doctor_documents_router.post("/{document_id}/verify", response_model=DoctorDocumentResponse)
async def verify_document(
    document_id: UUID,
    verification: DoctorDocumentVerify,
    db: Session = Depends(get_db),
):
    """
    Verify or reject a doctor document
    
    - **verified**: Set verification status (true/false)
    """
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    document.verified = verification.verified
    db.commit()
    db.refresh(document)
    return document


@doctor_documents_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a document by ID"""
    document = db.query(DoctorDocument).filter(DoctorDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    db.delete(document)
    db.commit()


# ============================================================
# Drugs Router (new)
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


# Create combined router for easy import
router = APIRouter()
router.include_router(user_router)
router.include_router(item_router)
router.include_router(doctor_router)
router.include_router(doctor_documents_router)
router.include_router(drugs_router)
router.include_router(stock_transactions_router)
