from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import yt_dlp
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    if formato == "mp4":
        opciones = {
            "format": "bestvideo+bestaudio[ext=m4a]/best[ext=mp4]",
            "outtmpl": "%(title)s.%(ext)s"
        }
    elif formato == "mp3":
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
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


