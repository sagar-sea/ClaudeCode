"""
Ollama + Claude Code Launcher
A modern UI to automate:
1. Starting Ollama server
2. Selecting and running a model
3. Launching Claude Code with the selected model
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import socket
import os


class OllamaClaudeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama + Claude Code Launcher")
        self.root.geometry("650x800")
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Set dark theme colors
        self.bg_color = "#1e1e2e"
        self.card_bg = "#2a2a3e"
        self.accent_color = "#7c3aed"
        self.success_color = "#22c55e"
        self.warning_color = "#f59e0b"
        self.text_color = "#ffffff"
        self.muted_color = "#9ca3af"

        self.root.configure(bg=self.bg_color)

        # State variables
        self.ollama_process = None
        self.selected_model = tk.StringVar()
        self.server_status = tk.StringVar(value="Not Running")
        self.model_type = tk.StringVar(value="local")

        # Claude Code path
        self.claude_path = r"C:\Users\Sagar\.local\bin\claude.exe"

        # Ollama paths - try to find in common locations
        self.ollama_paths = [
            r"C:\Users\Sagar\AppData\Local\Programs\Ollama\ollama.exe",
            r"C:\Program Files\Ollama\ollama.exe",
            r"C:\Program Files (x86)\Ollama\ollama.exe"
        ]
        self.ollama_cmd = self.find_ollama()

        self.create_scrollable_ui()
        self.refresh_models()
        self.check_initial_status()

    def find_ollama(self):
        """Find Ollama executable in common locations or PATH"""
        # First check if ollama is in PATH
        try:
            subprocess.run(["ollama", "--version"],
                         capture_output=True,
                         creationflags=subprocess.CREATE_NO_WINDOW)
            return "ollama"
        except (FileNotFoundError, subprocess.SubprocessError):
            # Check common installation paths
            for path in self.ollama_paths:
                if os.path.exists(path):
                    return path

            # If not found, return default command and hope for the best
            return "ollama"

    def create_scrollable_ui(self):
        """Create scrollable main UI"""
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Build UI in scrollable frame
        self.build_content(self.scrollable_frame)

        # Update canvas width when window resizes
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Handle window resize"""
        if event.widget == self.root:
            self.canvas.itemconfig(self.canvas.find_all()[0], width=event.width - 20)

    def build_content(self, parent):
        """Build the main content"""
        container = tk.Frame(parent, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=25, pady=20)

        # Title
        title = tk.Label(container, text="🚀 Ollama + Claude Launcher",
                        bg=self.bg_color, fg=self.text_color,
                        font=("Segoe UI", 18, "bold"))
        title.pack(pady=(0, 5))

        subtitle = tk.Label(container, text="Automate your local AI workflow",
                           bg=self.bg_color, fg=self.muted_color,
                           font=("Segoe UI", 10))
        subtitle.pack(pady=(0, 20))

        # Step 1: Server Control
        self.create_step1(container)

        # Step 2: Model Selection
        self.create_step2(container)

        # Step 3: Launch
        self.create_step3(container)

        # Log Area
        self.create_log(container)

    def create_card(self, parent, step_num, title):
        """Create a card with step number and title"""
        card = tk.Frame(parent, bg=self.card_bg, padx=20, pady=15)
        card.pack(fill="x", pady=10)

        # Header row
        header = tk.Frame(card, bg=self.card_bg)
        header.pack(fill="x", pady=(0, 10))

        badge = tk.Label(header, text=f" {step_num} ",
                        bg=self.accent_color, fg="white",
                        font=("Segoe UI", 9, "bold"))
        badge.pack(side="left")

        title_lbl = tk.Label(header, text=title,
                            bg=self.card_bg, fg=self.text_color,
                            font=("Segoe UI", 12, "bold"))
        title_lbl.pack(side="left", padx=10)

        return card

    def create_step1(self, parent):
        """Step 1: Ollama Server"""
        card = self.create_card(parent, "1", "Start Ollama Server")

        # Status
        status_row = tk.Frame(card, bg=self.card_bg)
        status_row.pack(fill="x", pady=5)

        tk.Label(status_row, text="Status:",
                bg=self.card_bg, fg=self.muted_color,
                font=("Segoe UI", 10)).pack(side="left")

        self.status_indicator = tk.Label(status_row, text="⚪",
                                        bg=self.card_bg, fg=self.warning_color,
                                        font=("Segoe UI", 12))
        self.status_indicator.pack(side="left", padx=5)

        self.status_label = tk.Label(status_row, textvariable=self.server_status,
                                    bg=self.card_bg, fg=self.warning_color,
                                    font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side="left")

        # Buttons
        btn_row = tk.Frame(card, bg=self.card_bg)
        btn_row.pack(fill="x", pady=(10, 0))

        self.start_btn = tk.Button(btn_row, text="▶ Start Server",
                                  bg=self.success_color, fg="white",
                                  font=("Segoe UI", 10, "bold"),
                                  relief="flat", cursor="hand2",
                                  command=self.start_ollama_server,
                                  padx=20, pady=8)
        self.start_btn.pack(side="left", padx=(0, 10))

        self.stop_btn = tk.Button(btn_row, text="⏹ Stop Server",
                                 bg="#ef4444", fg="white",
                                 font=("Segoe UI", 10, "bold"),
                                 relief="flat", cursor="hand2",
                                 command=self.stop_ollama_server,
                                 state="disabled",
                                 padx=20, pady=8)
        self.stop_btn.pack(side="left")

    def create_step2(self, parent):
        """Step 2: Model Selection"""
        card = self.create_card(parent, "2", "Select Model")

        # Model type radio buttons
        type_row = tk.Frame(card, bg=self.card_bg)
        type_row.pack(fill="x", pady=5)

        tk.Label(type_row, text="Type:",
                bg=self.card_bg, fg=self.muted_color,
                font=("Segoe UI", 10)).pack(side="left")

        local_rb = tk.Radiobutton(type_row, text="Local",
                                 variable=self.model_type, value="local",
                                 bg=self.card_bg, fg=self.text_color,
                                 selectcolor=self.card_bg,
                                 activebackground=self.card_bg,
                                 font=("Segoe UI", 10),
                                 command=self.refresh_models)
        local_rb.pack(side="left", padx=10)

        cloud_rb = tk.Radiobutton(type_row, text="Cloud",
                                 variable=self.model_type, value="cloud",
                                 bg=self.card_bg, fg=self.text_color,
                                 selectcolor=self.card_bg,
                                 activebackground=self.card_bg,
                                 font=("Segoe UI", 10),
                                 command=self.refresh_models)
        cloud_rb.pack(side="left")

        # Model dropdown
        select_row = tk.Frame(card, bg=self.card_bg)
        select_row.pack(fill="x", pady=10)

        tk.Label(select_row, text="Model:",
                bg=self.card_bg, fg=self.muted_color,
                font=("Segoe UI", 10)).pack(side="left")

        self.model_combo = ttk.Combobox(select_row,
                                       textvariable=self.selected_model,
                                       state="readonly",
                                       width=30,
                                       font=("Segoe UI", 10))
        self.model_combo.pack(side="left", padx=10)

        refresh_btn = tk.Button(select_row, text="🔄 Refresh",
                               bg=self.accent_color, fg="white",
                               font=("Segoe UI", 9),
                               relief="flat", cursor="hand2",
                               command=self.refresh_models,
                               padx=10, pady=3)
        refresh_btn.pack(side="left")

        # Run model button
        run_row = tk.Frame(card, bg=self.card_bg)
        run_row.pack(fill="x", pady=(5, 0))

        self.run_model_btn = tk.Button(run_row, text="🤖 Run Model",
                                      bg="#3b82f6", fg="white",
                                      font=("Segoe UI", 10, "bold"),
                                      relief="flat", cursor="hand2",
                                      command=self.run_model,
                                      padx=20, pady=8)
        self.run_model_btn.pack(side="left")

        self.model_status_lbl = tk.Label(run_row, text="",
                                        bg=self.card_bg, fg=self.muted_color,
                                        font=("Segoe UI", 9))
        self.model_status_lbl.pack(side="left", padx=15)

    def create_step3(self, parent):
        """Step 3: Launch Claude Code"""
        card = self.create_card(parent, "3", "Launch Claude Code")

        tk.Label(card, text="Opens Claude Code with the selected Ollama model",
                bg=self.card_bg, fg=self.muted_color,
                font=("Segoe UI", 10)).pack(anchor="w", pady=5)

        self.launch_btn = tk.Button(card, text="🚀 Launch Claude Code",
                                   bg=self.accent_color, fg="white",
                                   font=("Segoe UI", 12, "bold"),
                                   relief="flat", cursor="hand2",
                                   command=self.launch_claude_code,
                                   padx=30, pady=12)
        self.launch_btn.pack(pady=10)

    def create_log(self, parent):
        """Create activity log"""
        log_frame = tk.Frame(parent, bg=self.bg_color)
        log_frame.pack(fill="both", expand=True, pady=(15, 0))

        tk.Label(log_frame, text="📋 Activity Log",
                bg=self.bg_color, fg=self.text_color,
                font=("Segoe UI", 11, "bold")).pack(anchor="w")

        self.log_text = tk.Text(log_frame, height=8,
                               bg="#0f0f1a", fg="#4ade80",
                               font=("Consolas", 9),
                               relief="flat",
                               wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=8)
        self.log_text.config(state="disabled")

    def log(self, message):
        """Add message to log"""
        self.log_text.config(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def refresh_models(self):
        """Refresh model list"""
        model_type = self.model_type.get()

        if model_type == "local":
            try:
                result = subprocess.run([self.ollama_cmd, "list"],
                                       capture_output=True, text=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise Exception(f"Ollama command failed: {result.stderr}")

                lines = result.stdout.strip().split('\n')[1:]
                models = [line.split()[0] for line in lines if line.strip()]
                self.model_combo['values'] = models
                if models:
                    self.model_combo.set(models[0])
                self.log(f"Found {len(models)} local model(s)")
            except Exception as e:
                self.log(f"Error: {e}")
                self.model_combo['values'] = []
        else:
            cloud_models = [
                "qwen3-coder:480b-cloud",
                "llama3.1:70b-cloud",
                "codellama:70b-cloud",
                "deepseek-coder:33b-cloud"
            ]
            self.model_combo['values'] = cloud_models
            self.model_combo.set(cloud_models[0])
            self.log("Loaded cloud models")

    def is_ollama_running(self):
        """Check if Ollama server is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 11434))
            sock.close()
            return result == 0
        except:
            return False

    def check_initial_status(self):
        """Check server status on startup"""
        if self.is_ollama_running():
            self.update_server_status(True)
            self.log("Ollama server detected - already running")

    def update_server_status(self, running):
        """Update server status UI"""
        if running:
            self.server_status.set("Running")
            self.status_indicator.config(text="🟢", fg=self.success_color)
            self.status_label.config(fg=self.success_color)
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.server_status.set("Not Running")
            self.status_indicator.config(text="⚪", fg=self.warning_color)
            self.status_label.config(fg=self.warning_color)
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

    def start_ollama_server(self):
        """Start Ollama server"""
        if self.is_ollama_running():
            self.update_server_status(True)
            self.log("Server already running")
            return

        def start():
            try:
                self.root.after(0, lambda: self.log("Starting Ollama server..."))
                self.ollama_process = subprocess.Popen(
                    [self.ollama_cmd, "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                for i in range(30):
                    time.sleep(1)
                    if self.is_ollama_running():
                        self.root.after(0, lambda: self.update_server_status(True))
                        self.root.after(0, lambda: self.log("Server started!"))
                        return

                self.root.after(0, lambda: self.log("Timeout waiting for server"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {e}"))

        threading.Thread(target=start, daemon=True).start()

    def stop_ollama_server(self):
        """Stop Ollama server"""
        try:
            subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"],
                          capture_output=True,
                          creationflags=subprocess.CREATE_NO_WINDOW)
            self.update_server_status(False)
            self.log("Server stopped")
        except Exception as e:
            self.log(f"Error: {e}")

    def run_model(self):
        """Run selected model"""
        model = self.selected_model.get()
        if not model:
            messagebox.showwarning("Warning", "Select a model first")
            return

        if not self.is_ollama_running():
            messagebox.showwarning("Warning", "Start Ollama server first")
            return

        def run():
            try:
                self.root.after(0, lambda: self.model_status_lbl.config(text="Loading...", fg=self.warning_color))
                self.root.after(0, lambda: self.log(f"Loading model: {model}"))

                subprocess.Popen(
                    ["cmd", "/c", "start", "cmd", "/k", f"{self.ollama_cmd} run {model}"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                time.sleep(3)
                self.root.after(0, lambda: self.model_status_lbl.config(text=f"✓ {model} running", fg=self.success_color))
                self.root.after(0, lambda: self.log(f"Model running: {model}"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {e}"))

        threading.Thread(target=run, daemon=True).start()

    def launch_claude_code(self):
        """Launch Claude Code"""
        model = self.selected_model.get()
        if not model:
            messagebox.showwarning("Warning", "Select a model first")
            return

        if not self.is_ollama_running():
            if messagebox.askyesno("Server Not Running", "Start Ollama server now?"):
                self.start_ollama_server()
                time.sleep(3)
            else:
                return

        # Working directory for Claude Code
        claude_workdir = r"C:\Users\Sagar\ClaudeCode"

        # Create directory if it doesn't exist
        import os
        if not os.path.exists(claude_workdir):
            os.makedirs(claude_workdir)
            self.log(f"Created directory: {claude_workdir}")

        try:
            # Check if Claude Code exists
            if not os.path.exists(self.claude_path):
                raise FileNotFoundError(f"Claude Code not found at {self.claude_path}")

            self.log(f"Launching Claude Code with: {model}")
            self.log(f"Working directory: {claude_workdir}")
            subprocess.Popen(
                [self.claude_path, "--model", model],
                cwd=claude_workdir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.log("Claude Code launched!")
            messagebox.showinfo("Success", f"Claude Code launched with:\n{model}\n\nWorking directory:\n{claude_workdir}")
        except FileNotFoundError as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"Claude Code not found:\n{self.claude_path}\n\nPlease check the path in the script.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()

    # Center on screen
    width, height = 650, 800
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

    app = OllamaClaudeLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()