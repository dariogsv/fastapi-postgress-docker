from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = settings.DATABASE_URL

# Cria o engine assíncrono do SQLAlchemy
# echo=True é útil para debugging, pois mostra as queries SQL geradas
engine = create_async_engine(DATABASE_URL, echo=True)

# Cria uma fábrica de sessões assíncronas
# expire_on_commit=False evita que atributos expirem após o commit,
# o que pode ser útil em operações assíncronas.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Função para obter uma sessão de banco de dados (dependência)
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()