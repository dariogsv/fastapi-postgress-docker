import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não está configurada.")

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

# Base para os modelos declarativos do SQLAlchemy
Base = declarative_base()

# Função para obter uma sessão de banco de dados (dependência)
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit() # Opcional: fazer commit aqui se todas as operações dentro do 'yield' devem ser commitadas juntas.
                                   # Alternativamente, faça commits explícitos dentro das suas rotas/serviços.
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()