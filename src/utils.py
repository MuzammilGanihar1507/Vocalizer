# src/utils.py
import os
import tempfile
import streamlit as st
import logging
import re
from src import config # Import your config

# Basic Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_filename(filename):
     
     """Removes or replaces characters problematic for command-line or file systems."""
    # Remove characters that cause issues (like the vertical bar)
    # You can add other characters to this list/pattern as needed
     sanitized = re.sub(r'[\|:"*?<>/\\]', '_', filename) # Replace common problematic chars with underscore
    # Optionally, limit length or do other cleaning
    # Remove leading/trailing whitespace just in case
     sanitized = sanitized.strip()
     if not sanitized or sanitized == '.': # Handle case where filename becomes empty
         sanitized = "processed_audio_name"
         logger.debug(f"Sanitized filename: '{filename}' -> '{sanitized}'")
     return sanitized

def save_uploaded_file(uploaded_file) -> str | None:
     
     """Saves an uploaded file to a temporary directory with a sanitized name and returns the path."""
     if uploaded_file is None:
         return None
     try:
        original_name = uploaded_file.name
        sanitized_name = sanitize_filename(original_name)
        # Extract suffix (like .wav, .mp3) from sanitized name for NamedTemporaryFile
        _, suffix = os.path.splitext(sanitized_name)

        # Ensure the base temp directory exists
        os.makedirs(config.TEMP_DIR_BASE, exist_ok=True)

        # --- Use NamedTemporaryFile ---
        # delete=False is important, otherwise it's deleted when 'temp_file' goes out of scope/is closed
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            dir=config.TEMP_DIR_BASE,
            suffix=suffix # Helps tools identify file type
        )
        with temp_file: # Use context manager to ensure it's properly handled
            temp_file.write(uploaded_file.getbuffer())
            file_path = temp_file.name # Get the path
        
        logger.info(f"Uploaded file '{original_name}' saved temporarily as '{os.path.basename(file_path)}' to: {file_path}")
        return file_path # Return the actual path
     except Exception as e:
         logger.error(f"Error saving uploaded file: {e}", exc_info=True)
         st.error(f"Failed to save uploaded file: {e}")
         return None

def clean_temp_directory(file_path: str | None):
    """Removes the temporary directory containing the given file path."""
    if file_path and config.TEMP_DIR_BASE in file_path:
        temp_dir = os.path.dirname(file_path)
        try:
            # Ideally use shutil.rmtree(temp_dir) but be CAREFUL
            # For simplicity, just remove the file if that's all you need
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Removed temporary file: {file_path}")
            # If using mkdtemp, you should remove the directory after processing is fully done
            # shutil.rmtree(temp_dir)
            # logger.info(f"Removed temporary directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary file/directory for {file_path}: {e}")

# You might add functions here later like:
# - get_audio_duration(file_path)
# - validate_audio_file(file_path)