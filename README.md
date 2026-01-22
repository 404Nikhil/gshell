# gsh (Gemini Shell)

A cross-platform CLI assistant that uses Gemini to intelligently execute system operations and shell commands with safety checks.

## Installation & Running

1.  **Install Python Dependency:**
    ```bash
    pip install google-generativeai
    ```

2.  **Setup the Script:**
    * **Mac/Linux:** Save the script as `gsh`, run `chmod +x gsh`, and move it to `/usr/local/bin/`.
    * **Windows:** Save the script as `gsh.py` and add its folder to your System PATH.

3.  **Set API Key:**
    * **Mac/Linux:** `export GEMINI_API_KEY="your_key_here"`
    * **Windows:** `$env:GEMINI_API_KEY="your_key_here"`

4.  **Run:**
    Type `gsh` to start interactive mode or `gsh <command>` for one-off tasks.

## Example Use Cases

1.  **Install Software:** `gsh install vscode and python`
2.  **System Health:** `gsh check my disk usage and memory status`
3.  **Git Automation:** `gsh stage all changes and commit with message "bug fix"`
4.  **File Search:** `gsh find all jpg images modified in the last 24 hours`
5.  **Project Setup:** `gsh create a new folder called "api-service" and initialize a git repo inside it`
6.  **Network Check:** `gsh check my internet connection latency to google.com`
7.  **Process Management:** `gsh find the process id of chrome and kill it`
8.  **Cleanup:** `gsh remove unused docker containers`
9.  **File Manipulation:** `gsh convert all png files in this folder to webp` (requires ffmpeg/magick)
10. **System Update:** `gsh update all my installed packages`