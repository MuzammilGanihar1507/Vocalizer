# src/ui.py
import streamlit as st
import os
from src import config, youtube, utils # Import youtube core logic, not UI parts

logger = utils.logger # Use the logger from utils

# --- Common UI Elements ---

def display_file_uploader(label="Upload an audio file", types=["mp3", "wav", "m4a", "flac"], key_suffix=""):
    """Displays a file uploader and returns the uploaded file object."""
    return st.file_uploader(
        label,
        type=types,
        accept_multiple_files=False,
        key=f"file_uploader_{key_suffix}" # Unique key per uploader instance
    )

def display_audio_player_from_file(file_path, title="Audio"):
    """Displays an audio player if the file exists."""
    st.markdown(f"#### {title}")
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes) # format determined automatically usually
             # Add download button
            with open(file_path, "rb") as fp:
                st.download_button(
                    label=f"Download {title}",
                    data=fp,
                    file_name=os.path.basename(file_path), # Sensible default filename
                    mime="audio/wav" # Adjust MIME type if needed
                )
        except Exception as e:
            st.error(f"Could not load audio for '{title}': {e}")
    else:
        st.warning(f"{title} file not found or not generated yet.")


# --- Mode-Specific UI Functions ---

def render_youtube_downloader():
    """Renders the UI for the YouTube Downloader."""
    st.header("Download Audio from YouTube")
    url = st.text_input("YouTube Video URL:", key="yt_url")
    output_dir = st.text_input("Output Directory:", value=config.YOUTUBE_OUTPUT_DIR, key="yt_output_dir")
    # Add a placeholder for status messages or results
    status_placeholder = st.empty()
    download_button = st.button("Download Audio", key="yt_download")

    if download_button and url:
        with st.spinner("Attempting to download..."):
            # Call the CORE youtube download function
            result = youtube.download_audio_yt_dlp(url, output_dir)

        if result['success']:
            status_placeholder.success(f"Success: {result['message']}")
            st.info(f"File likely saved as: {result['file_path']}") # Provide path
            # Optional: Display audio player if path is returned and valid
            if result['file_path']:
                 display_audio_player_from_file(result['file_path'], title="Downloaded Audio")
        else:
            status_placeholder.error(f"Error: {result['message']}")
    elif download_button and not url:
         status_placeholder.warning("Please enter a YouTube URL.")


def render_demucs_separator():
    """Renders the UI for Demucs Vocal Separator."""
    st.header("Extract Vocals (Demucs)")
    uploaded_file = display_file_uploader(key_suffix="demucs")
    # Add options for model, stems later if needed
    process_button = st.button("Extract Vocals", key="demucs_process")
    results_placeholder = st.container() # Use a container for results

    # Return necessary info for app.py to call processing
    return uploaded_file, process_button, results_placeholder


def display_demucs_results(result_data, placeholder):
     """Displays the outcome of Demucs processing."""
     with placeholder: # Display results within the designated container
        if result_data['success']:
            st.success(result_data['message'])
            output_paths = result_data.get('output_paths')
            if output_paths:
                # Use the file-based player for demucs outputs
                display_audio_player_from_file(output_paths.get("vocals"), title="Vocals")
                display_audio_player_from_file(output_paths.get("other"), title="Accompaniment") # Or no_vocals
            else:
                st.warning("Processing successful, but no output file paths returned.")
        else:
            st.error(f"Demucs Error: {result_data.get('message', 'Unkown error')}")


def render_noise_reduction():
    """Renders the UI for Noise Reduction."""
    st.header("Adaptive Noise Reduction")
    uploaded_file = display_file_uploader(types=["wav"], key_suffix="nr", label="Upload vocal audio (WAV)")
    process_button = st.button("Apply Noise Reduction", key="nr_process")
    results_placeholder = st.container()
    return uploaded_file, process_button, results_placeholder

def display_nr_results(result_data, placeholder):
     """Displays the outcome of Noise Reduction processing using audio bytes."""
     with placeholder:
        if result_data.get('success'):
            st.success(result_data.get('message', 'Success!'))
            audio_bytes = result_data.get('audio_bytes')
            if audio_bytes:
                st.markdown("#### Noise Reduced Audio")
                st.audio(audio_bytes, format='audio/wav') # Pass bytes directly
                st.download_button(
                    label="Download Noise Reduced Audio",
                    data= audio_bytes,
                    file_name="noise_reduced_wav",
                    mime="audio/wav"
                )
            else:
                st.warning("Processing successful, but no audio data returned.")
        else:
            st.error(f"Noise Reduction Error: {result_data['message']}")


def render_loudness_normalization():
    """Renders the UI for Loudness Normalization."""
    st.header("Loudness Normalization")
    uploaded_file = display_file_uploader(types=["wav"], key_suffix="ln", label="Upload vocal audio (WAV)")
    target_lufs = st.number_input(
        "Target LUFS:",
        min_value=-70.0, max_value=0.0,
        value=config.DEFAULT_TARGET_LUFS,
        step=0.5,
        key="ln_lufs"
        )
    process_button = st.button("Normalize Loudness", key="ln_process")
    results_placeholder = st.container()
    return uploaded_file, target_lufs, process_button, results_placeholder

def display_ln_results(result_data, placeholder):
     """Displays the outcome of Loudness Normalization using audio bytes."""
     with placeholder:
        if result_data['success']:
            st.success(result_data.get('message', 'Success!'))
            audio_bytes = result_data.get('audio_bytes')
            if audio_bytes:
                st.markdown("#### Normalized Audio")
                st.audio(audio_bytes, format='audio/wav') # Pass bytes directly
                st.download_button(
                    label="Download Normalized Audio",
                    data=audio_bytes, # Pass bytes directly
                    file_name="loudness_normalized.wav", # Provide a filename for download
                    mime="audio/wav"
                )
            else:
                st.warning("Processing successful, but no audio data returned.")
        else:
            st.error(f"Loudness Normalization Error: {result_data.get('message', 'Unknown error')}")


def display_sidebar():
    """Displays the sidebar navigation."""
    st.sidebar.header("Choose a Functionality")
    app_mode = st.sidebar.radio(
        "Select Task",
        [
            "Download Audio from YouTube",
            "Extract Vocals (Demucs)",
            "Adaptive Noise Reduction",
            "Loudness Normalization",
        ],
        key="app_mode_radio"
    )
    st.sidebar.info("Built using Streamlit and Python")
    return app_mode