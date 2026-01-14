import subprocess
import os
import json

def run_somef_on_links(json_file, output_dir, threshold, temp):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    for i, entry in enumerate(data):
        link = entry.get('github_url')
        if link:
            print(f"Extracting: {link}")
            output_file = os.path.join(output_dir, f"output_{i+1}.json")
            command = f"somef describe -r {link} -o {output_file} -t {threshold} -p -m"
            subprocess.run(command, shell=True)


if __name__ == "__main__":
    pass