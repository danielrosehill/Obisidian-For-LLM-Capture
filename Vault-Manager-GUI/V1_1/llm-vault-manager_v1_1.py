import os
import sys
import re
import glob
import datetime
import json
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
import configparser
from PIL import ImageTk
import io
import threading

class RedirectText(io.StringIO):
    def __init__(self, text_widget):
        self.text_widget = text_widget
        super().__init__()

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

class ObsidianLLMVaultRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("Obsidian LLM Vault Script Runner, V1")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.config = configparser.ConfigParser()
        self.config_file = "config.ini"
        self.load_config()

        self.main_frame = None  # Initialize main_frame as None
        self.create_widgets()
        self.setup_theme()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config["Paths"] = {
                "prompts_path": "",
                "outputs_path": "",
                "agents_path": ""
            }

    def save_config(self):
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def setup_theme(self):
        self.is_dark_mode = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.main_frame, text="Dark Mode", variable=self.is_dark_mode, command=self.toggle_theme).grid(column=2, row=3, sticky=tk.E)

    def toggle_theme(self):
        if self.is_dark_mode.get():
            self.root.tk_setPalette(background='#2d2d2d', foreground='white')
        else:
            self.root.tk_setPalette(background='#f0f0f0', foreground='black')

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TEntry", padding=5)



        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)

        self.root.rowconfigure(0, weight=1)
        # Path Configurations
        paths_frame = ttk.LabelFrame(self.main_frame, text="Path Configurations", padding="10")
        paths_frame.grid(column=0, row=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        paths_frame.columnconfigure(1, weight=1)

        ttk.Label(paths_frame, text="Prompts Path:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.prompts_entry = ttk.Entry(paths_frame, width=50)
        self.prompts_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.prompts_entry.insert(0, self.config["Paths"]["prompts_path"])
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.prompts_entry)).grid(column=2, row=0, padx=5, pady=(0, 5))
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.prompts_entry)).grid(column=2, row=0, padx=5, pady=(0, 5))
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.prompts_entry)).grid(column=2, row=0, padx=5)

        ttk.Label(paths_frame, text="Outputs Path:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.outputs_entry = ttk.Entry(paths_frame, width=50)
        self.outputs_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.outputs_entry.insert(0, self.config["Paths"]["outputs_path"])
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.outputs_entry)).grid(column=2, row=1, padx=5, pady=(0, 5))
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.outputs_entry)).grid(column=2, row=1, padx=5)

        ttk.Label(paths_frame, text="Agents Path:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.agents_entry = ttk.Entry(paths_frame, width=50)
        self.agents_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), padx=(0, 10))
        self.agents_entry.insert(0, self.config["Paths"]["agents_path"])
        ttk.Button(paths_frame, text="Browse", command=lambda: self.browse_path(self.agents_entry)).grid(column=2, row=2, padx=5)

        ttk.Button(paths_frame, text="Save Configuration", command=self.save_paths).grid(column=1, row=3, pady=(10, 0))

        ttk.Button(paths_frame, text="Save Configuration", command=self.save_paths).grid(column=1, row=3, pady=(10, 0))

        # Action Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(column=0, row=1, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Extract Prompts", command=self.extract_prompts).grid(column=0, row=0, padx=5)
        ttk.Button(button_frame, text="Fix Filenames", command=self.fix_filenames).grid(column=1, row=0, padx=5)
        ttk.Button(button_frame, text="Generate Report", command=self.generate_report).grid(column=2, row=0, padx=5)
        ttk.Button(button_frame, text="Clear Terminal", command=self.clear_terminal).grid(column=3, row=0, padx=5)

        # Terminal Output
        terminal_frame = ttk.LabelFrame(self.main_frame, text="Terminal Output", padding="10")
        terminal_frame.grid(column=0, row=2, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        terminal_frame.columnconfigure(0, weight=1)
        terminal_frame.rowconfigure(0, weight=1)

        self.terminal_output = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, width=80, height=10)
        self.terminal_output.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Redirect stdout to the terminal output
        sys.stdout = RedirectText(self.terminal_output)

        # Status
        self.status_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status_var, wraplength=750, justify="center").grid(column=0, row=3, columnspan=3, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def clear_terminal(self):
        self.terminal_output.delete(1.0, tk.END)

    def browse_path(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_path)

    def save_paths(self):
        self.config["Paths"]["prompts_path"] = self.prompts_entry.get()
        self.config["Paths"]["outputs_path"] = self.outputs_entry.get()
        self.config["Paths"]["agents_path"] = self.agents_entry.get()
        self.save_config()
        self.status_var.set("Configuration saved successfully.")
        print("Configuration saved successfully.")

    def extract_prompts(self):
        if not self.validate_paths():
            return
        threading.Thread(target=self._extract_prompts).start()

    def _extract_prompts(self):
        outputs_path = self.config["Paths"]["outputs_path"]
        prompts_path = self.config["Paths"]["prompts_path"]

        if not os.path.exists(outputs_path):
            self.root.after(0, lambda: self.status_var.set("Error: Outputs directory not found."))
            print("Error: Outputs directory not found.")
            return

        os.makedirs(prompts_path, exist_ok=True)

        prompt_count = 0
        for filename in os.listdir(outputs_path):
            if filename.endswith('.md'):
                input_path = os.path.join(outputs_path, filename)
                output_path = os.path.join(prompts_path, filename)

                with open(input_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()

                prompts = re.findall(r'(?:^|\n)(#+\s*Prompt\s*\d*\s*\n[\s\S]*?)(?=\n#+|$)', content, re.MULTILINE)

                if prompts:
                    with open(output_path, 'w', encoding='utf-8') as outfile:
                        for prompt in prompts:
                            outfile.write(prompt.strip() + '\n\n')
                    prompt_count += len(prompts)

        self.root.after(0, lambda: self.status_var.set(f"Extracted {prompt_count} prompts."))

    def validate_paths(self):
        paths = [self.prompts_entry.get(), self.outputs_entry.get(), self.agents_entry.get()]
        for path in paths:
            if not os.path.exists(path):
                messagebox.showerror("Error", f"Path does not exist: {path}")
                return False
        return True

    def fix_filenames(self):
        paths = [self.config["Paths"]["prompts_path"], 
                 self.config["Paths"]["outputs_path"], 
                 self.config["Paths"]["agents_path"]]

        def sanitize_filename(filename):
            invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
            return re.sub(invalid_chars, '_', filename)

        rename_count = 0
        for path in paths:
            if not os.path.exists(path):
                continue
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    new_filename = sanitize_filename(filename)
                    if new_filename != filename:
                        old_file_path = os.path.join(dirpath, filename)
                        new_file_path = os.path.join(dirpath, new_filename)
                        os.rename(old_file_path, new_file_path)
                        rename_count += 1

        self.status_var.set(f"Renamed {rename_count} files.")
        print(f"Renamed {rename_count} files.")

    def generate_report(self):
        prompts_path = self.config["Paths"]["prompts_path"]
        outputs_path = self.config["Paths"]["outputs_path"]
        agents_path = self.config["Paths"]["agents_path"]
        
        reports_path = os.path.join(outputs_path, 'Reports')
        metrics_file = os.path.join(reports_path, 'last_metrics.json')

        os.makedirs(reports_path, exist_ok=True)

        current_time = datetime.datetime.now().strftime('%d_%m_%y_%H%M')
        report_name = f"{current_time}_report.md"
        report_path = os.path.join(reports_path, report_name)

        def count_markdown_files(directory):
            return len([file for file in glob.iglob(f'{directory}/**/*.md', recursive=True)])

        def gather_markdown_files(directory):
            return [file for file in glob.iglob(f'{directory}/**/*.md', recursive=True)]

        num_agents_docs = count_markdown_files(agents_path)
        outputs_files = gather_markdown_files(outputs_path)
        num_outputs_docs = len(outputs_files)
        total_words_in_outputs = sum(len(open(f, 'r', encoding='utf-8').read().split()) for f in outputs_files)
        num_prompts_docs = count_markdown_files(prompts_path)
        total_entities = num_agents_docs + num_outputs_docs + num_prompts_docs

        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                previous_metrics = json.load(f)
        else:
            previous_metrics = {
                "num_agents_docs": 0,
                "num_outputs_docs": 0,
                "total_words_in_outputs": 0,
                "num_prompts_docs": 0,
                "total_entities": 0
            }

        new_agents_docs = num_agents_docs - previous_metrics["num_agents_docs"]
        new_outputs_docs = num_outputs_docs - previous_metrics["num_outputs_docs"]
        new_words_in_outputs = total_words_in_outputs - previous_metrics["total_words_in_outputs"]
        new_prompts_docs = num_prompts_docs - previous_metrics["num_prompts_docs"]
        new_entities = total_entities - previous_metrics["total_entities"]

        report_content = f"""
# Vault Inventory Report

**Date:** {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}

## Agents Folder
- Number of documents: {num_agents_docs} (New: {new_agents_docs})

## Outputs Folder
- Number of documents: {num_outputs_docs} (New: {new_outputs_docs})
- Total word count: {total_words_in_outputs} (New: {new_words_in_outputs})

## Prompts Folder
- Number of documents: {num_prompts_docs} (New: {new_prompts_docs})

## Total Entities in System
- Total: {total_entities} (New: {new_entities})
"""

        with open(report_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report_content)

        with open(metrics_file, 'w') as f:
            json.dump({
                "num_agents_docs": num_agents_docs,
                "num_outputs_docs": num_outputs_docs,
                "total_words_in_outputs": total_words_in_outputs,
                "num_prompts_docs": num_prompts_docs,
                "total_entities": total_entities
            }, f)

        self.status_var.set(f"Report generated: {report_path}")
        print(f"Report generated: {report_path}")

def main():
    root = tk.Tk()
    ObsidianLLMVaultRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()