from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import yt_dlp
import os
import platform

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def obtener_ruta():
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    elif sistema_operativo == "Linux":
        ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    elif sistema_operativo == "Darwin":
        ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        ruta_descargas = "./downloads/"         
        
    return ruta_descargas

downdir = "./downloads/"
@app.get("/information")
def get_video(url: str = Query(..., description="URL video")):
    ydl = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),   
                
            }
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        
@app.get("/download")
def download_video(url: str = Query(..., description="URL video"), formato: str = Query(..., description="Formato de descarga")):
    ruta= os.path.join(obtener_ruta(), "%(title)s.%(ext)s")
    if formato == "mp4":
        opciones = {
            "format": "bestvideo+bestaudio[ext=m4a]/best[ext=mp4]",
            "outtmpl": ruta
        }
    elif formato == "mp3":
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": ruta,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
    else:
        raise ValueError("Formato no soportado")

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])
    return {"status": "ok", "formato": formato}


