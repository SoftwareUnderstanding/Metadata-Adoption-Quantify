import json
import requests
import os
import time


"""
This script is for answering RQ2
"""
SWH_API_ENDPOINT = "https://archive.softwareheritage.org/api/1/origin/"

token = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhMTMxYTQ1My1hM2IyLTQwMTUtODQ2Ny05MzAyZjk3MTFkOGEifQ.eyJpYXQiOjE3MzI4Mjc4MTgsImp0aSI6IjJjYTNhYzEwLWZkMmItNGFjNy05NmI2LWUzMTk4YjY2ZmZmNSIsImlzcyI6Imh0dHBzOi8vYXV0aC5zb2Z0d2FyZWhlcml0YWdlLm9yZy9hdXRoL3JlYWxtcy9Tb2Z0d2FyZUhlcml0YWdlIiwiYXVkIjoiaHR0cHM6Ly9hdXRoLnNvZnR3YXJlaGVyaXRhZ2Uub3JnL2F1dGgvcmVhbG1zL1NvZnR3YXJlSGVyaXRhZ2UiLCJzdWIiOiI3YjFiMjZmZi03NTYxLTQ1NjEtOGIwOS01ZjUwYTM4YzU4MWUiLCJ0eXAiOiJPZmZsaW5lIiwiYXpwIjoic3doLXdlYiIsInNlc3Npb25fc3RhdGUiOiIyOTE5NGU2My01MGRkLTQyOTItYWYxNi00MzhjNzA0Y2IwOGUiLCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyBwcm9maWxlIGVtYWlsIn0.xH3gFM3CNjlFi0OAO8q_lHVMulnC6493rfbdFuRFuQs"

result = {
        "results": [],
        "summary": {
            "count_in_swh": 0,
            "count_not_in_swh": 0
        },
    }

def check_swh_presence(github_url, token):

    headers = {"Authorization": f"Bearer {token}"}
    full_url = f"{SWH_API_ENDPOINT}{github_url}/get/"

    while True:
        
        try:
            response = requests.get(full_url, headers=headers)
            print(f"Processing {full_url} - Status: {response.status_code}")
            
            if response.status_code == 200:
                return True
            
            elif response.status_code == 404:
                return False
            
            #elif response.status_code == 429:
                #print("Rate limit reached. Waiting for reset...")
                #time.sleep(3600) 

            else:
                print(f"Unexpected status code: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"Error checking URL {github_url}: {e}")
            return False

def rq2(input_file, token, output_file, output_directory):

    try:
        with open(input_file, 'r') as file:
            repositories = json.load(file)
        print(f"Loaded {len(repositories)} repositories from {input_file}")

    except Exception as e:
        print(f"Could not open {input_file}: {e}")
        return

    for repo in repositories:
        github_url = repo.get("githublink")

        if github_url:

            in_swh = check_swh_presence(github_url, token)
            result["results"].append({
                "github_link": github_url,
                "in_swh": in_swh
            })
            
            if in_swh:
                result["summary"]["count_in_swh"] += 1
                print(f"{github_url} is available on SWH")
            else:
                result["summary"]["count_not_in_swh"] += 1

    print(f"Processed repositories. In SWH: {result['summary']['count_in_swh']}, Not in SWH: {result['summary']['count_not_in_swh']}")

    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, output_file)

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    pass
