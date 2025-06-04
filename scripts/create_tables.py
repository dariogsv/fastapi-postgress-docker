# scripts/create_tables.py
import asyncio
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
# para permitir importações como 'from app.db.init_db import ...'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.db.init_db import main as run_init_db # Importa a função main de init_db

if __name__ == "__main__":
    print("Executando script para criar/verificar tabelas do banco de dados...")
    asyncio.run(run_init_db())
    print("Script de criação/verificação de tabelas finalizado.")
