import unittest
import os
import json
import tempfile
import shutil
from quantify.rqs_scripts import rq5

class TestRQ5Function(unittest.TestCase):

    """Here I'm creating temporary files and clearing them after the test"""
    def setUp(self):

        self.temp_input_dir = tempfile.mkdtemp()
        self.temp_output_dir = tempfile.mkdtemp()

    def tearDown(self):

        shutil.rmtree(self.temp_input_dir)
        shutil.rmtree(self.temp_output_dir)

    def create_test_json_file(self, filename, content):
        """This is a method to create test JSON files"""
        file_path = os.path.join(self.temp_input_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(content, f)
        return file_path
    
###################################################################
    def test_citation_bib_detection(self):
        """This is for testing the detection of citation.bib"""
        test_data = {
            "citation": [
                {
                "confidence": 1,
                "result": {
                    "format": "bibtex",
                    "type": "File_dump",
                    "value": "year <- substr(Sys.Date(), 1, 4)\nbibentry(bibtype = \"Manual\",\n         title = \"{motus}: Fetch and use data from the Motus Wildlife Tracking System\",\n         author = person(\"Birds Canada\"),\n         year = year,\n         url = \"https://motusWTS.github.io/motus/\")\n"
                },
                "source": "https://raw.githubusercontent.com/MotusWTS/motus/main/inst/CITATION",
                "technique": "file_exploration"
                }
            ]
        }
        
        self.create_test_json_file('output_test1.json', test_data)
        
        # Call rq5 function
        rq5.rq5(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_citation_bib_rq5.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_citation_bib_rq5.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['citation']['bib'], 1)
###################################################################
    def test_citation_cff_detection(self):
        """This is for testing the detection of citation.cff"""
        test_data = {
            "citation": [
                {
                "confidence": 1,
                "result": {
                    "format": "cff",
                    "type": "File_dump",
                    "value": "# -*- mode: yaml -*-\n#\n# Run\n#\n# git shortlog -sn --no-merges `branch`\n#\n# to list contributors to a `branch` and the number of non-merge commits they made.\n#\n# Output as of 2023-10-25 (branch=dev)\n#\n# 6981  Constantine Khrulev\n# 1856  Ed Bueler\n#  360  Andy Aschwanden\n#  272  David Maxwell\n#  126  Torsten Albrecht\n#   86  Jed Brown\n#   47  Maria Zeitz\n#   30  Julien Seguinot\n#   22  Elizabeth Fischer\n#   18  Matthias Mengel\n#   13  Maria Martin\n#   13  Nathan Shemonski\n#   10  Anders Damsgaard\n#    4  Sebastian Hinck\n#    2  Enrico Degregori\n#    2  Florian Ziemen\n#    2  Joseph H Kennedy\n"
                },
                "source": "https://raw.githubusercontent.com/pism/pism/main/CITATION.cff",
                "technique": "file_exploration"
                }
            ]
        }
        
        self.create_test_json_file('output_test2.json', test_data)
        
        # Call rq5 function
        rq5.rq5(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_citation_cff_rq5.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_citation_cff_rq5.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['citation']['cff'], 1)

###################################################################
    def test_citation_readme_detection(self):
        """This is for testing the detection of citation in readme"""
        test_data = {
            "citation": [
                {
                    "result": {
                    "original_header": "Citation",
                     "type": "Text_excerpt",
                    "value": "If you use Kernel Tuner in research or research software, please cite the most relevant among the [publications on Kernel \nTuner](https://kerneltuner.github.io/kernel_tuner/stable/#citation). To refer to the project as a whole, please cite:\n\n```latex\n@article{kerneltuner,\n  author  = {Ben van Werkhoven},\n  title   = {Kernel Tuner: A search-optimizing GPU code auto-tuner},\n  journal = {Future Generation Computer Systems},\n  year = {2019},\n  volume  = {90},\n  pages = {347-358},\n  url = {https://www.sciencedirect.com/science/article/pii/S0167739X18313359},\n  doi = {https://doi.org/10.1016/j.future.2018.08.004}\n}\n```\n\n"
                    }
                }
            ]
        }
        
        self.create_test_json_file('output_test3.json', test_data)
        
        # Call rq5 function
        rq5.rq5(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_citation_readme_rq5.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_citation_readme_rq5.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['citation']['readme'], 1)

#########################################################""
if __name__ == '__main__':
    unittest.main()