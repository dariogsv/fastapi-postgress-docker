# Usar uma imagem Python oficial como base (escolha a versão desejada)
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
# Isso evita reinstalar tudo se apenas o código mudar, mas requirements.txt não.
COPY requirements.txt .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação vai usar dentro do contêiner
EXPOSE 8000

# O comando para iniciar a aplicação será definido no docker-compose.yml