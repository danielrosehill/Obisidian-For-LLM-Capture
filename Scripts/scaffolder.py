import os

# Define the base directory for Example-Vault relative to the script location
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Example-Vault'))

# Define the folder structure
folder_structure = {
    'Agents': ['Custom Agents', 'Predefined Agents'],
    'Outputs': ['Generated Outputs', 'Logs', 'Reviews'],
    'Prompts': ['User Prompts', 'System Prompts', 'Templates']
}

# Create the folders
for main_folder, subfolders in folder_structure.items():
    main_folder_path = os.path.join(base_dir, main_folder)
    os.makedirs(main_folder_path, exist_ok=True)  # Create main folder
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(main_folder_path, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)  # Create subfolder

# Verify the created folder structure
created_structure = {}
for main_folder in folder_structure.keys():
    created_structure[main_folder] = os.listdir(os.path.join(base_dir, main_folder))

print(created_structure)

# Create a README file to explain the folder structure and its purpose
readme_content = '''
# Obsidian Vault Structure

This README explains the folder structure of the Obsidian vault for storing prompts and agent configurations.

## Folder Structure

### Agents
- **Custom Agents**: Store your custom agent configurations here.
- **Predefined Agents**: Contains configurations for predefined or common agents.

### Outputs
- **Generated Outputs**: Store the outputs generated by the agents.
- **Logs**: Keep logs related to the operation of agents or processing.
- **Reviews**: Store reviews or evaluations of the outputs.

### Prompts
- **User Prompts**: Contains prompts created by users.
- **System Prompts**: Store system-generated prompts for internal use.
- **Templates**: Keep template prompts that can be reused for different scenarios.

The structure is designed to help organize and manage LLM-related content effectively.
'''

# Write the README content to the file
with open(os.path.join(base_dir, 'README.md'), 'w') as readme_file:
    readme_file.write(readme_content)

print('Folder structure created and README.md generated successfully.')