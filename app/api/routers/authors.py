# app/api/routers/authors.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.exc
import asyncpg

from app.api import deps # Importa as dependências
from app.crud import crud # Importa os módulos
from app.models import models as orm_models
from app.schemas import schemas as pydantic_schemas

router = APIRouter()

@router.post("/", response_model=pydantic_schemas.Author, status_code=status.HTTP_201_CREATED)
async def create_new_author(
    author_in: pydantic_schemas.AuthorCreate,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: orm_models.UserOrm = Depends(deps.get_current_user) # Protegendo o endpoint
):
    """
    Cria um novo autor. Requer autenticação.
    """
    try:
        created_author = await crud.create_author_crud(db=db, author=author_in)
        return created_author
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro de integridade dos dados ao criar autor: {e.orig}")

@router.get("/", response_model=List[pydantic_schemas.Author])
async def read_all_authors(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_session)
):
    """
    Lista todos os autores com paginação.
    """
    authors = await crud.get_authors_crud(db, skip=skip, limit=limit)
    return authors

@router.get("/{author_id}", response_model=pydantic_schemas.Author)
async def read_single_author(
    author_id: int,
    db: AsyncSession = Depends(deps.get_db_session)
):
    """
    Busca um autor pelo ID.
    """
    db_author = await crud.get_author_crud(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado")
    return db_author

# Adicionar PUT e DELETE para autores se necessário, similar ao de materiais
