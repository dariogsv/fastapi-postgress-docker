# app/api/routers/materials.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps # Importa as dependências
from app.crud import crud # Importa os módulos
from app.models import models as orm_models
from app.schemas import schemas as pydantic_schemas

router = APIRouter()

@router.post("/", response_model=pydantic_schemas.Material, status_code=status.HTTP_201_CREATED, tags=["Materiais"])
async def create_new_material(
    material_in: pydantic_schemas.MaterialCreate,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: orm_models.UserOrm = Depends(deps.get_current_user) # Usuário logado será o uploader
):
    """
    Cria um novo material. Requer autenticação.
    O usuário autenticado será definido como o 'uploader'.
    """
    # Verifica se o autor existe
    author = await crud.get_author_crud(db, author_id=material_in.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com ID {material_in.author_id} não encontrado"
        )

    return await crud.create_material_crud(db=db, material=material_in, uploader_id=current_user.id)

@router.get("/", response_model=List[pydantic_schemas.Material], tags=["Materiais"])
async def read_all_materials(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_session)
):
    """
    Lista todos os materiais com paginação.
    """
    materials = await crud.get_materials_crud(db, skip=skip, limit=limit)
    return materials

@router.get("/{material_id}", response_model=pydantic_schemas.Material, tags=["Materiais"])
async def read_single_material(
    material_id: int,
    db: AsyncSession = Depends(deps.get_db_session)
):
    """
    Busca um material pelo ID.
    """
    db_material = await crud.get_material_crud(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")
    return db_material

@router.put("/{material_id}", response_model=pydantic_schemas.Material, tags=["Materiais"])
async def update_existing_material(
    material_id: int,
    material_in: pydantic_schemas.MaterialUpdate,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: orm_models.UserOrm = Depends(deps.get_current_user) # Ou superuser, dependendo da regra
):
    """
    Atualiza um material existente.
    """
    db_material = await crud.get_material_crud(db, material_id=material_id)
    if not db_material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")

    # Opcional: Verificar permissão (ex: só o uploader ou superuser pode editar)
    # if db_material.uploader_id != current_user.id and not current_user.is_superuser:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para editar este material")

    # Verifica se o novo author_id (se fornecido) existe
    if material_in.author_id is not None:
        author = await crud.get_author_crud(db, author_id=material_in.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor com ID {material_in.author_id} não encontrado para atualização"
            )

    updated_material = await crud.update_material_crud(db=db, material_db_obj=db_material, material_in=material_in)
    return updated_material

@router.delete("/{material_id}", response_model=pydantic_schemas.Material, tags=["Materiais"]) # Ou status_code=204 e sem response_model
async def delete_existing_material(
    material_id: int,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: orm_models.UserOrm = Depends(deps.get_current_active_superuser) # só superuser pode deletar
):
    """
    Deleta um material. (Exemplo: protegido para superusuários)
    """
    deleted_material = await crud.delete_material_crud(db, material_id=material_id)
    if not deleted_material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")
    return deleted_material # Retorna o objeto deletado ou pode retornar um {"detail": "Material deletado"}
