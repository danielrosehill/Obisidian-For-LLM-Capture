import os
import re

def extract_prompt(content):
    match = re.search(r'# Prompt\n\n(.*?)\n\n# Output', content, re.DOTALL)
    return match.group(1) if match else None

def create_bidirectional_link(prompt_file, output_file):
    with open(prompt_file, 'a') as f:
        f.write(f"\n\n[Output]({os.path.relpath(output_file, os.path.dirname(prompt_file))})")
    
    with open(output_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f"[Prompt]({os.path.relpath(prompt_file, os.path.dirname(output_file))})\n\n{content}")

def process_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(os.path.dirname(script_dir), 'Outputs')
    prompts_dir = os.path.join(os.path.dirname(script_dir), 'Prompts')

    if not os.path.exists(prompts_dir):
        os.makedirs(prompts_dir)

    for filename in os.listdir(outputs_dir):
        if filename.endswith('.md'):
            output_file = os.path.join(outputs_dir, filename)
            with open(output_file, 'r') as f:
                content = f.read()
            
            prompt_text = extract_prompt(content)
            if prompt_text:
                prompt_filename = f"{os.path.splitext(filename)[0]}_prompt.md"
                prompt_file = os.path.join(prompts_dir, prompt_filename)
                
                with open(prompt_file, 'w') as f:
                    f.write(f"# Prompt\n\n{prompt_text}")
                
                create_bidirectional_link(prompt_file, output_file)
                print(f"Processed {filename}")
            else:
                print(f"No prompt found in {filename}")

if __name__ == "__main__":
    process_files()