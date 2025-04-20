# src/config.py
import os

# --- Output Directories ---
# Use absolute paths or paths relative to the project root is often safer
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project Root
BASE_DIR = "." # Or keep relative to where app.py is run if simpler for now

DEMUCS_OUTPUT_DIR = os.path.join(BASE_DIR, "output_demucs")
# NR_OUTPUT_DIR = os.path.join(BASE_DIR, "output_noise_reduced") # Removed
# LOUDNESS_OUTPUT_DIR = os.path.join(BASE_DIR, "output_loudness_normalized") # Removed
YOUTUBE_OUTPUT_DIR = os.path.join(BASE_DIR, "output_youtube")

# --- Default Parameters ---
DEFAULT_TARGET_LUFS = -23.0
DEFAULT_DEMUCS_MODEL = "htdemucs" # Or whichever you prefer
DEFAULT_DEMUCS_STEMS = "vocals" # e.g., 'vocals' for vocals/no_vocals

# --- File Handling ---
TEMP_DIR_BASE = os.path.join(BASE_DIR, ".temp_audio") # For temporary uploaded files

# --- Ensure Directories Exist ---
def ensure_dirs():
    os.makedirs(DEMUCS_OUTPUT_DIR, exist_ok=True)
    # os.makedirs(NR_OUTPUT_DIR, exist_ok=True) # Removed
    # os.makedirs(LOUDNESS_OUTPUT_DIR, exist_ok=True) # Removed
    os.makedirs(YOUTUBE_OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR_BASE, exist_ok=True)