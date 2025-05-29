from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base # Importa a Base do seu arquivo database.py

class AuthorOrm(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, nullable=True) # Exemplo de campo para Autor (Instituição)

    materials = relationship("MaterialOrm", back_populates="author")

class MaterialOrm(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="rascunho") # Adicionando o campo status
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("AuthorOrm", back_populates="materials")

# Adicione outros modelos conforme necessário (User, Book, Article, Video)