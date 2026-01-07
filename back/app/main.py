from fastapi import HTTPException

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import yt_dlp
import os
import platform
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mymusica.netlify.app", "http://localhost:5173"],
    
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
def download_video(url: str, formato: str):
    ruta = "/tmp/%(title)s.%(ext)s"

    opciones = {
        "format": "bestaudio/best" if formato == "mp3" else "bestvideo+bestaudio/best",
        "outtmpl": ruta,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }] if formato == "mp3" else []
    }

    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"ytsearch1:{url}"

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        real_title = info.get("title", "cancion") 
        ext = "mp3" if formato == "mp3" else info.get("ext", "mp4")
        filename = f"/tmp/{real_title}.{ext}"
        if formato == "mp3":
            filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

    print("Título detectado:", info.get("title"), flush=True)
    print("Archivo generado:", filename, flush=True)

    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="Archivo no generado")

    return FileResponse(
        filename,
        media_type="audio/mpeg" if formato == "mp3" else "video/mp4",
        filename=os.path.basename(filename)
    )

if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 8080)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port)