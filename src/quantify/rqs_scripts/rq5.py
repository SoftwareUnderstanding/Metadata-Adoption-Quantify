import os
import json

"""
This script is for answering RQ5
"""

result = {
    "citation": {"bib": 0, "cff": 0, "readme": 0}
}

def rq5(directory, missing_key, output_file, output_directory):

    for file_name in os.listdir(directory):
        
        if file_name.startswith("output_") and file_name.endswith(".json"):
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
    
            missing_categories = data.get(missing_key, [])

            if 'citation' in data and 'citation' not in missing_categories:
                
                for citation in data["citation"]:
                    format_value = citation.get("result", {}).get("format")
                    
                    if format_value == "bibtex":
                        result["citation"]["bib"] += 1
                        break

                    if format_value == "cff":
                        result["citation"]["cff"] += 1
                        break

                    if citation.get("result", {}).get("original_header"):
                        result["citation"]["readme"] += 1
                        break
                    
                    else:
                        result["None"]["count"] += 1

    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, output_file)
    with open(output_file, 'w') as outfile:
        json.dump(result, outfile, indent=4)
    
    print("Successfully extracted the necessary information!")


if __name__ == "__main__":
    pass
