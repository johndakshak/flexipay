from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user_models import User
from app.schemas.users_schema import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from base import Base
from database import get_db, Session
import logging
import bcrypt
from datetime import datetime

router = APIRouter(prefix='/user', tags=['User'])

logger = logging.getLogger(__name__)

@router.post('/create', response_model=UserResponse)
def create_users(user_create: UserCreate, db: Session = Depends(get_db)):
    
    existing_email = db.query(User).filter(User.email == user_create.email).first()
        
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email: '{user_create.email}' already exist!"
        )
    
    existing_phone = db.query(User).filter(User.phone == user_create.phone).first()

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Phone: '{user_create.phone}' already exist"
        )
    
    password = hash_password(user_create.password)

    new_user = User(
        name=user_create.name,
        phone=user_create.phone,
        email=user_create.email,
        password=password,
        gender=user_create.gender,
        location=user_create.location
    )

    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

@router.get('/', response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users

@router.get('/{user_id}', response_model=list[UserResponse])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID: {user_id} not found!"
        )
    
    return user

@router.put('/update/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User: '{user_id}' not found!"
        )

    phone_exist = db.query(User).filter(User.phone == user_update.phone).first()
    if phone_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Phone: '{user_update.phone}' already exist!"
    )

    email_exist = db.query(User).filter(User.email == user_update.email).first()
    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email: '{user_update.email}' already exist"
        )

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@router.patch('/{user_id}', response_model=UserResponse)
def patch_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User: {user_id} not found!"
        )
    
    phone_exist = db.query(User).filter(User.phone == user_update.phone).first()
    if phone_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Phone: {user_update.phone} already exist"
        )
    
    email_exist = db.query(User).filter(User.email == user_update.email).first()
    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email: '{user_update.email}' already exist"
        )
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User: {user_id} not found!"
        )
    
    db.delete(user)
    db.commit()
    return {
        "message": f"User: {user_id} deleted succssfully!"
        }

def hash_password(password) -> str:
    salts = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salts)
        

