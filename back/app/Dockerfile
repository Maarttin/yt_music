FROM python:3.11-slim

# Instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -U yt-dlp


# Copiar tu código
COPY . .

#CMD ["uvicorn", "back.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python", "back/app/main.py"]
