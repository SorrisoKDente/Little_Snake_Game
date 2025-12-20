# Usa uma imagem Python oficial
FROM python:3.11-slim

# Instala dependências de sistema para o Pygame e áudio
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos (se houver) e instala o pygame
COPY requirements.txt .
RUN pip install --no-cache-dir pygame

# Copia o restante do código do jogo
COPY . .

# Cria o diretório de scores no home do root e dá permissão
# Isso garante que o Python consiga escrever o scores.json
RUN mkdir -p /root/.little_snake_game && chmod 777 /root/.little_snake_game

# Comando para rodar o jogo
CMD ["python", "Main.py"]
