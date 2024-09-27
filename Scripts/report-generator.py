import os
from datetime import datetime

def count_markdown_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                count += 1
    return count

# Define the base directory for Example-Vault
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Example-Vault'))

# Define the folders to check
folders = ['Agents', 'Outputs', 'Prompts']

# Count markdown files in each folder
counts = {}
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    counts[folder] = count_markdown_files(folder_path)

# Create Reports folder if it doesn't exist
reports_folder = os.path.join(base_dir, 'Reports')
os.makedirs(reports_folder, exist_ok=True)

# Generate report content
report_content = f"""# Vault Report {datetime.now().strftime('%d%m%y')}

## Agents
Number of markdown files: {counts['Agents']}

## Outputs
Number of markdown files: {counts['Outputs']}

## Prompts
Number of markdown files: {counts['Prompts']}
"""

# Save the report
report_filename = f"{datetime.now().strftime('%d%m%y')}_vaultreport.md"
report_path = os.path.join(reports_folder, report_filename)
with open(report_path, 'w') as report_file:
    report_file.write(report_content)

print(f"Report generated: {report_path}")