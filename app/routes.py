"""
Example routes demonstrating database usage
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Item
from app.schemas import UserCreate, UserResponse, ItemCreate, ItemResponse


router = APIRouter(prefix="/api", tags=["items"])


@router.post("/items", response_model=ItemResponse)
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


@router.get("/items", response_model=list[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get all active items from the database"""
    items = db.query(Item).filter(Item.is_active == True).offset(skip).limit(limit).all()
    return items


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific item by ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """Create a new user in the database"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get all active users from the database"""
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    return users
