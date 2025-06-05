# app/api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud # Importa os módulos
from app.models import models as orm_models
from app.schemas import schemas as pydantic_schemas
from app.api import deps # Importa as dependências

router = APIRouter()

@router.post("/", response_model=pydantic_schemas.User, status_code=status.HTTP_201_CREATED, tags=["Usuários"])
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

    created_user = await crud.create_user(db=db, user=user_in)
    return created_user

@router.get("/me", response_model=pydantic_schemas.User, tags=["Usuários"])
async def read_users_me(
    current_user: orm_models.UserOrm = Depends(deps.get_current_user)
):
    """
    Retorna os dados do usuário autenticado.
    """
    return current_user

@router.get("/", response_model=list[pydantic_schemas.User], tags=["Usuários"])
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
