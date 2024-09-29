import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

class ObsidianScaffolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Obsidian Vault Scaffolder')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("v""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Introduction
        intro_label = QLabel("Welcome to the Obsidian Vault Scaffolder!")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(intro_label)

        description = QLabel("This utility creates a folder structure for storing LLM 'entities' in your Obsidian Vault.")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        collaboration = QLabel("A collaboration between Daniel Rosehill (danielrosehill.com) and Claude Sonnet 3.5")
        collaboration.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(collaboration)

        repo_link = QLabel('<a href="https://github.com/danielrosehill/Obisidian-For-LLM-Capture">Project Repository</a>')
        repo_link.setOpenExternalLinks(True)
        repo_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(repo_link)

        layout.addSpacing(20)

        # Step 1: Vault Path Selection
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Enter Obsidian vault path")
        path_layout.addWidget(self.path_input)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_button)

        layout.addLayout(path_layout)

        set_path_button = QPushButton("Set Repo Path")
        set_path_button.clicked.connect(self.set_repo_path)
        layout.addWidget(set_path_button)

        layout.addSpacing(20)

        # Step 2: Confirmation and Folder Creation
        self.confirm_label = QLabel("Click 'Create Folders' to proceed with folder creation.")
        self.confirm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.confirm_label)

        create_button = QPushButton("Create Folders")
        create_button.clicked.connect(self.create_folders)
        layout.addWidget(create_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Obsidian Vault")
        if folder:
            self.path_input.setText(folder)

    def set_repo_path(self):
        path = self.path_input.text()
        if os.path.isdir(path):
            self.repo_path = path
            self.confirm_label.setText(f"Path set to: {path}")
        else:
            QMessageBox.warning(self, "Invalid Path", "Please enter a valid directory path.")

    def create_folders(self):
        if not hasattr(self, 'repo_path'):
            QMessageBox.warning(self, "No Path Set", "Please set a repository path first.")
            return

        confirm = QMessageBox.question(self, "Confirm Folder Creation",
                                       f"Are you sure you want to create folders in:\n{self.repo_path}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            folders = [
                "Agents", "Analytics", "Analytics/Reports", "Context", "Context/My-Projects",
                "Context/Work-Info", "Metadata", "Other", "Prompts", "Prompts/Active",
                "Prompts/Archived", "Prompts/Drafts", "Prompts/LLM-Engineered",
                "Prompts/Snippets", "Prompts/Specs", "Reference", "Reference/Articles",
                "Reference/LLM-Research"
            ]

            try:
                for folder in folders:
                    os.makedirs(os.path.join(self.repo_path, folder), exist_ok=True)
                self.status_label.setText("Folders created successfully!")
                self.show_success_message()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        else:
            self.status_label.setText("Folder creation cancelled.")

    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Folders have been created successfully!")
        msg.setInformativeText("Would you like to view the created folder structure?")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            os.startfile(self.repo_path) if sys.platform == "win32" else os.system(f"open {self.repo_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ObsidianScaffolder()
    ex.show()
    sys.exit(app.exec())