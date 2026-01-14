import json
import os


def count_rq1(dir1, cluster1, num1):
    json_file_path = os.path.join(dir1, f"analysis_{cluster1}_rq1.json")

    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        return


    with open(json_file_path, "r") as file:
        data = json.load(file)

    rq1 = {
        cluster1: {
            "cff": 0,
            "readme": 0,
            "package": 0,
            "authors": 0,
            "contributors": 0,
            "license": 0,
            "codemeta": 0,
            "zenodo_doi": 0,
            "none": 0
        }
    }

    rq1[cluster1]["cff"] = (data.get("citation.cff", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["readme"] = (data.get("readme_url", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["package"] = (data.get("package", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["authors"] = (data.get("authors", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["contributors"] = (data.get("contributors", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["license"] = (data.get("license", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["codemeta"] = (data.get("codemeta.json", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["zenodo_doi"] = (data.get("identifier_extract", {}).get("count", 0) / num1) * 100
    rq1[cluster1]["none"] = (data.get("None", {}).get("count", 0) / num1) * 100

    results_dir = os.path.join(dir1, "calculations", "rq1")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, f"rq1_results_{cluster1}.json")
    with open(output_file, "w") as outfile:
        json.dump(rq1, outfile, indent=4)

    print(f"RQ1 Results saved to {output_file}")
    
    l_num = data.get("license", {}).get("count")
    doi = rq1[cluster1]["zenodo_doi"]
    return doi, l_num 

def count_rq2(dir2, cluster2, doi, num2):

    json_file_path = os.path.join(dir2, f"analysis_{cluster2}_rq2.json")

    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        return


    with open(json_file_path, "r") as file:
        data = json.load(file)

    rq2 = {cluster2:
        {
            "swh":0,
            "zenodo_doi":0
        }
    }

    rq2[cluster2]["swh"] = (data.get("summary", {}).get("count_in_swh", 0) / num2) * 100
    rq2[cluster2]["zenodo_doi"] = doi

    results_dir = os.path.join(dir2, "calculations", "rq2")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, f"rq2_results_{cluster2}.json")
    with open(output_file, "w") as outfile:
        json.dump(rq2, outfile, indent=4)

    print(f"RQ2 Results saved to {output_file}")
    
def count_rq3(dir3, cluster3, num3):
    json_file_path1 = os.path.join(dir3, f"class_{cluster3}_rq3.json")
    json_file_path2 = os.path.join(dir3, f"const_{cluster3}_rq3.json")

    if not os.path.exists(json_file_path1) or not os.path.exists(json_file_path2):
        print(f"Error: Files do not exist.")
        return

    with open(json_file_path1, "r") as file:
        data1 = json.load(file)
    with open(json_file_path2, "r") as file:
        data2 = json.load(file)

    rq3 = {cluster3:
        {
            "rq3-1": {
                "releases":0,
                "consistency":0
            },

            "rq3-2":{
                "semantic":0,
                "calendar":0,
                "Alphanumeric":0,
                "other":0
            }
        }
    }

    num_r = rq3[cluster3]["rq3-1"]["releases"]
    num_r = (data1.get("releases", {}).get("count", 0))
    print((f"Number of releases are: {num_r}"))
    rq3[cluster3]["rq3-1"]["releases"] = (data1.get("releases", {}).get("count", 0) / num3) * 100
    rq3[cluster3]["rq3-1"]["consistency"] = (data2.get("summary", {}).get("consistent_count", 0) / num_r) * 100

    rq3[cluster3]["rq3-2"]["semantic"] = (data2.get("summary", {}).get("class_counts", {}).get("Semantic", 0) / num_r) * 100
    rq3[cluster3]["rq3-2"]["calendar"] = (data2.get("summary", {}).get("class_counts", {}).get("Calendar", 0) / num_r) * 100
    rq3[cluster3]["rq3-2"]["Alphanumeric"] = (data2.get("summary", {}).get("class_counts", {}).get("Alphanumeric", 0) / num_r) * 100
    rq3[cluster3]["rq3-2"]["other"] = (data2.get("summary", {}).get("class_counts", {}).get("Other", 0) / num_r) * 100

    results_dir = os.path.join(dir3, "calculations", "rq3")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, f"rq3_results_{cluster3}.json")
    with open(output_file, "w") as outfile:
        json.dump(rq3, outfile, indent=4)

    print(f"RQ3 Results saved to {output_file}")

def count_rq4(dir4, cluster4, num4):
    json_file_path = os.path.join(dir4, f"analysis_{cluster4}_rq4.json")

    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        return


    with open(json_file_path, "r") as file:
        data = json.load(file)

    rq4 = {cluster4:
        {
            "rq4-1": {
                "long_desc":0,
                "short_desc":0,
                "None":0
            },

            "rq4-2":{
                "spdx":0,
                "other":0,
                "no_license":0,
            },
            
            "rq4-3":{
                "requirements":0,
                "installation":0,
                "documentation":0,
            }
        }
    }

    rq4[cluster4]["rq4-1"]["long_desc"] = (data.get("description", {}).get("count_long", 0) / num4) * 100
    rq4[cluster4]["rq4-1"]["short_desc"] = (data.get("description", {}).get("count_short", 0) / num4) * 100
    rq4[cluster4]["rq4-1"]["None"] = (data.get("no_description", {}).get("count", 0) / num4) * 100

    rq4[cluster4]["rq4-2"]["spdx"] = (data.get("license", {}).get("spdx", {}).get("count", 0) / num4) * 100
    rq4[cluster4]["rq4-2"]["other"] =  (data.get("license", {}).get("no_spdx", {}).get("count", 0) / num4) * 100
    rq4[cluster4]["rq4-2"]["no_license"] = (data.get("license", {}).get("no_license", {}).get("count", 0) / num4) * 100    

    rq4[cluster4]["rq4-3"]["requirements"] = (data.get("requirements", {}).get("count", 0) / num4) * 100
    rq4[cluster4]["rq4-3"]["installation"] = (data.get("installation", {}).get("count", 0) / num4) * 100
    rq4[cluster4]["rq4-3"]["documentation"] = (data.get("documentation", {}).get("count", 0) / num4) * 100

    results_dir = os.path.join(dir4, "calculations", "rq4")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, f"rq4_results_{cluster4}.json")
    with open(output_file, "w") as outfile:
        json.dump(rq4, outfile, indent=4)

    print(f"RQ4 Results saved to {output_file}")

def count_rq5(dir5, cluster5, num5):

    json_file_path = os.path.join(dir5, f"analysis_{cluster5}_rq5.json")

    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        return

    with open(json_file_path, "r") as file:
        data = json.load(file)

    rq5 = {cluster5:
        {
            "bib":0,
            "cff":0,
            "readme":0,
            "total":0
        }
    }

    rq5[cluster5]["bib"] = (data.get("citation", {}).get("bib", 0) / num5) * 100
    rq5[cluster5]["cff"] = (data.get("citation", {}).get("cff", 0) / num5) * 100
    rq5[cluster5]["readme"] = (data.get("citation", {}).get("readme", 0) / num5) * 100
    rq5[cluster5]["total"] = (rq5[cluster5]["bib"] + rq5[cluster5]["cff"] + rq5[cluster5]["readme"])

    results_dir = os.path.join(dir5, "calculations", "rq5")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, f"rq5_results_{cluster5}.json")
    with open(output_file, "w") as outfile:
        json.dump(rq5, outfile, indent=4)

    print(f"RQ5 Results saved to {output_file}")

if __name__ == "__main__":
    pass
