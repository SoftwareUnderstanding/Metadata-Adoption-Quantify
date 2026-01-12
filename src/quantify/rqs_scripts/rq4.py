import os
import json
import re

result = {
    "description": {"count_short": 0, "count_long": 0},
    "no_description": {"count":0},
    "license": {
        "spdx": {"count": 0, "licenses": []},
        "no_spdx": {"count": 0, "licenses": []},
        "no_license":{"count": 0, "files": []}
    },
    "installation": {"count": 0},
    "requirements": {"count": 0},
    "download": {"count": 0},
    "documentation": {"count": 0}
}

def rq4(json_files_directory, missing_key, output_file, output_directory):
    for root, dirs, files in os.walk(json_files_directory):
        for file_name in files:
            if file_name.startswith("output_") and file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)

                with open(file_path, 'r') as file:
                    data = json.load(file)
            
                missing_categories = data.get(missing_key, [])
                spdx_found = False

                if "license" in data:

                    for license_entry in data["license"]:
                        license_result = license_entry.get("result", {})
                        license_name = license_result.get("name", "Unknown License")
                        spdx_id = license_result.get("spdx_id")

                        if spdx_id:
                            result["license"]["spdx"]["count"] += 1
                            result["license"]["spdx"]["licenses"].append({"file": file_name, "name": license_name, "spdx_id": spdx_id})
                            spdx_found = True
                            print(f"Found spdx in {file_name}")
                            break


                    if not spdx_found:
                        result["license"]["no_spdx"]["count"] += 1
                        result["license"]["no_spdx"]["licenses"].append({"file": file_name, "name": license_name})
                        print(f"Did not find spdx in {file_name}")
                
                elif "license" in missing_categories:
                    result["license"]["no_license"]["count"] += 1
                    result["license"]["no_license"]["files"].append({"file": file_name})


                
                if "installation" in data and "installation" not in data.get("somef_missing_categories", []):
                    for tech_type in data["installation"]:
                        if tech_type.get("technique") != "supervised_classification":
                            result["installation"]["count"] += 1
                            print("Found installation!")
                            break

                if "requirements" in data and "requirements" not in data.get("somef_missing_categories", []):
                    result["requirements"]["count"] += 1

                if "download" in data and "download" not in data.get("somef_missing_categories", []):
                    result["download"]["count"] += 1

                if "documentation" in data and "documentation" not in data.get("somef_missing_categories", []):
                    result["documentation"]["count"] += 1

                if "description" in data.get("somef_missing_categories", []):
                    result["no_description"]["count"] += 1

                elif "description" in data:
                    for desc_entry in data["description"]:
                        if desc_entry.get("technique") == "GitHub_API":
                            result["description"]["count_short"] += 1

                        if "README.md" in desc_entry.get("source", ""):
                            result["description"]["count_long"] += 1
                            break

    os.makedirs(output_directory, exist_ok=True)
    with open(os.path.join(output_directory, output_file), 'w') as f:
        json.dump(result, f, indent=4)                        
    
    print("Successfully extracted the necessary information!")


if __name__ == "__main__":
    pass
