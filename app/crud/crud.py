# app/crud/crud.py
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import models # Alterado para importar o módulo models
from app.schemas import schemas # Alterado para importar o módulo schemas
from app.core.security import get_password_hash

# --- User CRUD ---
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.UserOrm]:
    result = await db.execute(select(models.UserOrm).filter(models.UserOrm.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.UserOrm]:
    result = await db.execute(select(models.UserOrm).filter(models.UserOrm.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.UserOrm:
    hashed_password = get_password_hash(user.password)
    db_user = models.UserOrm(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
        # is_active e is_superuser terão seus defaults do modelo ORM
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Author CRUD ---
async def create_author_crud(db: AsyncSession, author: schemas.AuthorCreate) -> models.AuthorOrm:
    db_author = models.AuthorOrm(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

async def get_authors_crud(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[models.AuthorOrm]:
    result = await db.execute(select(models.AuthorOrm).offset(skip).limit(limit))
    return list(result.scalars().all())

async def get_author_crud(db: AsyncSession, author_id: int) -> Optional[models.AuthorOrm]:
    result = await db.execute(select(models.AuthorOrm).filter(models.AuthorOrm.id == author_id))
    return result.scalars().first()

# --- Material CRUD ---
async def create_material_crud(db: AsyncSession, material: schemas.MaterialCreate, uploader_id: Optional[int] = None) -> models.MaterialOrm:
    db_material = models.MaterialOrm(**material.model_dump(), uploader_id=uploader_id)
    db.add(db_material)
    await db.commit()
    await db.refresh(db_material) 
    # Carrega o autor associado ao material
    await db.refresh(db_material, attribute_names=['author'])

    return db_material

async def get_materials_crud(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[models.MaterialOrm]:
    result = await db.execute(
        select(models.MaterialOrm)
        .options(selectinload(models.MaterialOrm.author))
        .order_by(models.MaterialOrm.id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all()) # Convertendo para lista

async def get_material_crud(db: AsyncSession, material_id: int) -> Optional[models.MaterialOrm]:
    result = await db.execute(
        select(models.MaterialOrm)
        .options(selectinload(models.MaterialOrm.author))
        .filter(models.MaterialOrm.id == material_id)
    )
    return result.scalars().first()

async def update_material_crud(
    db: AsyncSession, material_db_obj: models.MaterialOrm, material_in: schemas.MaterialUpdate
) -> models.MaterialOrm:
    update_data = material_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(material_db_obj, field, value)
    db.add(material_db_obj)
    await db.commit()
    await db.refresh(material_db_obj)
    return material_db_obj

async def delete_material_crud(db: AsyncSession, material_id: int) -> Optional[models.MaterialOrm]:
    db_material = await get_material_crud(db, material_id=material_id)
    if db_material:
        await db.delete(db_material)
        await db.commit()
    return db_material
