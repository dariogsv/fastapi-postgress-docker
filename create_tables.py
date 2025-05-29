from database import engine, Base
import asyncio

async def create_all_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Cuidado: apaga todas as tabelas
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas (se não existiam).")

if __name__ == "__main__":
    asyncio.run(create_all_tables())