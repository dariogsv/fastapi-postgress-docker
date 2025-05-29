from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select # Para SQLAlchemy 1.4+ e 2.0

from database import get_db_session, engine, Base # Adicione Base se for criar tabelas aqui
from models import MaterialOrm, AuthorOrm # Importe seus modelos ORM
# import asyncio # Se for usar create_all_tables aqui

app = FastAPI()

# Opcional: criar tabelas ao iniciar (para desenvolvimento)
# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all) # Cuidado
#         await conn.run_sync(Base.metadata.create_all)

@app.post("/authors/", response_model=None) # Defina um Pydantic model para a resposta
async def create_author(name: str, city: str | None = None, db: AsyncSession = Depends(get_db_session)):
    new_author = AuthorOrm(name=name, city=city)
    db.add(new_author)
    # await db.commit() # Commit pode ser feito aqui ou centralizado no get_db_session
    # await db.refresh(new_author) # Para obter o ID gerado, etc.
    return new_author # FastAPI serializará automaticamente

@app.get("/authors/", response_model=list[None]) # Defina um Pydantic model para a lista
async def read_authors(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(AuthorOrm).offset(skip).limit(limit))
    authors = result.scalars().all()
    return authors

@app.post("/materials/", response_model=None) # Defina Pydantic models para request/response
async def create_material(title: str, author_id: int, description: str | None = None, db: AsyncSession = Depends(get_db_session)):
    # Verifique se o autor existe
    author_result = await db.execute(select(AuthorOrm).where(AuthorOrm.id == author_id))
    author = author_result.scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    new_material = MaterialOrm(title=title, description=description, author_id=author_id)
    db.add(new_material)
    # await db.commit()
    # await db.refresh(new_material)
    return new_material

@app.get("/materials/", response_model=list[None])
async def read_materials(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(MaterialOrm).offset(skip).limit(limit))
    materials = result.scalars().all()
    return materials

# Não se esqueça de criar Pydantic models (schemas) para validação de entrada e formatação de saída!