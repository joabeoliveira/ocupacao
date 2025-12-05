# Usa uma imagem Python leve
FROM python:3.9-slim

# Define pasta de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs python
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do app
COPY . .

# Expõe a porta 80 (padrão web)
EXPOSE 80

# Comando para rodar o app (usando gunicorn para produção ou python direto)
# Para simplificar aqui, vamos usar python direto, mas gunicorn é recomendado
CMD ["python", "app.py"]