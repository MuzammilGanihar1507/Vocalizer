# src/youtube.py
import yt_dlp
import re
import os
import logging
from src import config # Use config for output path

logger = logging.getLogger(__name__)

# Keep get_yt_vid_id as it is (it's fine)
def get_yt_vid_id(url):
    """ Extracts the video ID from a YouTube URL. """
    # ... (keep existing implementation) ...
    patterns = [
        r'youtu\.be/([a-zA-Z0-9_-]{11})',          # youtu.be format
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # youtube.com format
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',     # youtube.com embed format
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})'          # youtube.com/v format
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Return None or raise specific error for clarity
    logger.warning(f"Could not extract video ID from URL: {url}")
    return None


def download_audio_yt_dlp(video_url: str, output_dir: str = config.YOUTUBE_OUTPUT_DIR) -> dict:
    """
    Downloads the audio of a YouTube video using yt_dlp.

    Args:
        video_url: The URL of the YouTube video.
        output_dir: Directory where the audio file will be saved.

    Returns:
        A dictionary: {'success': bool, 'message': str, 'file_path': str | None}
    """
    final_file_path = None # Keep track of the downloaded file path

    def hook(d):
        nonlocal final_file_path
        if d['status'] == 'finished':
            final_file_path = d['filename']
            logger.info(f"Download complete. File saved to: {final_file_path}")
        # You can add more hooks here for progress reporting if needed later

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'), # Use os.path.join
        'quiet': True, # Suppress yt-dlp stdout unless debugging
        'progress_hooks': [hook], # Use hook to get filename
        'noplaylist': True, # Ensure only single video is downloaded
    }

    logger.info(f"Attempting to download audio from: {video_url}")
    try:
        # Ensure output directory exists just before download
        os.makedirs(output_dir, exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        if final_file_path and os.path.exists(final_file_path):
             return {'success': True, 'message': 'Audio download complete!', 'file_path': final_file_path}
        else:
             # This case might happen if hook didn't capture or file was moved/deleted unexpectedly
             logger.error("Download reported finished, but output file path not found.")
             return {'success': False, 'message': 'Download finished, but file path not found.', 'file_path': None}

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp download error: {e}", exc_info=True)
        return {'success': False, 'message': f"Download Error: {e}", 'file_path': None}
    except Exception as e:
        logger.error(f"An unexpected error occurred during download: {e}", exc_info=True)
        return {'success': False, 'message': f"An unexpected error occurred: {e}", 'file_path': None}

# REMOVE the handle_youtube_operations function entirely from this file.
# It will be recreated in ui.py