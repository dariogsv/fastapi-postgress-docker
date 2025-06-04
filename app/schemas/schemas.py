from datetime import datetime, date # Para os timestamps e publication_date

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.models import AuthorTypeEnum, MaterialTypeEnum, MaterialStatusEnum

# --- User Schemas ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    time_created: datetime
    time_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    author_type: Optional[AuthorTypeEnum] = AuthorTypeEnum.person

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    time_created: datetime
    time_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Material Schemas ---
class MaterialBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    material_type: MaterialTypeEnum
    status: MaterialStatusEnum = MaterialStatusEnum.draft
    publication_date: Optional[date] = None
    
    # Campos específicos (opcionais na base, validados na criação/atualização específica)
    isbn: Optional[str] = Field(None, max_length=20)
    pages: Optional[int] = Field(None, gt=0)
    doi: Optional[str] = Field(None, max_length=100)
    journal_name: Optional[str] = Field(None, max_length=150)
    duration_seconds: Optional[int] = Field(None, gt=0)
    video_url: Optional[str] = Field(None, max_length=255)


class MaterialCreate(MaterialBase):
    author_id: int

class MaterialUpdate(MaterialBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    material_type: Optional[MaterialTypeEnum] = None # Permitir não atualizar o tipo
    author_id: Optional[int] = None # Permitir não atualizar o autor


class Material(MaterialBase):
    id: int
    author_id: int
    uploader_id: Optional[int] = None
    time_created: datetime
    time_updated: Optional[datetime] = None
    author: Author # Para mostrar dados do autor aninhados

    class Config:
        from_attributes = True