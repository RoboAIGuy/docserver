"""
PYTHON FILE TO STORE PYDANTIC MODELS OR SCHEMAS REPRESENTING JSON FORMATS WHILE INTERACTING WITH API/DB
"""

from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import validator
from datetime import datetime
from fastapi import Query



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    
    class Config:
        orm_mode = True
        
class UserRead(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime = None
    id: int
    
    class Config:
        orm_mode = True
        
        

class DocumentCreate(BaseModel):
    title: str
    content: str
    creator: EmailStr
    public: Optional[bool] = False
    
    class Config:
        orm_mode = True

class DocumentUpdate(BaseModel):
    creator: EmailStr
    title: Optional[str] = None
    content: Optional[str] = None
    public: Optional[bool]
    
    class Config:
        orm_mode = True
        
class DocumentRead(BaseModel):
    id: int
    title: str
    creator: EmailStr
    public: bool
    
    class Config:
        orm_mode = True
        
class DocumentReadContent(BaseModel):
    title: str
    creator: EmailStr
    content: str
    
    class Config:
        orm_mode = True

class DocumentDelete(BaseModel):
    title: str
    creator: EmailStr


class PermissionCreate(BaseModel):
    document_title: str
    user_email: EmailStr
    can_read: bool = False
    can_write: bool = False
    can_delete: bool = False
    
    class Config:
        orm_mode = True
        
class PermissionRead(PermissionCreate):
    id: int

    class Config:
        orm_mode = True
        
        
class PermissionUpdate(BaseModel):
    document_title: str
    user_email: EmailStr
    can_read: Optional[bool] = False
    can_write: Optional[bool] = False
    can_delete: Optional[bool] = False
    
    class Config:
        orm_mode = True
