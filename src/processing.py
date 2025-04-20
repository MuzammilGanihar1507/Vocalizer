# src/processing.py
import os
import subprocess
import librosa
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
import logging
import sys
import io
from src import config # Use config for paths and defaults

logger = logging.getLogger(__name__)

# Removed ensure_output_dir, handled by config or calling function


# 1. Extract Vocals using Demucs
def separate_audio_with_demucs(audio_path: str, # audio_path will now be the sanitized path from utils.py
                               output_dir: str = config.DEMUCS_OUTPUT_DIR,
                               model: str = config.DEFAULT_DEMUCS_MODEL,
                               stems: str = config.DEFAULT_DEMUCS_STEMS) -> dict:
    """
    Separates audio using Demucs CLI.
    Uses sanitized input path and forces UTF-8 IO encoding for subprocess robustness.
    Args:
        audio_path: Path to the input audio file.
        output_dir: Directory to save separated stems.
        model: Demucs model name.
        stems: Stem to separate ('vocals' or 'four').

    Returns:
        A dictionary: {'success': bool, 'message': str, 'output_paths': dict | None}
        output_paths might contain {'vocals': path, 'other': path}
    """
    if not os.path.exists(audio_path):
         # Log the path that was attempted
         logger.error(f"Input file not found at expected sanitized path: {audio_path}")
         return {'success': False, 'message': f"Input file not found: {audio_path}", 'output_paths': None}

    os.makedirs(output_dir, exist_ok=True)
    # Use subprocess for better control and error handling than os.system
    cmd = [
        sys.executable, "-m", "demucs", # Or just "demucs" if in PATH 
        "--" + ("two-stems" if stems == "vocals" else "stems"), # Handle two-stems vs --stems
        stems,
        "--out", output_dir,
        "-n", model,
        # Crucially, ensure the audio_path itself is passed correctly.
        # If the path itself contained unexpected encoding issues, that's another layer,
        # but Python 3 generally handles paths well. Let's assume the path string is fine for now
        audio_path
    ]
    logger.info(f"Running Demucs command: {' '.join(cmd)}")

    #--- Creating a modified environment for the subprocess ---
        # this is done to tell python to encode different special characters like '|' to print it on to its standard output/error stream 
        # now we will tell python to use UTF-8 for all encoding and stuff by creating a copy of current environment and adding the PYTHONIOENCODING='utf-8' to it.  
    process_env = os.environ.copy()
    process_env["PYTHONIOENCODING"] = "utf-8"

    try:
        # Use capture_output=True to get stdout/stderr if needed
        # Passing the modified environment using the 'env' argument
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace', env=process_env)
        logger.info("Demucs execution successful.")
        logger.debug(f"Demucs stdout:\n{result.stdout}")

        # --- Determine output paths (This is crucial and depends on Demucs version/settings) ---
        # Assuming default output: output_dir / model_name / filename_without_ext / stem.wav
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        # Note: Demucs output structure can vary. CHECK your actual output.
        # This assumes the common structure like "output_demucs/htdemucs/YourSong/vocals.wav"
        expected_output_subdir = os.path.join(output_dir, model, base_name)

        # Adjust based on the stems you expect
        expected_files = {}
        if stems == "vocals":
            expected_files["vocals"] = os.path.join(expected_output_subdir, "vocals.wav")
            expected_files["other"] = os.path.join(expected_output_subdir, "no_vocals.wav") # Check if it's 'other' or 'no_vocals'
        # Add elif for 'four' stems if needed (drums, bass, other, vocals)

        # Verify files exist
        found_paths = {}
        all_found = True
        for stem_name, file_path in expected_files.items():
            if os.path.exists(file_path):
                found_paths[stem_name] = file_path
                logger.info(f"Found output stem: {file_path}")
            else:
                logger.warning(f"Expected Demucs output file not found: {file_path}")
                all_found = False
                # Attempt fallback? Maybe demucs output structure changed?
                # Could check output_dir directly for .wav files? Risky.

        if not found_paths:
             # If *no* expected files were found, report failure clearly
             logger.error(f"Demucs ran, but no expected output files found in {expected_output_subdir}")
             return {'success': False, 'message': f"Demucs ran, but no output files found in expected location: {expected_output_subdir}. Check logs and Demucs output.", 'output_paths': None}

        return {'success': True, 'message': "Separation complete!", 'output_paths': found_paths}

    except subprocess.CalledProcessError as e:
        logger.error(f"Demucs execution failed with code {e.returncode}", exc_info=False)# exc_info=False as we log stderr below
        # Decode stderr explicitly with utf-8, replacing errors if any occur during decoding
        stderr_decoded = e.stderr # Already decoded if text=True, but using env should fix internal print
        logger.error(f"Demucs stderr:\n{stderr_decoded}")
        return {'success': False, 'message': f"Demucs failed: {e.stderr[:500]}...", 'output_paths': None} # Show part of error
    except Exception as e:
        logger.error(f"An unexpected error occurred during Demucs processing: {e}", exc_info=True)
        return {'success': False, 'message': f"An unexpected error occurred: {e}", 'output_paths': None}


# 2. Adaptive Noise Reduction
def adaptive_noise_reduction(input_file: str) -> dict: #removed output_file parameter
    """ Applies adaptive noise reduction and return audio bytes. """
    logger.info(f"Applying adaptive noise reduction on {input_file}...")
    try:
        if not os.path.exists(input_file):
             raise FileNotFoundError(f"Input file not found: {input_file}")

        y, sr = librosa.load(input_file, sr=None)

        # Simple noise profile from the start (adjust duration if needed)
        noise_duration_sec = 0.5
        if len(y) < int(noise_duration_sec * sr):
             logger.warning("Audio too short for noise profile, using entire clip.")
             noise_profile = y
        else:
             noise_profile = y[:int(noise_duration_sec * sr)]

        # Check for silence in noise profile
        if np.max(np.abs(noise_profile)) < 1e-5:
            logger.warning("Noise profile seems silent. Noise reduction might be ineffective.")
            bytes_io = io.BytesIO()
            # Write original audio to bytes if silent
            sf.write(bytes_io, y, sr, format='WAV') 
            return {'success': True, 'message': 'Noise profile silent, returning original.', 'audio_bytes': bytes_io.getvalue()}


        noise_stft = librosa.stft(noise_profile)
        # Use median instead of mean for potentially better robustness to transients
        noise_magnitude = np.median(np.abs(noise_stft), axis=1)

        vocal_stft = librosa.stft(y)
        vocal_magnitude, phase = librosa.magphase(vocal_stft)

        # Apply subtraction (add a small floor to avoid subtracting too much)
        noise_floor = 0.02 # Adjust this factor
        vocal_magnitude_cleaned = np.maximum(0, vocal_magnitude - noise_magnitude[:, np.newaxis] * (1 + noise_floor) )

        stft_cleaned = vocal_magnitude_cleaned * phase
        y_cleaned = librosa.istft(stft_cleaned, length=len(y)) # Ensure original length

         # --- Write processed audio to bytes ---
        bytes_io = io.BytesIO()
        sf.write(bytes_io, y_cleaned, sr, format='WAV') # Must specify format for BytesIO
        logger.info(f"Adaptive noise reduction complete for {input_file}.")
        return {'success': True, 'message': 'Noise reduction complete!', 'audio_bytes': bytes_io.getvalue()} # Return bytes

    except FileNotFoundError as e:
        logger.error(f"Noise reduction failed: {e}")
        return {'success': False, 'message': str(e), 'audio_bytes': None} # Return None for bytes
    except Exception as e:
        logger.error(f"An error occurred in noise reduction: {e}", exc_info=True)
        return {'success': False, 'message': f"Noise reduction error: {e}", 'output_path': None} # Return None for bytes


# 3. Loudness Normalization
def loudness_normalization(input_file: str, target_lufs: float = config.DEFAULT_TARGET_LUFS) -> dict: # Removed output_file parameter
    """ Normalizes audio loudness to target LUFS and return audio bytes. """
    logger.info(f"Applying loudness normalization ({target_lufs} LUFS) on {input_file}...")
    try:
        if not os.path.exists(input_file):
             raise FileNotFoundError(f"Input file not found: {input_file}")

        y, sr = librosa.load(input_file, sr=None)

        # Check for silence
        if np.max(np.abs(y)) < 1e-5:
             logger.warning("Input audio is silent. Skipping normalization.")
             bytes_io = io.BytesIO()
             sf.write(bytes_io, y, sr, format='WAV') # Write original silent file
             return {'success': True, 'message': 'Input silent, saved original.', 'audio_bytes': bytes_io.getvalue()}

        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(y)

        # Check loudness is valid (not -inf)
        if loudness == -float('inf'):
             logger.warning(f"Could not measure loudness (likely silence). Skipping normalization for {input_file}")
             # Write original audio to bytes if loudness invalid
             bytes_io = io.BytesIO()
             sf.write(bytes_io, y, sr, format='WAV') 
             return {'success': True, 'message': 'Could not measure loudness (silence?), saved original.', 'audio_bytes': bytes_io.getvalue()}

        y_normalized = pyln.normalize.loudness(y, loudness, target_lufs)

        # --- Write processed audio to bytes ---
        bytes_io = io.BytesIO()
        sf.write(bytes_io, y_normalized, sr, format='WAV') # Must specify format for BytesIO
        logger.info(f"Loudness normalization complete for {input_file}.")
        return {'success': True, 'message': 'Loudness normalization complete!', 'audio_bytes': bytes_io.getvalue()} # Return bytes

    except FileNotFoundError as e:
        logger.error(f"Loudness normalization failed: {e}")
        return {'success': False, 'message': str(e), 'audio_bytes': None} # Return None for bytes
    except Exception as e:
        logger.error(f"An error occurred in loudness normalization: {e}", exc_info=True)
        return {'success': False, 'message': f"Loudness normalization error: {e}", 'audio_bytes': None}# Return None for bytes