from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user_models import User
from app.schemas.users_schema import UserCreate, UserResponse
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
    
def raiseError(e):
    logger.error(f"failed to create record: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "status": "error",
            "message": "failed to create user: {e}",
            "datetime": f"{datetime.utcnow()}"
        }
    )

def hash_password(password) -> str:
    salts = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salts)
        

