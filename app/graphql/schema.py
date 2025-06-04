# app/graphql/schema.py
import strawberry
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import models as orm_models # Renomeado para evitar conflito com tipos Strawberry
from app.schemas import schemas as pydantic_schemas
from app.crud import crud
from app.graphql.context import get_graphql_context # Importa o context getter

# --- Tipos GraphQL ---

# Usando pydantic.type para converter automaticamente schemas Pydantic para tipos Strawberry
@strawberry.experimental.pydantic.type(model=pydantic_schemas.Author, all_fields=True)
class AuthorGQLType:
    pass

@strawberry.experimental.pydantic.type(model=pydantic_schemas.Material, all_fields=True)
class MaterialGQLType:
    # Strawberry tentará resolver 'author: Author' do Pydantic para AuthorGQLType.
    # Se o Pydantic schema for `author: pydantic_schemas.Author`
    # e você tiver `AuthorGQLType` definido, deve funcionar.
    # Caso contrário, você pode definir explicitamente:
    # author: AuthorGQLType
    pass

@strawberry.experimental.pydantic.type(model=pydantic_schemas.User, all_fields=True)
class UserGQLType:
    pass


# --- Inputs para Mutations ---

@strawberry.experimental.pydantic.input(model=pydantic_schemas.MaterialCreate, all_fields=True)
class MaterialCreateGQLInput:
    # Strawberry pode inferir os campos do Pydantic schema.
    # Se precisar de customização, defina os campos aqui.
    # Ex: title: str
    #     description: Optional[str] = strawberry.UNSET
    #     material_type: orm_models.MaterialTypeEnum
    #     author_id: int
    pass

@strawberry.experimental.pydantic.input(model=pydantic_schemas.AuthorCreate, all_fields=True)
class AuthorCreateGQLInput:
    # name: strawberry.auto
    # city: strawberry.auto
    # author_type: strawberry.auto
    pass

@strawberry.experimental.pydantic.input(model=pydantic_schemas.UserCreate, all_fields=True)
class UserCreateGQLInput:
    pass


# --- Queries ---

@strawberry.type
class Query:
    @strawberry.field
    async def materials(
        self,
        info: strawberry.Info,
        skip: int = 0,
        limit: int = 10
    ) -> List[MaterialGQLType]:
        db: AsyncSession = info.context["db"]
        materials_orm = await crud.get_materials_crud(db, skip=skip, limit=limit)
        # A conversão de ORM para Pydantic e depois para Strawberry é feita pelo .from_pydantic
        return [MaterialGQLType.from_pydantic(pydantic_schemas.Material.from_orm(m)) for m in materials_orm]

    @strawberry.field
    async def material(self, info: strawberry.Info, id: int) -> Optional[MaterialGQLType]:
        db: AsyncSession = info.context["db"]
        material_orm = await crud.get_material_crud(db, material_id=id)
        if material_orm:
            return MaterialGQLType.from_pydantic(pydantic_schemas.Material.from_orm(material_orm))
        return None

    @strawberry.field
    async def authors(
        self,
        info: strawberry.Info,
        skip: int = 0,
        limit: int = 10
    ) -> List[AuthorGQLType]:
        db: AsyncSession = info.context["db"]
        authors_orm = await crud.get_authors_crud(db, skip=skip, limit=limit)
        return [AuthorGQLType.from_pydantic(pydantic_schemas.Author.from_orm(a)) for a in authors_orm]

    @strawberry.field
    async def author(self, info: strawberry.Info, id: int) -> Optional[AuthorGQLType]:
        db: AsyncSession = info.context["db"]
        author_orm = await crud.get_author_crud(db, author_id=id)
        if author_orm:
            return AuthorGQLType.from_pydantic(pydantic_schemas.Author.from_orm(author_orm))
        return None

    # Adicionar query para user (ex: user(id: int) ou me())
    # @strawberry.field
    # async def me(self, info: strawberry.Info) -> Optional[UserGQLType]:
    #     current_user = info.context.get("current_user") # Supondo que get_graphql_context injete
    #     if current_user:
    #         return UserGQLType.from_pydantic(pydantic_schemas.User.from_orm(current_user))
    #     return None


# --- Mutations ---

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_material(
        self, info: strawberry.Info, material_data: MaterialCreateGQLInput
    ) -> MaterialGQLType:
        db: AsyncSession = info.context["db"]
        # current_user_id = info.context.get("current_user_id") # Se o uploader for obrigatório
        # if not current_user_id:
        #     raise Exception("Usuário não autenticado para criar material.")

        # Converta o input GraphQL para o schema Pydantic esperado pelo CRUD
        # O .to_pydantic faz a conversão do input Strawberry para o Pydantic model
        pydantic_material_create = material_data.to_pydantic()

        # Verifica se o autor existe
        author_orm = await crud.get_author_crud(db, author_id=pydantic_material_create.author_id)
        if not author_orm:
            raise Exception(f"Autor com ID {pydantic_material_create.author_id} não encontrado.")

        # uploader_id pode vir do contexto se a mutação for protegida
        uploader_id_from_context = None # Exemplo: info.context.get("current_user_id")
        created_material_orm = await crud.create_material_crud(
            db=db,
            material=pydantic_material_create,
            uploader_id=uploader_id_from_context
        )
        return MaterialGQLType.from_pydantic(pydantic_schemas.Material.from_orm(created_material_orm))

    @strawberry.mutation
    async def create_author(
        self, info: strawberry.Info, author_data: AuthorCreateGQLInput
    ) -> AuthorGQLType:
        db: AsyncSession = info.context["db"]
        pydantic_author_create = author_data.to_pydantic()
        created_author_orm = await crud.create_author_crud(db=db, author=pydantic_author_create)
        return AuthorGQLType.from_pydantic(pydantic_schemas.Author.from_orm(created_author_orm))

    @strawberry.mutation
    async def create_user(
        self, info: strawberry.Info, user_data: UserCreateGQLInput
    ) -> UserGQLType:
        db: AsyncSession = info.context["db"]
        pydantic_user_create = user_data.to_pydantic()

        # Verificar se usuário ou email já existem
        existing_user_by_username = await crud.get_user_by_username(db, username=pydantic_user_create.username)
        if existing_user_by_username:
            raise Exception(f"Username '{pydantic_user_create.username}' já registrado.")
        existing_user_by_email = await crud.get_user_by_email(db, email=pydantic_user_create.email)
        if existing_user_by_email:
            raise Exception(f"Email '{pydantic_user_create.email}' já registrado.")

        created_user_orm = await crud.create_user(db=db, user=pydantic_user_create)
        return UserGQLType.from_pydantic(pydantic_schemas.User.from_orm(created_user_orm))


# Crie o schema GraphQL
# O context_getter é crucial para injetar a sessão do DB e outras dependências.
graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    # types=[MaterialGQLType, AuthorGQLType, UserGQLType] # Opcional, Strawberry geralmente descobre
)
