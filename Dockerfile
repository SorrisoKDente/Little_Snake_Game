FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema para o Pygame 
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto 
COPY . .

# Garante que o container possa escrever o arquivo de score
RUN touch score.json && chmod 666 score.json

CMD ["python", "Main.py"]
