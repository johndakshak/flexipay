from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from enums import Gender
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str
    gender: Gender
    location: str

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    location: str
    role: str
    created_at: datetime
    updated_at: datetime


    