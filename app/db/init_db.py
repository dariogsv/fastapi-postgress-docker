# app/db/init_db.py
import asyncio
from app.db.database import engine # Importa o engine
from app.db.base_class import Base # Importa a Base que contém os metadados das tabelas
# Importar os modelos ORM para que Base.metadata seja populado
from app.models import models # noqa: F401 (para o linter não reclamar de import não usado diretamente)

async def create_tables_on_startup():
    """
    Cria todas as tabelas no banco de dados que são definidas
    e herdadas de Base.metadata.
    """
    async with engine.begin() as conn:
        # Em um ambiente de produção, você pode querer usar ferramentas de migração como Alembic
        # await conn.run_sync(Base.metadata.drop_all) # CUIDADO: Apaga todas as tabelas! Use apenas em dev.
        await conn.run_sync(Base.metadata.create_all)
    # Não é estritamente necessário descartar o engine aqui se ele for usado pela aplicação principal,
    # mas se este script fosse executado isoladamente, seria uma boa prática.
    # await engine.dispose()

async def main():
    """Função principal para executar a criação de tabelas como um script."""
    print("Iniciando criação/verificação de tabelas...")
    await create_tables_on_startup()
    print("Processo de tabelas concluído.")
    await engine.dispose() # Descartar o engine após o uso no script

if __name__ == "__main__":
    # Este bloco permite executar este script diretamente para criar as tabelas.
    # Ex: python -m app.db.init_db
    asyncio.run(main())
