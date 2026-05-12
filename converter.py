#!/usr/bin/env python3
"""
Audio to MP3 Converter
A simple GUI application to convert M4A/MP4 audio or video files to MP3.
Requires FFmpeg to be installed and in PATH.
"""

import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import re


class MP4toMP3Converter:
    """Main converter application with Tkinter GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Audio to MP3 Converter")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.input_file = tk.StringVar()
        self.input_files = []
        self.output_folder = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.progress_value = tk.IntVar(value=0)
        self.is_converting = False
        self.cancel_requested = False
        self.process = None
        
        # Check FFmpeg availability
        if not self.check_ffmpeg():
            messagebox.showerror(
                "FFmpeg Not Found",
                "FFmpeg is not installed or not in PATH.\n"
                "Please install FFmpeg to use this converter."
            )
            self.root.destroy()
            return
        
        self.create_widgets()
        
        # Set window position to center
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed and accessible."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Audio to MP3 Converter",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Input file section
        input_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_file,
            state='readonly'
        )
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_input_btn = ttk.Button(
            input_frame,
            text="Browse...",
            command=self.browse_input_file
        )
        browse_input_btn.pack(side=tk.RIGHT)
        
        # Output folder section
        output_frame = ttk.LabelFrame(main_frame, text="Output Folder", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_entry = ttk.Entry(
            output_frame,
            textvariable=self.output_folder,
            state='readonly'
        )
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_output_btn = ttk.Button(
            output_frame,
            text="Browse...",
            command=self.browse_output_folder
        )
        browse_output_btn.pack(side=tk.RIGHT)
        
        # Button frame for convert and cancel
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 10))
        
        # Convert button
        self.convert_btn = ttk.Button(
            button_frame,
            text="CONVERT TO MP3",
            command=self.start_conversion,
            style="Convert.TButton"
        )
        self.convert_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 5))
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            button_frame,
            text="CANCEL",
            command=self.cancel_conversion,
            state='disabled'
        )
        self.cancel_btn.pack(side=tk.LEFT, ipady=8, padx=(5, 0))
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_value,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = ttk.Label(
            progress_frame,
            text="Ready",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(pady=(5, 0))
        
        # Styling
        style = ttk.Style()
        style.configure("Convert.TButton", font=("Segoe UI", 11, "bold"))
    
    def browse_input_file(self):
        """Open file dialog to select input audio/video files."""
        filenames = filedialog.askopenfilenames(
            title="Select audio or video files",
            filetypes=[
                ("Audio/Video Files", "*.m4a *.mp4 *.avi *.mov *.mkv"),
                ("M4A Files", "*.m4a"),
                ("MP4 Files", "*.mp4"),
                ("All Files", "*.*")
            ]
        )
        if filenames:
            self.input_files = list(filenames)
            if len(self.input_files) == 1:
                self.input_file.set(self.input_files[0])
            else:
                self.input_file.set(f"{len(self.input_files)} files selected")
    
    def browse_output_folder(self):
        """Open directory dialog to select output folder."""
        folder = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.output_folder.get()
        )
        if folder:
            self.output_folder.set(folder)
    
    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        if self.is_converting:
            return
        
        input_paths = self.input_files
        output_path = self.output_folder.get()
        
        # Validation
        if not input_paths:
            messagebox.showwarning("No File Selected", "Please select one or more input files.")
            return
        
        for path in input_paths:
            if not os.path.exists(path):
                messagebox.showerror("File Not Found", f"The file does not exist:\n{path}")
                return
        
        if not os.path.isdir(output_path):
            messagebox.showerror("Invalid Folder", f"The output folder does not exist:\n{output_path}")
            return
        
        # Start conversion in thread
        self.is_converting = True
        self.cancel_requested = False
        self.convert_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress_value.set(0)
        self.status_label.config(text="Starting conversion...")
        
        thread = threading.Thread(target=self.convert_file, args=(input_paths, output_path))
        thread.daemon = True
        thread.start()
    
    def convert_file(self, input_paths, output_folder):
        """Convert input files to MP3 using FFmpeg."""
        try:
            total_files = len(input_paths)
            completed_files = 0
            failed_files = []

            for index, input_path in enumerate(input_paths, start=1):
                if self.cancel_requested:
                    break

                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(output_folder, f"{base_name}.mp3")
                counter = 1
                while os.path.exists(output_path):
                    output_path = os.path.join(output_folder, f"{base_name}_{counter}.mp3")
                    counter += 1

                self.root.after(0, lambda idx=index, tot=total_files, name=base_name: self.status_label.config(
                    text=f"Converting {name} ({idx}/{tot})..."
                ))

                cmd = [
                    'ffmpeg',
                    '-i', input_path,
                    '-vn',
                    '-ab', '192k',
                    '-ar', '44100',
                    '-y',
                    output_path
                ]

                self.process = subprocess.Popen(
                    cmd,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    universal_newlines=True
                )

                process = self.process
                duration = None
                file_progress = 0

                while True:
                    line = process.stderr.readline()
                    if not line:
                        break

                    if self.cancel_requested:
                        process.terminate()
                        break

                    if duration is None:
                        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+)\.(\d+)', line)
                        if duration_match:
                            hours = int(duration_match.group(1))
                            minutes = int(duration_match.group(2))
                            seconds = int(duration_match.group(3))
                            duration = hours * 3600 + minutes * 60 + seconds

                    time_match = re.search(r'time=(\d+):(\d+):(\d+)\.(\d+)', line)
                    if time_match and duration:
                        hours = int(time_match.group(1))
                        minutes = int(time_match.group(2))
                        seconds = int(time_match.group(3))
                        current_time = hours * 3600 + minutes * 60 + seconds
                        file_progress = min(int((current_time / duration) * 100), 100)
                        total_progress = min(int(((index - 1) + (file_progress / 100)) / total_files * 100), 100)

                        self.root.after(0, lambda p=total_progress: self.progress_value.set(p))
                        self.root.after(0, lambda p=file_progress, idx=index, tot=total_files: self.status_label.config(
                            text=f"Converting ({idx}/{tot})... {p}%"
                        ))

                process.wait()

                if self.cancel_requested:
                    break

                if process.returncode == 0:
                    completed_files += 1
                    self.root.after(0, lambda p=min(int((completed_files / total_files) * 100), 100): self.progress_value.set(p))
                else:
                    failed_files.append(input_path)
                    failure_name = os.path.basename(input_path)
                    self.root.after(0, lambda name=failure_name: self.status_label.config(text=f"Failed: {name}"))
                    
                    # Continue converting remaining files after a failure
                    continue

            if self.cancel_requested:
                self.root.after(0, lambda: self.status_label.config(text="Conversion cancelled"))
                self.root.after(0, lambda: messagebox.showinfo(
                    "Cancelled",
                    "Conversion was cancelled."
                ))
            elif failed_files:
                self.root.after(0, lambda: self.status_label.config(text="Conversion completed with errors"))
                self.root.after(0, lambda: messagebox.showwarning(
                    "Partial Success",
                    f"Converted {completed_files} of {total_files} files successfully.\n"
                    f"Failed files:\n{chr(10).join(failed_files)}"
                ))
            else:
                self.root.after(0, lambda: self.progress_value.set(100))
                self.root.after(0, lambda: self.status_label.config(text="Conversion complete!"))
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"Converted {completed_files} file{'s' if completed_files != 1 else ''} successfully.\n\nSaved to:\n{output_folder}"
                ))

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error occurred"))
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n{str(e)}"
            ))
        finally:
            self.is_converting = False
            self.cancel_requested = False
            self.root.after(0, lambda: self.convert_btn.config(state='normal'))
            self.root.after(0, lambda: self.cancel_btn.config(state='disabled'))
            self.process = None
    
    def cancel_conversion(self):
        """Cancel the ongoing conversion process."""
        if self.process and self.is_converting:
            self.cancel_requested = True
            self.root.after(0, lambda: self.status_label.config(text="Cancelling..."))
            self.process.terminate()


def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Set app icon (optional, uses default)
    try:
        root.iconbitmap(default=None)
    except:
        pass
    
    app = MP4toMP3Converter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
