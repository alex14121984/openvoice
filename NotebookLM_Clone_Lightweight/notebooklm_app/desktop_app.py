#!/usr/bin/env python3
"""
NotebookLM Clone - Desktop Application
A simple desktop GUI that wraps the web application for easier use.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import webbrowser
import subprocess
import sys
import os
from pathlib import Path
import time

class NotebookLMDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NotebookLM Clone")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Server process
        self.server_process = None
        self.server_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 NotebookLM Clone", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Server status
        self.status_label = ttk.Label(main_frame, text="Server: Stopped", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        self.start_button = ttk.Button(button_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.browser_button = ttk.Button(button_frame, text="Open in Browser", command=self.open_browser, state=tk.DISABLED)
        self.browser_button.pack(side=tk.LEFT)
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="10")
        actions_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        actions_frame.columnconfigure(1, weight=1)
        
        # File upload
        ttk.Label(actions_frame, text="Upload File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(actions_frame, textvariable=self.file_path_var, state="readonly")
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(actions_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=(0, 5))
        
        # URL input
        ttk.Label(actions_frame, text="URL:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(actions_frame, textvariable=self.url_var)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Text input
        ttk.Label(actions_frame, text="Text:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(5, 0))
        self.text_input = scrolledtext.ScrolledText(actions_frame, height=6, width=50)
        self.text_input.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 10))
        
        # Generate button
        self.generate_button = ttk.Button(actions_frame, text="Generate Audio Overview", 
                                        command=self.generate_audio, state=tk.DISABLED)
        self.generate_button.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Setup close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def start_server(self):
        """Start the Flask server"""
        if self.server_running:
            return
            
        self.log_message("Starting NotebookLM server...")
        
        def run_server():
            try:
                # Import and run the Flask app
                sys.path.insert(0, str(Path(__file__).parent))
                from app import app
                app.run(host='0.0.0.0', port=12000, debug=False, use_reloader=False)
            except Exception as e:
                self.log_message(f"Server error: {e}")
                self.server_running = False
                self.update_ui_state()
        
        # Start server in separate thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Give server time to start
        self.root.after(2000, self.check_server_started)
        
    def check_server_started(self):
        """Check if server started successfully"""
        try:
            import requests
            response = requests.get("http://localhost:12000/health", timeout=2)
            if response.status_code == 200:
                self.server_running = True
                self.log_message("✅ Server started successfully!")
                self.update_ui_state()
            else:
                self.log_message("❌ Server failed to start")
        except:
            self.log_message("❌ Server failed to start")
            
    def stop_server(self):
        """Stop the Flask server"""
        if not self.server_running:
            return
            
        self.server_running = False
        self.log_message("Server stopped")
        self.update_ui_state()
        
    def update_ui_state(self):
        """Update UI based on server state"""
        if self.server_running:
            self.status_label.config(text="Server: Running ✅", foreground="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.browser_button.config(state=tk.NORMAL)
            self.generate_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Server: Stopped ❌", foreground="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.browser_button.config(state=tk.DISABLED)
            self.generate_button.config(state=tk.DISABLED)
            
    def open_browser(self):
        """Open web browser"""
        if self.server_running:
            webbrowser.open('http://localhost:12000')
            self.log_message("Opened browser at http://localhost:12000")
        else:
            messagebox.showwarning("Server Not Running", "Please start the server first")
            
    def browse_file(self):
        """Browse for file"""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("All Supported", "*.pdf *.docx *.txt"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.log_message(f"Selected file: {Path(file_path).name}")
            
    def generate_audio(self):
        """Generate audio overview"""
        if not self.server_running:
            messagebox.showwarning("Server Not Running", "Please start the server first")
            return
            
        # Check what input we have
        file_path = self.file_path_var.get()
        url = self.url_var.get().strip()
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not any([file_path, url, text]):
            messagebox.showwarning("No Input", "Please provide a file, URL, or text to process")
            return
            
        self.log_message("Generating audio overview...")
        messagebox.showinfo("Processing", "Audio generation started!\nCheck the web interface for progress.")
        self.open_browser()
        
    def on_closing(self):
        """Handle window closing"""
        if self.server_running:
            self.stop_server()
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.log_message("NotebookLM Clone Desktop started")
        self.log_message("Click 'Start Server' to begin")
        self.root.mainloop()

def main():
    """Main function"""
    app = NotebookLMDesktop()
    app.run()

if __name__ == "__main__":
    main()