# app/api/deps.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.crud import crud
from app.core import security
from app.models import models
from app.db.database import get_db_session

# OAuth2PasswordBearer define a URL onde o cliente pode obter o token
# O tokenUrl deve corresponder ao endpoint de login/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") # Ajustado para o prefixo do router

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> models.UserOrm:
    """
    Decodifica o token, obtém o username e busca o usuário no banco.
    Levanta HTTPException se o token for inválido ou o usuário não for encontrado.
    """
    username = security.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado com este token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo")
    return user

async def get_current_active_superuser(
    current_user: models.UserOrm = Depends(get_current_user)
) -> models.UserOrm:
    """Verifica se o usuário atual é um superusuário ativo."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permissão de superusuário necessária"
        )
    return current_user
