## Setup e configuração do projeto

### Pré-requisitos
Para rodar o projeto, você precisa ter instalado em sua máquina:
- docker

### Instalação e execução
1. Clone o repositório:    git clone https://github.com/dariogsv/fastapi-postgress-docker.git
2. Entre na pasta do projeto: cd fastapi-postgress-docker
3. Copie o arquivo .env.example para .env: cp .env.example .env
4. Configure as variáveis de ambiente no arquivo .env com os valores correspondentes
3. Execute o comando para criar e iniciar a imagem Docker: docker compose -f 'docker-compose.yml' up --build --watch
4. Acesse a aplicação no navegador: http://localhost:8000
5. CTRL+C para parar a execução

** Rotas disponíveis: **
- **API REST**: http://localhost:8000/docs
- **GraphQL**: http://localhost:8000/graphql

### Estrutura de pastas do projeto
```
fastapi-postgress-docker/
├── app/
│   ├── __init__.py             # Torna 'app' um pacote Python
│   ├── main.py                 # Ponto de entrada da aplicação FastAPI, configuração de routers
│   │
│   ├── api/                    # Módulos específicos da API REST
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependências da API (ex: get_current_user, get_db_session)
│   │   └── routers/            # Routers para os endpoints da API
│   │       ├── __init__.py
│   │       ├── auth.py         # Endpoints de autenticação (ex: /token)
│   │       ├── users.py        # Endpoints para usuários
│   │       ├── authors.py      # Endpoints para autores
│   │       └── materials.py    # Endpoints para materiais
│   │
│   ├── core/                   # Lógica principal e configurações da aplicação
│   │   ├── __init__.py
│   │   ├── config.py           # Configurações da aplicação (ex: chaves secretas, URL do banco)
│   │   └── security.py         # Lógica de segurança (hashing de senhas, JWT)
│   │
│   ├── crud/                   # Operações CRUD (Create, Read, Update, Delete)
│   │   ├── __init__.py
│   │   └── crud.py             # Funções CRUD (pode ser dividido por modelo se crescer muito)
│   │
│   ├── db/                     # Módulos relacionados ao banco de dados
│   │   ├── __init__.py
│   │   ├── base_class.py       # Definição da Base declarativa do SQLAlchemy
│   │   ├── database.py         # Engine do SQLAlchemy, SessionLocal
│   │   └── init_db.py          # Função para inicializar o banco (criar tabelas)
│   │
│   ├── graphql/                # Módulos específicos do GraphQL
│   │   ├── __init__.py
│   │   ├── schema.py           # Definição do schema GraphQL (Strawberry)
│   │   └── context.py          # Getter de contexto para GraphQL (se necessário)
│   │
│   ├── models/                 # Modelos ORM do SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py           # Todos os modelos ORM (pode ser dividido por funcionalidade)
│   │
│   └── schemas/                # Schemas Pydantic para validação e serialização
│       ├── __init__.py
│       └── schemas.py          # Todos os schemas Pydantic (pode ser dividido)
│
├── scripts/                    # Scripts utilitários standalone
│   ├── __init__.py
│   └── create_tables.py        # Script para executar a inicialização do banco de dados
│
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py             # Fixtures do Pytest
│   └── ...                     # Arquivos de teste espelhando a estrutura do 'app/'
│
├── .env                        # Arquivo para variáveis de ambiente (não versionado)
├── .gitignore                  # Especifica arquivos ignorados pelo Git
├── README.md                   # Documentação do projeto
└── requirements.txt            # Dependências do projeto
```
