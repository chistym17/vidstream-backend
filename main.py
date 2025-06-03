from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
import logging
from typing import Callable
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "87539753467"
ALGORITHM = "HS256"

VIDEOS = {
    "sample1": {"type": "hls", "path": "videos/stream.m3u8"},
    "yt1": {"type": "youtube", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
}

@app.middleware("http")
async def verify_token_middleware(request: Request, call_next: Callable):
    if (request.url.path in ["/get-token", "/", "/docs", "/openapi.json"] or 
        request.url.path.endswith('.ts')): 
        return await call_next(request)

    token = request.query_params.get("token") or request.headers.get("Authorization")
    

    
    if token:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info(f"Token valid for video_id: {data.get('video_id')}")
            logger.info(f"Token expires at: {datetime.fromtimestamp(data.get('exp'))}")
            request.state.token_data = data
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return JSONResponse(
                status_code=401,
                content={"detail": "Token expired"}
            )
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
    else:
        logger.warning("No token provided")
        if request.url.path.startswith("/static/"):
            logger.info("Serving static file without token")
        else:
            return JSONResponse(
                status_code=401,
                content={"detail": "No token provided"}
            )

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request processed in {process_time:.2f} seconds")
    
    return response

@app.get("/get-token")
def get_token(video_id: str):
    if video_id not in VIDEOS:
        raise HTTPException(status_code=404, detail="Video not found")

    payload = {
        "video_id": video_id,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}


@app.get("/stream")
async def stream_video(request: Request):
    video_id = request.state.token_data["video_id"]

    try:
        video_path = "static/sample1/master.m3u8"
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found at path: {video_path}")
            raise HTTPException(status_code=404, detail="Video file not found")

        file_size = os.path.getsize(video_path)

        return FileResponse(
            path=video_path,
            media_type="application/vnd.apple.mpegurl",
            headers={
                "Content-Disposition": "inline",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache",
                "X-Video-ID": video_id,
                "X-Token-Valid": "true"
            }
        )

    except Exception as e:
        logger.error(f"Error serving video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving video: {str(e)}")


@app.get("/")
def root():
    return {"message": "Secure Video Backend Ready"}
