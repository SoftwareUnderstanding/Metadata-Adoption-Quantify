[![DOI](https://zenodo.org/badge/878193479.svg)](https://doi.org/10.5281/zenodo.14803005)

> [!WARNING]
> This is still in progress and subject to change, as additional requirements may arise.

# Metadata-Adoption-Quantify

This software extracts relevant data from SOMEF (Software Metadata Extraction Framework) results to answer specific research questions. The extracted insights are returned as structured JSON files, allowing easy integration and analysis.

## Table of Contents

- [Metadata-Adoption-Quantify](#metadata-adoption-quantify)
  - [Table of Contents](#table-of-contents)
  - [About the Software](#about-the-software)
  - [Research Questions](#research-questions)
  - [Features](#features)
  - [Installation](#installation)
  - [Output](#output)

## About the Software

This tool is designed to process metadata extracted using SOMEF, focusing on answering predefined research questions. It parses the data from SOMEF's output and generates JSON files with the information relevant to each research question (RQ) and generating calculations for each data requested.

## Research Questions

This software is tailored to answer the following research questions:

1. RQ1: How do communities describe Research Software metadata in their code repositories?
2. RQ2: What is the adoption of archival infrastructures across the disciplines?
3. RQ3: How do software projects adopt versioning?
4. RQ4: How comprehensive is the metadata provided in code repositories?
5. RQ5: What are the most common citation practices among the communities?

## Features

- Extract metadata from repositories using SOMEF.
- Extracts and processes metadata from SOMEF results.
- Filters information relevant to specific research questions.
- Outputs the results as structured JSON files for easy review and further analysis.
- **Custom Loading Animation**: Visual feedback during processing.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and requires Python 3.10

1. Clone this repository:

   ```bash
   git clone https://github.com/Anas-Elhounsri/Metadata-Adoption-Quantify.git
   cd Metadata-Adoption-Quantify
   ```

2. Install the package and its dependencies:

   ```bash
   poetry install
   ```

3. Set up SoMEF where you will be prompted to enter your GitHub authentication token optionally if you wish to have more rate limit per hour. More information can be found [here](https://github.com/KnowledgeCaptureAndDiscovery/somef)

   ```bash
   somef configure
   ```

## Usage

The tool is accessible via the `quantify` command. All commands should be prefixed with `poetry run` if you are not in the poetry shell.

### Available Commands

#### 1. Run SoMEF on Repositories

Extracts metadata from a list of GitHub repositories provided in a JSON file.

```bash
poetry run quantify somef --input repos.json --output-dir somef_outputs --threshold 0.8
```

#### 2. Run RQ Analysis

Analyzes SoMEF outputs to answer specific research questions.

```bash
poetry run quantify rqs --somef-dir somef_outputs --input-repos repos.json --output-dir rq_results --cluster default
```

_Note: `--input-repos` is required for RQ2 analysis._

The input (in the case of the example that would be `repos.json`) should be a JSON file with the following format:

```json
[
  {
    "github_url": "https://github.com/foo/bar"
  },
  {
    "github_url": "https://github.com/dgarijo/Widoco/"
  }
]
```

#### 3. Calculate Final Results

Calculates the final percentages and insights for each RQ.

```bash
poetry run quantify calculate --input repos.json --rq-results-dir rq_results --results-dir final_results --cluster default
```

### Main Menu (Alternative)

You can still access help for any command by running:

```bash
poetry run quantify --help
```

After running the `calculate` command for a cluster, you get the final summary:

```bash
{
    "escape": {
        "cff": 5.88235294117647,
        "readme": 100.0,
        "package": 41.17647058823529,
        "authors": 11.76470588235294,
        "contributors": 17.647058823529413,
        "license": 100.0,
        "codemeta": 88.23529411764706,
        "zenodo": 29.411764705882355,
        "zenodo_doi": 41.17647058823529,
        "none": 0.0
    }
}
```

## Ackowlegement:

The authors acknowledge the OSCARS project, which has received funding from the European Commission's Horizon Europe Research and Innovation programme under grant agreement No. 101129751

<img src="logo.png" alt="logo"/>
