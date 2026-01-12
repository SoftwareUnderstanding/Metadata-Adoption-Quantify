import os
import json

"""
This script is for answering RQ1
"""
result = {
    "citation.cff": {"count": 0},
    "readme_url": {"count": 0},
    "package": {"count": 0, "files": []},
    "authors": {"count": 0, "files": []},
    "contributors": {"count": 0, "files": []},
    "license": {"count": 0},
    "codemeta.json": {"count": 0, "files": []},
    "zenodo.json": {"count": 0, "files": []},
    "identifier_extract": {"count": 0, "extracted_values": []},
    "None": {"count": 0}
}

def rq1(directory, missing_key, output_file, output_directory):

    for file_name in os.listdir(directory):
        if file_name.startswith("output_") and file_name.endswith(".json"):
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            missing_categories = data.get(missing_key, [])
            all_keys_missing = True

            if 'citation' in data and 'citation' not in missing_categories:
                for citation in data["citation"]:
                    format_value = citation.get("result", {}).get("format")
                    if format_value == "cff":
                        result["citation.cff"]["count"] += 1
                        all_keys_missing = False

            if 'readme_url' in data and 'readme_url' not in missing_categories:
                result['readme_url']['count'] += 1
                all_keys_missing = False

            if 'contributors' in data and 'contributors' not in missing_categories:
                result['contributors']['count'] += 1
                result["contributors"]['files'].append(file_name)
                all_keys_missing = False
            
            if 'license' in data and 'license' not in missing_categories:
                result['license']['count'] += 1
                all_keys_missing = False

            if 'identifier' in data and 'identifier' not in missing_categories:
                for identifier in data["identifier"]:
                    doi_value = identifier.get("result", {}).get("value", "")

                    if doi_value.startswith("https://doi.org/") and "10.5281/zenodo." in doi_value:
                        extracted_part = doi_value.split("https://doi.org/")[-1]
                        result["identifier_extract"]["count"] += 1
                        result["identifier_extract"]["extracted_values"].append(extracted_part)
                        break
                    
                    elif doi_value.startswith("https://zenodo.org/badge/latestdoi/"):
                        extracted_part = doi_value.split("https://zenodo.org/badge/latestdoi/")[-1]
                        result["identifier_extract"]["count"] += 1
                        result["identifier_extract"]["extracted_values"].append(doi_value)
                        break

            if all_keys_missing:
                result['None']['count'] += 1
    
    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, output_file)
    with open(output_path, 'w') as outfile:
        json.dump(result, outfile, indent=4)
    
if __name__ == "__main__":
    pass
