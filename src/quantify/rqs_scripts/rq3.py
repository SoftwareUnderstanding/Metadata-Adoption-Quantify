import os
import json
import re

"""
This script is for answering RQ3
"""
result = {
    "releases": {"count": 0, "versions": []},
    "None": {"count": 0}
}

SEMANTIC_PATTERN = r"^v?\d+\.\d+\.\d+(-\w+)?$"
CALENDAR_PATTERN = re.compile(
    r"""
    ^                                
    (?P<year>(\d{4}|\d{2}))          
    ([-._])                          
    (?P<month>(0[1-9]|1[0-2]))      
    ([-._])?                         
    (?P<day_or_minor>(0[1-9]|[1-9]|[1-2][0-9]|3[0-1]))?  
    ([-._])?                         
    (?P<micro>\d+)?                  
    (?P<modifier>                    
        [-._]?(dev|alpha|beta|rc\d*) 
    )?                               
    $
    """,
    re.VERBOSE
)

ALPHANUMERIC_PATTERN = r"^[a-zA-Z0-9._-]+$"

def classify_version(version):
    if re.match(SEMANTIC_PATTERN, version):
        return "Semantic"
    elif re.match(CALENDAR_PATTERN, version):
        return "Calendar"
    elif re.match(ALPHANUMERIC_PATTERN, version):
        return "Alphanumeric"
    else:
        return "Other"

def rq3(directory, missing_key):
    for file_name in os.listdir(directory):
        if file_name.startswith("output_") and file_name.endswith(".json"):
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            missing_categories = data.get(missing_key, [])
            releases_missing = True

            if 'releases' in data and 'releases' not in missing_categories:
                releases = data["releases"]  
                result['releases']['count'] += 1
                releases_missing = False

                tags_list = []
                for release in releases:
                    tag = release.get("result", {}).get("tag", "").lower()
                    if tag: 
                        tags_list.append(tag)
                
                if tags_list:
                    result['releases']['versions'].append({file_name: tags_list})

            if releases_missing:
                result['None']['count'] += 1

    return result

def process_versions(directory, result):
    consistency_results = {
        "files": {},
        "summary": {
            "consistent_count": 0,
            "inconsistent_count": 0,
            "class_counts": {
                "Semantic": 0,
                "Calendar": 0,
                "Alphanumeric": 0,
                "Other": 0
            }
        }
    }
    
    for file_data in result["releases"]["versions"]:
        for file_name, versions in file_data.items():
            classifications = [classify_version(version) for version in versions]
            primary_classification = classifications[0] 
            
            consistency_results["summary"]["class_counts"][primary_classification] += 1

            is_consistent = all(classification == primary_classification for classification in classifications)
            consistency_results["files"][file_name] = {
                "is_consistent": is_consistent,
                "classification": primary_classification if is_consistent else "Inconsistent"
            }

            if is_consistent:
                consistency_results["summary"]["consistent_count"] += 1
            else:
                consistency_results["summary"]["inconsistent_count"] += 1

            file_data[file_name] = [{"version": version, "classification": classification} 
                                    for version, classification in zip(versions, classifications)]
    
    return consistency_results


def save_results(output_directory, result, consistency_results, output_release_class_analysis, output_release_const_analysis):
    os.makedirs(output_directory, exist_ok=True)

    with open(os.path.join(output_directory, output_release_class_analysis), 'w') as f:
        json.dump(result, f, indent=4)

    with open(os.path.join(output_directory, output_release_const_analysis), 'w') as f:
        json.dump(consistency_results, f, indent=4)

    print(f"Results saved to {output_release_class_analysis} and {output_release_const_analysis}")



if __name__ == "__main__":
    pass
