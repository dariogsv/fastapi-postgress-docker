# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter

from app.api.routers import auth, users, authors, materials
from app.graphql.schema import graphql_schema # Importa o schema GraphQL montado
from app.graphql.context import get_graphql_context # Importa o getter de contexto
from app.db.init_db import create_tables_on_startup # Para criar tabelas no início (opcional)

# --- Eventos de Startup/Shutdown ---
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Executa ações no início da aplicação.
    Ideal para criar tabelas no banco de dados (em desenvolvimento).
    """
    print("Aplicação iniciando...")
    await create_tables_on_startup() # Cria tabelas se não existirem
    print("Tabelas do banco de dados verificadas/criadas.")
    print("Servidor pronto.")
    yield
    # Código de limpeza
    print("Aplicação encerrando...")

app = FastAPI(
    title="Biblioteca Digital API",
    description="API para gerenciar uma biblioteca digital com autenticação, usuários, autores e materiais.",
    version="0.2.0",
    lifespan=lifespan
)
# --- Montar Routers da API REST ---
api_prefix = "/api/v1"

app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Autenticação REST"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Usuários REST"])
app.include_router(authors.router, prefix=f"{api_prefix}/authors", tags=["Autores REST"])
app.include_router(materials.router, prefix=f"{api_prefix}/materials", tags=["Materiais REST"])


# --- Montar GraphQL ---
# O context_getter é passado para o GraphQLRouter para que as resolvers tenham acesso ao contexto.
graphql_app_router = GraphQLRouter(
    schema=graphql_schema,
    context_getter=get_graphql_context,
    graphiql=True # Habilita a interface GraphiQL (ótimo para desenvolvimento)
)
app.include_router(graphql_app_router, prefix="/graphql", tags=["GraphQL"])


# --- Rota Raiz (Opcional) ---
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Bem-vindo à API da Biblioteca Digital!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "graphql_url": "/graphql"
    }
