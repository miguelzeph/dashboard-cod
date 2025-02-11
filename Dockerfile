# Use uma imagem base com Python 3.7
FROM python:3.7-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de configuração para o diretório de trabalho
COPY config_dashboard_atlas_nuvem.yml /app/

# Copie o código fonte para o diretório de trabalho
COPY src /app/src

# Copie o arquivo de dependências para o diretório de trabalho
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina as variáveis de ambiente
ENV KLEIN_CONFIG=/app/config_dashboard_atlas_nuvem.yml

# Exponha a porta em que o Flask irá rodar
EXPOSE 5000

WORKDIR /app/src

# Comando para rodar o aplicativo Flask
CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=5000"]
