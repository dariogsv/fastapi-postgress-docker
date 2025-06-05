# app/api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.exc
import asyncpg

from app.crud import crud # Importa os módulos
from app.models import models as orm_models
from app.schemas import schemas as pydantic_schemas
from app.api import deps # Importa as dependências

router = APIRouter()

@router.post("/", response_model=pydantic_schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: pydantic_schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db_session)
):
    """
    Registra um novo usuário.
    """
    db_user_by_username = await crud.get_user_by_username(db, username=user_in.username)
    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado")
    db_user_by_email = await crud.get_user_by_email(db, email=user_in.email)
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado")

    try:
        created_user = await crud.create_user(db=db, user=user_in)
        return created_user
    except sqlalchemy.exc.IntegrityError as e:
        if isinstance(e.orig, asyncpg.exceptions.UniqueViolationError):
            if "users_username_key" in str(e.orig).lower() or (e.orig.constraint_name and "username" in e.orig.constraint_name.lower()):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Este nome de usuário já existe."
                )
            elif "users_email_key" in str(e.orig).lower() or (e.orig.constraint_name and "email" in e.orig.constraint_name.lower()):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Este email já está registrado."
                )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro de integridade dos dados ao criar usuário: {e.orig}")

@router.get("/me", response_model=pydantic_schemas.User)
async def read_users_me(
    current_user: orm_models.UserOrm = Depends(deps.get_current_user)
):
    """
    Retorna os dados do usuário autenticado.
    """
    return current_user

@router.get("/", response_model=list[pydantic_schemas.User])
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: orm_models.UserOrm = Depends(deps.get_current_active_superuser) # Protegido
):
    """
    Lista todos os usuários (apenas para superusuários).
    """
    users = await crud.get_users(db, skip=skip, limit=limit) # Precisaria de um crud.get_users
    return users
