import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum as SAEnum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Para default timestamps

from app.db.base_class import Base

class AuthorTypeEnum(str, enum.Enum):
    person = "person"
    institution = "institution"

class MaterialTypeEnum(str, enum.Enum):
    book = "book"
    article = "article"
    video = "video"

class MaterialStatusEnum(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class UserOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    uploaded_materials = relationship("MaterialOrm", back_populates="uploader")

class AuthorOrm(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    city = Column(String, nullable=True)
    author_type = Column(SAEnum(AuthorTypeEnum), nullable=True, default=AuthorTypeEnum.person)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    materials = relationship("MaterialOrm", back_populates="author")

class MaterialOrm(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    material_type = Column(SAEnum(MaterialTypeEnum), nullable=False, index=True)
    status = Column(SAEnum(MaterialStatusEnum), default=MaterialStatusEnum.draft, nullable=False)
    
    publication_date = Column(Date, nullable=True)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("AuthorOrm", back_populates="materials")

    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    uploader = relationship("UserOrm", back_populates="uploaded_materials")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    isbn = Column(String, nullable=True, unique=True) # books
    pages = Column(Integer, nullable=True) # books
    doi = Column(String, nullable=True, unique=True) # articles
    journal_name = Column(String, nullable=True) # articles
    duration_seconds = Column(Integer, nullable=True) # videos
    video_url = Column(String, nullable=True) #videos
