import os
import json

"""
This script is for answering RQ1
"""
def rq1(directory, missing_key, output_file, output_directory):
    result = {
        "citation.cff": {"count": 0},
        "readme_url": {"count": 0},
        "package": {"count": 0, "files": []},
        "authors": {"count": 0, "files": []},
        "contributors": {"count": 0, "files": []},
        "license": {"count": 0},
        "codemeta.json": {"count": 0, "files": []},
        "identifier_extract": {"count": 0, "extracted_values": []},
        "None": {"count": 0}
    }

    package_files = [
        "description", 
        "composer.json", 
        "package.json", 
        "pom.xml", 
        "pyproject.toml", 
        "requirements.txt", 
        "setup.py"
    ]

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

            # Now we check for codemeta.json across all fields with "source" instead of temp_dir
            codemeta_found = False
            for key, value in data.items():
                if key == missing_key or key in missing_categories:
                    continue
                
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            source_value = item.get("source", "")
                            if isinstance(source_value, str) and "codemeta.json" in source_value.lower():
                                result["codemeta.json"]["count"] += 1
                                result["codemeta.json"]["files"].append(file_name)
                                all_keys_missing = False
                                codemeta_found = True
                                break
                
                if codemeta_found:
                    break
            
            # Same thing here we AUTHORS in different formats
            authors_file_found = False
            for key, value in data.items():
                if key == missing_key or key in missing_categories:
                    continue
                
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            source_value = item.get("source", "")
                            if isinstance(source_value, str):
                                source_lower = source_value.lower()
                                if "/authors" in source_lower or "/authors." in source_lower:
                                    if source_lower.endswith("/authors") or "/authors." in source_lower:
                                        result["authors"]["count"] += 1
                                        result["authors"]["files"].append(file_name)
                                        all_keys_missing = False
                                        authors_file_found = True
                                        break
                
                if authors_file_found:
                    break
            
            # Same thing here for package files
            package_found = False
            if 'has_build_file' in data and 'has_build_file' not in missing_categories:
                for build_file in data["has_build_file"]:
                    source_value = build_file.get("result", {}).get("value", "").lower()
                    format_value = build_file.get("result", {}).get("format", "").lower()
                    
                    for pkg_file in package_files:
                        if pkg_file.lower() in source_value or pkg_file.lower() == format_value:
                            if not package_found: 
                                result["package"]["count"] += 1
                                result["package"]["files"].append(file_name)
                                all_keys_missing = False
                                package_found = True
                            break
                    
                    if package_found:
                        break

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