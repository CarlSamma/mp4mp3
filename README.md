# Audio to MP3 Converter

A simple Python GUI app that converts `.m4a` or `.mp4` files to `.mp3` using FFmpeg.

## Features

- Select one or more input audio/video files (`.m4a`, `.mp4`, and other common formats)
- Choose an output folder
- Convert to MP3 with progress display
- Cancel conversion while it is running

## Requirements

- Python 3.7+ installed
- FFmpeg installed and available on `PATH`
- `tkinter` (usually included with standard Python installations)

## Setup

1. Install Python if needed: https://www.python.org/downloads/
2. Install FFmpeg and add it to your system `PATH`.
3. Open a terminal in the project folder:

```powershell
cd "c:\Users\night\OneDrive\Desktop\PROGETTI\MP4MP3 Converter\mp4mp3"
```

## Running the App

```powershell
python converter.py
```

## Usage

1. Click `Browse...` next to the input field and select an `.m4a` or `.mp4` file.
2. Choose an output folder.
3. Click `CONVERT TO MP3`.
4. Wait for the conversion to complete and check the output folder for the `.mp3` file.

## Notes

- The app uses FFmpeg to perform the conversion.
- If an output file already exists, the app automatically saves a unique filename like `filename_1.mp3`.
- The existing implementation supports both audio-only and video inputs for MP3 extraction.

## Troubleshooting

- If you see `FFmpeg Not Found`, verify that FFmpeg is installed and that `ffmpeg` can be run from the terminal.
- If the selected file is not found, ensure the path is valid and the file still exists.
