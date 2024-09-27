import tkinter as tk
from tkinter import filedialog, messagebox
import os

class VaultOutputSaver:
    def __init__(self, master):
        self.master = master
        master.title("Vault Output Saver")
        master.geometry("600x650")
        master.configure(bg="#f0f0f0")

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Title input
        tk.Label(self.master, text="Title:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = tk.Entry(self.master, width=50)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Prompt input
        tk.Label(self.master, text="Prompt:", bg="#f0f0f0").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
        self.prompt_text = tk.Text(self.master, height=10, width=50)
        self.prompt_text.grid(row=1, column=1, padx=10, pady=5)

        # Output input
        tk.Label(self.master, text="Output:", bg="#f0f0f0").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.output_text = tk.Text(self.master, height=10, width=50)
        self.output_text.grid(row=2, column=1, padx=10, pady=5)

        # Save path
        self.save_path = os.getcwd()
        self.save_path_label = tk.Label(self.master, text=f"Save Path: {self.save_path}", bg="#f0f0f0", wraplength=500)
        self.save_path_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Buttons
        self.change_path_button = tk.Button(self.master, text="Change Save Path", command=self.change_save_path)
        self.change_path_button.grid(row=4, column=0, padx=10, pady=5)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_file)
        self.save_button.grid(row=4, column=1, padx=10, pady=5)

    def change_save_path(self):
        new_path = filedialog.askdirectory()
        if new_path:
            self.save_path = new_path
            self.save_path_label.config(text=f"Save Path: {self.save_path}")
            self.save_config()

    def save_file(self):
        title = self.title_entry.get().strip()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        output = self.output_text.get("1.0", tk.END).strip()

        if not title or not prompt or not output:
            messagebox.showerror("Error", "All fields must be filled")
            return

        filename = title.replace(" ", "_") + ".md"
        file_path = os.path.join(self.save_path, filename)

        content = f"# Prompt\n\n{prompt}\n\n# Output\n\n{output}"

        try:
            with open(file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Success", f"File saved successfully: {file_path}")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.prompt_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.txt")
        with open(config_path, "w") as config_file:
            config_file.write(self.save_path)

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.txt")
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                self.save_path = config_file.read().strip()
                self.save_path_label.config(text=f"Save Path: {self.save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VaultOutputSaver(root)
    root.mainloop()