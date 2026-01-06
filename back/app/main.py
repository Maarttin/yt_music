from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import yt_dlp
import os
import platform

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mymusica.netlify.app"],
    
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


@app.get("/information")
def get_video(url: str = Query(..., description="URL video")):
    ydl = {"quiet": True, "skip_download": True}
    if url.startswith("http://") or url.startswith("https://"):
        objetivo = url
    else:
        objetivo = f"ytsearch1:{url}"
        
    with yt_dlp.YoutubeDL(ydl) as ydl:
        try:
            info = ydl.extract_info(objetivo, download=False)
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
    
    if url.startswith("http://") or url.startswith("https://"):
        objetivo = [url]
    else:
        objetivo = [f"ytsearch1:{url}"]
        

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(objetivo[0], download=True) 
        filename = ydl.prepare_filename(info)
        if formato == "mp3": 
            filename = filename.rsplit(".", 1)[0] + ".mp3"
    return FileResponse(filename, media_type="audio/mpeg" if formato=="mp3" else "video/mp4", filename=os.path.basename(filename))


