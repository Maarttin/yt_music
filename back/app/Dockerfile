FROM python:3.13-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y ffmpeg

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar
COPY back/app/requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del backend
COPY back/app/ .

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]