# app.py
import streamlit as st
import os
# import tempfile
# import shutil # For removing temp directories

# Import from the src package
from src import ui, processing, config, utils, __version__

# --- Initial Setup ---
st.set_page_config(page_title="Audio Processing Suite", layout="wide")
st.title("🎧 Audio Processing Suite")
logger = utils.logger # Use the shared logger
config.ensure_dirs() # Make sure output directories exist at startup

# --- Global State (Optional but can be useful) ---
# Use session state to store temporary file paths across reruns if needed
# Initialize state variables
if 'temp_file_path' not in st.session_state:
    st.session_state.temp_file_path = None


# --- Sidebar Navigation ---
app_mode = ui.display_sidebar()

# --- Display Version in Sidebar (Example Usage) ---
st.sidebar.markdown("---") # Separator
st.sidebar.caption(f"Vocalizer Version: {__version__}") # <--- Use the imported variable

# --- Main App Logic ---

# Use a function to handle the file processing logic cleanly
def handle_file_processing(processor_func, uploaded_file, process_button, results_placeholder, display_results_func, *args):
    temp_input_path = None # Initialize outside try for use in finally
    if uploaded_file and process_button:
        try:
            # Save uploaded file temporarily(now returns path to a single temp file)
            temp_input_path = utils.save_uploaded_file(uploaded_file)
            if temp_input_path:
                st.info(f"Processing: {uploaded_file.name}")
                with st.spinner("Processing audio... Please wait."):
                    result = processor_func(temp_input_path, *args)
                display_results_func(result, results_placeholder)
            else:
                st.error("COuld not prepare uploaded file for processing.")
            # st.session_state.temp_file_path = temp_input_path # Store in state if needed later

        except Exception as e:
            logger.error(f"An error occurred during {processor_func.__name__} processing: {e}", exc_info=True)
            st.error(f"An unexpected error occurred: {e}")
        finally:
            if temp_input_path and os.path.exists(temp_input_path):
                logger.info(f"Attempting to clean up temporary file: {temp_input_path}")
                try:
                    os.remove(temp_input_path)
                    logger.info(f"Successfully removed temporary file: {temp_input_path}")
                except OSError as e:
                    logger.error(f"Error removing temporary file {temp_input_path}: {e}", exc_info=True)
                    st.warning(f"Could not automatically clean up temporary file:{e}.")


# --- Mode Switching ---
if app_mode == "Download Audio from YouTube":
    ui.render_youtube_downloader()

elif app_mode == "Extract Vocals (Demucs)":
    uploaded_file, process_button, results_placeholder = ui.render_demucs_separator()
    # Determine output path for Demucs (can be based on config)
    demucs_out = config.DEMUCS_OUTPUT_DIR
    handle_file_processing(
        processing.separate_audio_with_demucs,
        uploaded_file,
        process_button,
        results_placeholder,
        ui.display_demucs_results,
        demucs_out # Pass output dir as an argument
    )

elif app_mode == "Adaptive Noise Reduction":
    uploaded_file, process_button, results_placeholder = ui.render_noise_reduction()
    # Define output file path
    if uploaded_file:
        handle_file_processing(
            processing.adaptive_noise_reduction,
            uploaded_file,
            process_button,
            results_placeholder,
            ui.display_nr_results
            
        )
    elif process_button: # Handle case where button clicked but no file
        st.warning("Please upload a file first.")


elif app_mode == "Loudness Normalization":
    uploaded_file, target_lufs, process_button, results_placeholder = ui.render_loudness_normalization()
    if uploaded_file:
        handle_file_processing(
            processing.loudness_normalization,
            uploaded_file,
            process_button,
            results_placeholder,
            ui.display_ln_results,
            target_lufs # Pass target LUFS
        )
    elif process_button: # Handle case where button clicked but no file
        st.warning("Please upload a file first.")