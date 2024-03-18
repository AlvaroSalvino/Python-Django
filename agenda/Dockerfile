# Use uma imagem base do Python
FROM python:3.8-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências
RUN pip install -r requirements.txt

# Exponha a porta em que seu aplicativo será executado
EXPOSE 8000

# Defina o comando para iniciar seu aplicativo
CMD ["gunicorn", "agenda.wsgi:application", "--bind", "0.0.0.0:8000"]
