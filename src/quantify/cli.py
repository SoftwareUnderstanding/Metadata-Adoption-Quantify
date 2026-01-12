import argparse
import sys
import time
import threading
import itertools
import os
import json
from contextlib import contextmanager

from quantify.run_somef import run_somef_on_links
from quantify.rqs_scripts.rq1 import rq1
from quantify.rqs_scripts.rq2 import rq2, token as default_token
from quantify.rqs_scripts.rq3 import rq3, process_versions, save_results as save_results_rq3
from quantify.rqs_scripts.rq4 import rq4
from quantify.rqs_scripts.rq5 import rq5
from quantify.results_rqs.count_results import count_rq1, count_rq2, count_rq3, count_rq4, count_rq5

@contextmanager
def spinner_animation(message="Processing"):
    stop_event = threading.Event()
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    
    def animate():
        while not stop_event.is_set():
            sys.stdout.write(f"\r{message} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f"\r{message} Done!     \n")
        sys.stdout.flush()

    t = threading.Thread(target=animate)
    t.start()
    try:
        yield
    finally:
        stop_event.set()
        t.join()

def get_repo_count(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return len(data)
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return 0

def run_somef(args):
    print(f"Running SoMEF with input file: {args.input}")
    output_dir = args.output_dir
    threshold = args.threshold
    keep_tmp = args.keep_tmp # can be None if empty
    
    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        return

    repo_count = get_repo_count(args.input)
    
    with spinner_animation(f"Running SoMEF on {repo_count} repositories..."):
        # We might want to capture output or just run it
        # run_somef_on_links prints things, which might mess up spinner.
        # But for now we just wrap the call.
        
        # run_somef_on_links arguments: json_file, output_dir, threshold, temp
        # Note: if keep_tmp is None, we pass ignore it or pass empty string?
        # The original script passed it to -kt flag. 
        # If user doesn't provide it, we might want to default to a temp dir
        kt_arg = keep_tmp if keep_tmp else "temp_somef_analysis"
        
        run_somef_on_links(args.input, output_dir, threshold, kt_arg)

def run_rqs(args):
    print("Running RQs analysis...")
    somef_dir = args.somef_dir
    output_dir = args.output_dir
    missing_key = "somef_missing_categories"
    cluster = args.cluster
    
    if not os.path.exists(somef_dir):
        print(f"Error: SoMEF output directory {somef_dir} not found.")
        return
        
    os.makedirs(output_dir, exist_ok=True)

    # RQ1
    with spinner_animation("Running RQ1..."):
        rq1(somef_dir, missing_key, f"analysis_{cluster}_rq1.json", output_dir)
        
    # RQ2
    if args.input_repos:
        with spinner_animation("Running RQ2..."):
            rq2(args.input_repos, default_token, f"analysis_{cluster}_rq2.json", output_dir)
    else:
        print("Skipping RQ2 (needs --input-repos)")

    # RQ3
    with spinner_animation("Running RQ3..."):
        result_rq3 = rq3(somef_dir, missing_key)
        # Assuming process_versions logic handles the result
        consistency = process_versions(somef_dir, result_rq3)
        save_results_rq3(output_dir, result_rq3, consistency, f"class_{cluster}_rq3.json", f"const_{cluster}_rq3.json")

    # RQ4
    with spinner_animation("Running RQ4..."):
        rq4(somef_dir, missing_key, f"analysis_{cluster}_rq4.json", output_dir)

    # RQ5
    with spinner_animation("Running RQ5..."):
        rq5(somef_dir, missing_key, f"analysis_{cluster}_rq5.json", output_dir)

def run_calculate(args):
    print(f"Calculating results using repo list from: {args.input}")
    repo_count = get_repo_count(args.input)
    if repo_count == 0:
        print("Error: No repositories found or file error.")
        return

    results_dir = args.results_dir
    cluster_name = args.cluster # Used for file naming

    os.makedirs(results_dir, exist_ok=True)
    
    # We assume run_rqs saved files in specific names or user points to dir containing them.
    # The original count_results functions expect specific filenames like f"analysis_{cluster}_rq1.json"
    # But run_rqs saved them as "analysis_rq1.json" (without cluster name) or we need to align them.
    
    # If we want to support the original naming convention "analysis_{cluster}_rqX.json",
    # we should probably rename files or adjust count_results to just take filename.
    # But count_results does `os.path.join(dir1, f"analysis_{cluster1}_rq1.json")`.
    
    # So if we used "analysis_rq1.json" in run_rqs, and pass cluster="" (empty), it becomes "analysis__rq1.json" or similar.
    # To avoid breaking changes, let's just ask run_rqs to use the cluster name if provided?
    # But run_rqs logic I wrote above hardcoded filenames.
    
    # Let's adjust run_rqs to take an optional prefix/cluster name!
    # Or simpler: In this calculate step, we create symlinks or we assume the user ran 'rqs' and we know the filenames.
    
    # Actually, the best way is to modify count_results functions to take explicit file path instead of (dir, cluster).
    # But that requires more refactoring.
    
    # Alternative: The user script uses `cluster` string to construct filenames.
    # If I pass `cluster="rq1"` it looks for `analysis_rq1_rq1.json`? No.
    # `analysis_{cluster}_rq1.json`.
    
    # So if I saved files as `analysis_rq1.json`, then `cluster` must be empty string? 
    # file = f"analysis_rq1.json".
    
    # Wait, `count_results` uses f"analysis_{cluster1}_rq1.json".
    # If cluster1 is "", file is "analysis__rq1.json".
    
    # I should update `count_results` input expectation or `run_rqs` output naming.
    # I will stick to one convention. Let's say we use a default cluster name "default" or just update `count_results` logic to look for standard names if cluster not found.
    
    # BETTER: Update `run_rqs` above to use `analysis_default_rq1.json` etc if we want to be safe, 
    # or better yet, assume `analysis_{cluster}_rqX.json` and defaulting cluster to "all" or something.
    
    # I will assume the user has results in `args.rq_results_dir`.
    # AND I will assume the filename format is `analysis_{cluster}_rqX.json`.
    # So I need to know what `cluster` name was used.
    # If `run_rqs` generated them, it generated `analysis_rqX.json`.
    # So for `calculate` to work with `run_rqs` output, I need to match filenames.
    
    # I will modify `run_rqs` to save as `analysis_default_rqX.json` 
    # and `run_calculate` to look for `default` cluster.
    
    print(f"Results: {results_dir}, Cluster: {cluster_name}, Total Repos: {repo_count}")
    
    # RQ1
    # count_rq1 returns (doi, l_num).
    # It expects `dir1` containing `analysis_{cluster}_rq1.json`.
    with spinner_animation("Calculating RQ1 stats..."):
        try:
           doi, _ = count_rq1(args.rq_results_dir, cluster_name, repo_count)
        except Exception as e:
            print(f"Error calculating RQ1: {e}")
            doi = 0 # fall back

    # RQ2 (Needs doi from RQ1 if chaining, but count_rq2 accepts it)
    # count_rq2 expects `dir2` containing `analysis_{cluster}_rq2.json`
    with spinner_animation("Calculating RQ2 stats..."):
        try:
             count_rq2(args.rq_results_dir, cluster_name, doi, repo_count)
        except Exception as e:
            print(f"Error calculating RQ2: {e}")

    # RQ3
    with spinner_animation("Calculating RQ3 stats..."):
        try:
             count_rq3(args.rq_results_dir, cluster_name, repo_count)
        except Exception as e:
            print(f"Error calculating RQ3: {e}")

    # RQ4
    with spinner_animation("Calculating RQ4 stats..."):
        try:
             count_rq4(args.rq_results_dir, cluster_name, repo_count)
        except Exception as e:
            print(f"Error calculating RQ4: {e}")

    # RQ5
    with spinner_animation("Calculating RQ5 stats..."):
        try:
             count_rq5(args.rq_results_dir, cluster_name, repo_count)
        except Exception as e:
            print(f"Error calculating RQ5: {e}")


def main():
    parser = argparse.ArgumentParser(description="Metadata Adoption Quantify CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: somef
    parser_somef = subparsers.add_parser("somef", help="Run SoMEF on a JSON list of repositories")
    parser_somef.add_argument("--input", "-i", required=True, help="Path to JSON file containing list of repositories")
    parser_somef.add_argument("--output-dir", "-o", default="somef_outputs", help="Directory to store SoMEF JSON outputs")
    parser_somef.add_argument("--threshold", "-t", default="0.8", help="Threshold for SoMEF")
    parser_somef.add_argument("--keep-tmp", "-kt", help="Directory to keep temp files (default: temp_somef_analysis)")
    parser_somef.set_defaults(func=run_somef)

    # Command: rqs
    parser_rqs = subparsers.add_parser("rqs", help="Run RQs analysis on SoMEF output")
    parser_rqs.add_argument("--somef-dir", "-s", required=True, help="Directory containing SoMEF output JSON files")
    parser_rqs.add_argument("--input-repos", "-i", help="Path to original JSON list of repositories (Required for RQ2)")
    parser_rqs.add_argument("--output-dir", "-o", default="rq_results", help="Directory to store RQ analysis results")
    parser_rqs.add_argument("--cluster", "-c", default="default", help="Cluster name suffix used in output filenames (default: 'default')")
    parser_rqs.set_defaults(func=run_rqs)

    # Command: calculate
    parser_calculate = subparsers.add_parser("calculate", help="Calculate total results percentages")
    parser_calculate.add_argument("--input", "-i", required=True, help="Path to original JSON list of repositories (to count total repos)")
    parser_calculate.add_argument("--rq-results-dir", "-r", required=True, help="Directory containing RQ analysis output files")
    parser_calculate.add_argument("--results-dir", "-o", default="final_results", help="Directory to store final calculated results")
    parser_calculate.add_argument("--cluster", "-c", default="default", help="Cluster name suffix used in RQ result filenames (default: 'default')")
    parser_calculate.set_defaults(func=run_calculate)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
