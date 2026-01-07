from fileinput import filename
from fastapi import HTTPException

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import yt_dlp
import os
import platform
import uvicorn
import re
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mymusica.netlify.app", "http://localhost:5173", "https://maarttin.github.io"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
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
        objetivo = f"ytsearch:{url}"
        
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

    if formato == "mp3":
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": ruta,  # ruta donde guardar
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
    else:
        opciones = {
            "format": "bestvideo+bestaudio",
            "merge_output_format": "mp4",  # fuerza salida mp4
            "outtmpl": ruta,
            "postprocessors": [{ "key": "FFmpegVideoConvertor", "preferredformat": "mp4" }]
        }


    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"ytsearch:{url}"

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        # Ruta real del archivo generado 
      #  if "requested_downloads" in info and info["requested_downloads"]:
           # filename = info["requested_downloads"][0]["filepath"] 
       # else: 
           # filename = ydl.prepare_filename(info) 
           # if formato == "mp3": 
               # filename = os.path.splitext(filename)[0] + ".mp3"
               
    if "entries" in info:
        entry = info["entries"][0] 
        if "requested_downloads" in entry and entry["requested_downloads"]: 
            filename = entry["requested_downloads"][0]["filepath"] 
        else: 
            filename = ydl.prepare_filename(entry)
            if formato == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3" 
        real_title = entry.get("title", "cancion")
    else: 
        # URL directa 
        if "requested_downloads" in info and info["requested_downloads"]: 
            filename = info["requested_downloads"][0]["filepath"]
        else:
            filename = ydl.prepare_filename(info)
            if formato == "mp3": 
                filename = os.path.splitext(filename)[0] + ".mp3"
        real_title = info.get("title", "cancion")
                
    print("Archivo real generado:", filename, flush=True)
    print("prepare_filename:", ydl.prepare_filename(info), flush=True)
    print("final filename:", filename, flush=True)

    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="Archivo no generado")
    safe_name = os.path.basename(filename)
    safe_name = safe_name.strip()
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", safe_name)
    return FileResponse(
        filename,
        media_type="audio/mpeg" if formato == "mp3" else "video/mp4",
        filename=f"{real_title}.mp3" if formato == "mp3" else f"{real_title}.mp4"
        #filename=safe_name
    )

if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 8080)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port)