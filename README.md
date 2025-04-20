# 🎧 Vocalizer: Your Simple Audio Processing Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to Vocalizer! This easy-to-use tool helps you perform common audio tasks like downloading songs from YouTube, separating vocals from music, cleaning up background noise, and making audio levels consistent – all through a simple web interface.

<!-- Optional: Add a screenshot of your app here! -->
<!-- ![Vocalizer Screenshot](link/to/your/screenshot.png) -->
<!-- (Replace the line above with an actual link to a screenshot if you have one) -->

## ✨ Features

*   **YouTube Audio Downloader:** Paste a YouTube video link and download just the audio track (usually as an M4A file).
*   **Vocal Extractor (using Demucs):** Upload an audio file (like MP3, WAV, M4A, FLAC) and separate the vocals from the instrumental parts. You can then download both separated tracks.
*   **Adaptive Noise Reduction:** Upload an audio file (works well on extracted vocals!) and automatically reduce background hiss or noise. Download the cleaned-up audio.
*   **Loudness Normalization:** Upload an audio file and adjust its overall volume to a standard level (around -23 LUFS, common for broadcast). Download the normalized audio.

## 📋 Prerequisites

Before you can run Vocalizer, you need a couple of things installed on your computer:

1.  **Python:** This project is built with Python. You'll need a compatible version installed. This project has been developed and tested with **Python 3.12.8**. If you have a different version, you might encounter issues. You can download Python from [python.org](https://www.python.org/).
2.  **FFmpeg:** This is a required background tool needed for several features (like YouTube downloading). Installation varies by operating system.
    *   ➡️ **Please follow the detailed [FFmpeg Installation Guide](INSTALL_FFMPEG.md) for instructions specific to your system.**
    *   **OR** Download it yourself without the guide.            
    *   **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows) and add it to your system's PATH (see instructions online).
    *   **macOS:** The easiest way is using Homebrew: `brew install ffmpeg`
    *   **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
    *   **Linux (Fedora):** `sudo dnf install ffmpeg`

## 🚀 Installation & Setup

Follow these steps to get Vocalizer running on your local machine:

1.  **Get the Code:**
    *   **Option A (Git):** If you have Git installed, open your terminal or command prompt and run:
        ```bash
        git clone https://github.com/MuzammilGanihar1507/Vocalizer.git 
        cd Vocalizer # Or your project's folder name
        ```
    *   **Option B (Download ZIP):** Download the project files as a ZIP and extract them to a folder on your computer. Open your terminal/command prompt and navigate into that folder:
        ```bash
        cd path/to/your/Vocalizer-folder
        ```

2.  **Create a Virtual Environment:** This creates an isolated space for the project's specific required libraries, keeping them separate from other Python projects or your system's global Python. (Make sure you have Python 3.12 available).
    ```bash
    # Use your Python 3.12 executable here
    # Example for Linux/macOS if 'python3.12' command exists:
    python3.12 -m venv venv
    # Example for Windows if Python 3.12 is at C:\Python38:
    # C:\Python312\python.exe -m venv venv
    ```
    *(This creates a folder named `venv` in your project directory.)*

3.  **Activate the Virtual Environment:** You need to activate this environment every time you want to work on or run the project.
    *   **Windows (Command Prompt):**
        ```cmd
        venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```powershell
        # You might need to run this first if you get an error:
        # Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
        venv\Scripts\Activate.ps1
        ```
    *   **macOS / Linux (bash/zsh):**
        ```bash
        source venv/bin/activate
        ```
    *(Your terminal prompt should change, often showing `(venv)` at the beginning.)*

4.  **Install Required Libraries:** While the virtual environment is active, install all the necessary libraries listed in the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
    *(This might take a few minutes as it downloads and installs libraries like Streamlit, Demucs, PyTorch, etc.)*

## ▶️ How to Use Vocalizer

1.  **Activate Environment:** Make sure your virtual environment (`venv`) is activated in your terminal (see Step 3 in Installation if you closed it).
2.  **Run the App:** Navigate to the project directory in your terminal (if you aren't already there) and run:
    ```bash
    streamlit run app.py
    ```
3.  **Open in Browser:** The app should automatically open in your web browser. If not, your terminal will show a local URL like `http://localhost:8501` – just copy and paste that into your browser's address bar.
4.  **Select a Task:** Use the sidebar on the left to choose what you want to do (Download from YouTube, Extract Vocals, etc.).
5.  **Follow On-Screen Instructions:**
    *   For downloading, paste the YouTube link.
    *   For processing, upload your audio file using the "Browse files" button.
    *   Click the relevant button (e.g., "Download Audio", "Extract Vocals", "Apply Noise Reduction").
    *   Wait for the processing to complete (Demucs can take a while!).
    *   The results (audio players and download buttons) will appear on the page. Click the download buttons to save the processed files to your computer.

## ⚙️ Functionality Details

*   **YouTube Audio Downloader:** Takes a standard YouTube video URL and uses `yt-dlp` in the background to fetch and save the best available audio stream, typically as an `.m4a` file in the `output_youtube` folder within your project directory.
*   **Vocal Extractor:** Uses the powerful `Demucs` library (based on AI/Deep Learning) to analyze the uploaded track and separate it into (usually) two files: one containing the vocals and the other containing everything else (instruments, backing track). The results are saved temporarily and offered for direct download via buttons in the app.
*   **Adaptive Noise Reduction:** Analyzes the beginning of the audio file to estimate the background noise profile and then subtracts this noise from the rest of the track. Useful for cleaning up vocals extracted by Demucs or other recordings with steady background hiss. The result is provided directly for download.
*   **Loudness Normalization:** Measures the perceived loudness (using the LUFS standard) of the entire audio file and adjusts the volume so the overall loudness matches a target level (default is -23 LUFS). This helps make different tracks sound consistent in volume. The result is provided directly for download.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file (if you have one) or the [MIT License text](https://opensource.org/licenses/MIT) for details.

## 🙏 Acknowledgements

This tool relies on several fantastic open-source libraries, including:

*   [Streamlit](https://streamlit.io/) (For the web interface)
*   [Demucs](https://github.com/facebookresearch/demucs) (For vocal separation)
*   [yt-dlp](https://github.com/yt-dlp/yt-dlp) (For YouTube downloading)
*   [Librosa](https://librosa.org/) (For audio analysis)
*   [PyLoudnorm](https://github.com/csteinmetz1/pyloudnorm) (For loudness normalization)
*   [SoundFile](https://pysoundfile.readthedocs.io/) (For reading/writing audio files)
*   [PyTorch](https://pytorch.org/) (Required by Demucs)

---

Enjoy using Vocalizer!