# Use a imagem oficial do Python 3.8
FROM python:3.8-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config

# Copie o diretório atual para o contêiner
COPY . /app

# Instale as dependências
RUN pip install -r requirements.txt

# Exponha a porta em que seu aplicativo será executado
EXPOSE 8000

# Defina o comando para iniciar seu aplicativo
CMD ["gunicorn", "agenda.wsgi:application", "--bind", "0.0.0.0:8000"]

