import yt_dlp
import uuid
import os

DOWNLOAD_DIR = "downloads"

def download_tiktok_video(url: str) -> dict:
    """Downloads the best quality video using yt-dlp."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    file_id = str(uuid.uuid4())
    output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            ext = info_dict.get('ext', 'mp4')
            filename = f"{file_id}.{ext}"
            
            return {
                "success": True,
                "filename": filename,
                "title": info_dict.get('title', 'TikTok Video')
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }