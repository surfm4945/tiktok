import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_old_files(directory: str, max_age_minutes: int = 15):
    """Deletes files in the directory older than max_age_minutes."""
    if not os.path.exists(directory):
        return

    current_time = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            if file_age > (max_age_minutes * 60):
                try:
                    os.remove(filepath)
                    logger.info(f"Deleted old file: {filename}")
                except Exception as e:
                    logger.error(f"Error deleting file {filename}: {e}")