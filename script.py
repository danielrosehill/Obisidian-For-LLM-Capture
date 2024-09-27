import os
import re
import glob
import datetime
import json
import tkinter as tk
from tkinter import filedialog, ttk
import configparser
from PIL import Image, ImageTk

class ObsidianLLMVaultRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("Obsidian LLM Vault Script Runner, V1")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.config = configparser.ConfigParser()
        self.config_file = "config.ini"
        self.load_config()

        self.create_widgets()

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

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Add icon (if available)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icon.png")
        if os.path.exists(icon_path):
            try:
                icon_image = Image.open(icon_path)
                icon_image = icon_image.resize((80, 80), Image.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label = ttk.Label(main_frame, image=icon_photo, background="#f0f0f0")
                icon_label.image = icon_photo
                icon_label.grid(column=0, row=0, columnspan=3, pady=(0, 20))
            except Exception as e:
                print(f"Failed to load icon: {e}")
        else:
            print(f"Icon file not found at {icon_path}. Continuing without icon.")

        # Path Configurations
        ttk.Label(main_frame, text="Prompts Path:").grid(column=0, row=1, sticky=tk.W, pady=(0, 5))
        self.prompts_entry = ttk.Entry(main_frame, width=50)
        self.prompts_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.prompts_entry.insert(0, self.config["Paths"]["prompts_path"])
        ttk.Button(main_frame, text="Browse", command=lambda: self.browse_path(self.prompts_entry)).grid(column=2, row=1)

        ttk.Label(main_frame, text="Outputs Path:").grid(column=0, row=2, sticky=tk.W, pady=(0, 5))
        self.outputs_entry = ttk.Entry(main_frame, width=50)
        self.outputs_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), padx=(0, 10))
        self.outputs_entry.insert(0, self.config["Paths"]["outputs_path"])
        ttk.Button(main_frame, text="Browse", command=lambda: self.browse_path(self.outputs_entry)).grid(column=2, row=2)

        ttk.Label(main_frame, text="Agents Path:").grid(column=0, row=3, sticky=tk.W, pady=(0, 5))
        self.agents_entry = ttk.Entry(main_frame, width=50)
        self.agents_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), padx=(0, 10))
        self.agents_entry.insert(0, self.config["Paths"]["agents_path"])
        ttk.Button(main_frame, text="Browse", command=lambda: self.browse_path(self.agents_entry)).grid(column=2, row=3)

        save_button = ttk.Button(main_frame, text="Save Configuration", command=self.save_paths)
        save_button.grid(column=1, row=4, pady=20)

        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(column=0, row=5, columnspan=3, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Extract Prompts", command=self.extract_prompts).grid(column=0, row=0, padx=5)
        ttk.Button(button_frame, text="Fix Filenames", command=self.fix_filenames).grid(column=1, row=0, padx=5)
        ttk.Button(button_frame, text="Generate Report", command=self.generate_report).grid(column=2, row=0, padx=5)

        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, wraplength=650, justify="center").grid(column=0, row=6, columnspan=3, pady=20)

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

    def extract_prompts(self):
        outputs_path = self.config["Paths"]["outputs_path"]
        prompts_path = self.config["Paths"]["prompts_path"]

        if not os.path.exists(outputs_path):
            self.status_var.set(f"Error: Outputs directory not found.")
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

        self.status_var.set(f"Extracted {prompt_count} prompts.")

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

def main():
    root = tk.Tk()
    app = ObsidianLLMVaultRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()