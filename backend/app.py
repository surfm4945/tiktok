from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

from backend.downloader import download_tiktok_video
from backend.utils import cleanup_old_files, DOWNLOAD_DIR

app = FastAPI(title="TikTok Downloader API")

# Mount static files (Frontend and Downloads)
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
# Serve index.html at root
app.mount("/", StaticFiles(directory="frontend", html=True), name="root")

class URLRequest(BaseModel):
    url: str

def is_valid_tiktok_url(url: str) -> bool:
    """Basic validation to prevent command injection or processing junk URLs."""
    pattern = r"https?://(www\.)?(tiktok\.com|vt\.tiktok\.com)/.*"
    return re.match(pattern, url) is not None

@app.post("/api/download")
async def process_download(request: URLRequest, background_tasks: BackgroundTasks):
    # 1. Trigger background cleanup of old files (SaaS best practice)
    background_tasks.add_task(cleanup_old_files, DOWNLOAD_DIR, max_age_minutes=15)

    # 2. Validate URL
    if not is_valid_tiktok_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid TikTok URL provided.")

    # 3. Process Download
    result = download_tiktok_video(request.url)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail="Failed to process video. It may be private or deleted.")

    return {
        "success": True,
        "file_url": f"/downloads/{result['filename']}",
        "message": "Video processed successfully!"
    }