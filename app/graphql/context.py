# app/graphql/context.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional

from app.api import deps # Para get_current_user, se necessário no contexto GraphQL
from app.db.database import get_db_session
from app.models import models as orm_models # Renomeado para evitar conflito

async def get_graphql_context(
    db: AsyncSession = Depends(get_db_session),
    # Você pode adicionar a dependência do usuário atual aqui se quiser injetá-lo no contexto GraphQL
    # current_user: Optional[orm_models.UserOrm] = Depends(deps.get_current_user_optional) # Crie get_current_user_optional se necessário
) -> Dict[str, Any]:
    """
    Cria o contexto para as resolvers GraphQL.
    Inclui a sessão do banco de dados e, opcionalmente, o usuário atual.
    """
    context = {"db": db}
    # if current_user:
    #     context["current_user"] = current_user
    #     context["current_user_id"] = current_user.id
    return context
