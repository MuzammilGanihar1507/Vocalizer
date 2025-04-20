## Installing FFmpeg (Required Dependency)

Vocalizer relies on **FFmpeg**, a powerful background tool for handling audio and video operations. Several features, especially downloading audio from YouTube and potentially some audio format conversions used by other libraries, require FFmpeg to be installed and accessible on your system.

Please follow the instructions below for your specific operating system.

---

### Windows Installation

The most common way to install FFmpeg on Windows is to download a pre-built version and add it to your system's Environment Variables (specifically the PATH).

1.  **Download FFmpeg:**
    *   Go to the official FFmpeg Builds page: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) (Gyan.dev provides trusted, up-to-date builds).
    *   Look for the latest **release** build (not nightly or git master unless you know you need it).
    *   Download the `ffmpeg-release-full.7z` archive (the full version includes `ffprobe` which is often needed too).

2.  **Extract the Archive:**
    *   You'll need a tool like [7-Zip](https://www.7-zip.org/) (free) or WinRAR to extract `.7z` files.
    *   Extract the contents of the downloaded `.7z` file to a permanent location on your computer where you want to keep FFmpeg. A good simple choice is directly on your `C:` drive, like `C:\ffmpeg`.
    *   After extraction, you should have a folder structure like `C:\ffmpeg\bin`, `C:\ffmpeg\doc`, etc. The important folder is `bin`, which contains `ffmpeg.exe`, `ffprobe.exe`, and `ffplay.exe`.

3.  **Add FFmpeg to the Windows PATH:**
    *   This step makes FFmpeg accessible from any command prompt or terminal window.
    *   Press the `Windows key`, type `Environment Variables`, and click on "Edit the system environment variables".
    *   In the System Properties window that appears, click the "Environment Variables..." button.
    *   In the **System variables** section (bottom half), find the variable named `Path`, select it, and click "Edit...".
    *   Click the "New" button.
    *   Enter the **full path** to the `bin` directory inside the folder where you extracted FFmpeg. Using our example, this would be: `C:\ffmpeg\bin`
    *   Click "OK" on all the windows ("Edit environment variable", "Environment Variables", "System Properties") to save the changes.

4.  **Restart Terminal/IDE:** **Crucial Step!** You must close *any* open Command Prompt, PowerShell, or IDE terminal windows and re-open them for the new PATH changes to take effect.

5.  **Verify Installation:** Open a **new** Command Prompt or PowerShell window and type:
    ```cmd
    ffmpeg -version
    ```
    If FFmpeg is installed correctly and added to the PATH, you should see version information printed without any "command not found" errors.

---

### macOS Installation

The easiest and recommended way to install FFmpeg on macOS is using the [Homebrew](https://brew.sh/) package manager.

1.  **Install Homebrew (if you don't have it):**
    *   Open the **Terminal** application (Applications > Utilities > Terminal).
    *   Paste the following command and press Enter:
        ```bash
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
    *   Follow any on-screen instructions from the Homebrew installer.

2.  **Install FFmpeg:**
    *   Once Homebrew is installed, run the following command in the Terminal:
        ```bash
        brew install ffmpeg
        ```
    *   Homebrew will download and install FFmpeg and its dependencies.

3.  **Verify Installation:** After the installation completes, run:
    ```bash
    ffmpeg -version
    ```
    You should see the FFmpeg version information displayed.

---

### Linux Installation

Installation on Linux typically uses the distribution's package manager.

**1. Debian / Ubuntu / Mint:**

*   Open your terminal.
*   Update your package list and install FFmpeg:
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
*   Enter your password when prompted.

**2. Fedora / CentOS / RHEL (Recent Versions):**

*   Open your terminal.
*   Install FFmpeg:
    ```bash
    sudo dnf install ffmpeg
    ```
*   *Note:* On CentOS/RHEL, you might need to enable the EPEL and RPM Fusion repositories first if FFmpeg isn't found in the default repositories. Search online for instructions specific to your CentOS/RHEL version if needed.

**3. Arch Linux / Manjaro:**

*   Open your terminal.
*   Install FFmpeg:
    ```bash
    sudo pacman -Syu ffmpeg
    ```

**4. Verify Installation (All Linux Distros):**

*   After installation, run:
    ```bash
    ffmpeg -version
    ```
    You should see the FFmpeg version information.

---

Once you have successfully installed FFmpeg using the method for your operating system and verified it with `ffmpeg -version`, Vocalizer should be able to use it correctly for tasks like YouTube audio downloading.