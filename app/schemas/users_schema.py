from pydantic import BaseModel, EmailStr,field_validator, Field, model_validator
import re
from enums import Gender
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str 
    phone: str
    email: EmailStr
    password: str 
    gender: Gender
    location: str 

    @field_validator('name')
    def validate_name(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('Name cannot be empty!')
        
        if len(v) < 3:
            raise ValueError("Name must be atleast 3 characters long")
        
        if len(v) > 30:
            raise ValueError("Name cannot be more than 30 characters long")
        
        return v
    
    @field_validator('phone')
    def validate_phone(cls, value):
        value = value.strip()  
        if not value:
            raise ValueError('Phone cannot be empty!')
    
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) != 11:
            raise ValueError("Phone number must be exactly 11 digits")

        return value

    
    @field_validator("password")
    def validate_password(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('Password cannot be empty!')
    
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")

        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False

        specials = "@$!%*#?&"

        for passwd in v:
            if passwd.islower():
                has_lower = True
            elif passwd.isupper():
                has_upper = True
            elif passwd.isdigit():
                has_digit = True
            elif passwd in specials:
                has_special = True

        if not has_lower:
            raise ValueError("Password must contain a lowercase letter")

        if not has_upper:
            raise ValueError("Password must contain an uppercase letter")

        if not has_digit:
            raise ValueError("Password must contain a number")

        if not has_special:
            raise ValueError("Password must contain a special character (@$!%*#?&)")

        return v
    
    @field_validator('location')
    def validate_location(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('location cannot be empty!')
        
        if len(v) < 3:
            raise ValueError("location must be atleast 3 characters long")
        
        if len(v) > 255:
            raise ValueError("location cannot be more than 30 characters long")
        
        return v

    
    # @model_validator(mode='after')
    # def validate_confirm_password(self):
    #     if self.password != self.confirm_password:
    #         raise ValueError('passwords must match')
    #     return self

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    location: Optional[str] = None

    @field_validator('name')
    def validate_name(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('Name cannot be empty!')
        
        if len(v) < 3:
            raise ValueError("Name must be atleast 3 characters long")
        
        if len(v) > 30:
            raise ValueError("Name cannot be more than 30 characters long")
        
        return v
    
    @field_validator('phone')
    def validate_phone(cls, value):
        value = value.strip()  
        if not value:
            raise ValueError('Phone cannot be empty!')
    
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) != 11:
            raise ValueError("Phone number must be exactly 11 digits")

        return value
    
    @field_validator('location')
    def validate_location(cls, v):
        v = v.strip()  
        if not v:
            raise ValueError('location cannot be empty!')
        
        if len(v) < 3:
            raise ValueError("location must be atleast 3 characters long")
        
        if len(v) > 255:
            raise ValueError("location cannot be more than 30 characters long")
        
        return v

    # @model_validator(mode='after')
    # def validate_confirm_password(self):
    #     if self.password != self.confirm_password:
    #         raise ValueError('passwords must match')
    #     return self

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    location: str
    created_at: datetime
    updated_at: datetime


    