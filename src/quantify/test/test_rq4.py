import unittest
import os
import json
import tempfile
import shutil
from quantify.rqs_scripts import rq4

class TestRQ4Function(unittest.TestCase):

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
    def test_installation_detection(self):
        """This is for testing the detection of intsallation"""
        test_data = {
              "installation": [
                {
                "confidence": 0.999999997918323,
                "result": {
                    "original_header": "Create and test locally",
                    "type": "Text_excerpt",
                    "value": "    $ git clone https://github.com/explore-platform/g-tomo.git\n    $ cd g-tomo/\n    $ docker-compose up --build\n    \n \n"
                },
                "source": "https://raw.githubusercontent.com/explore-platform/g-tomo/v2/README.md",
                "technique": "supervised_classification"
                }
            ]
        }
        
        self.create_test_json_file('output_test1.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_installation_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_installation_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['installation']['count'], 0)
###################################################################
    def test_requirements_detection(self):
        """This is for testing the detection of requirements"""
        test_data = {
              "requirements": [
                {
                "confidence": 1,
                "result": {
                    "original_header": "dependencies",
                    "parent_header": [
                    "agnpy"
                    ],
                    "type": "Text_excerpt",
                    "value": "The only dependencies are:\n\n* [numpy](https://numpy.org) managing the numerical computation;\n\n* [astropy](https://www.astropy.org) managing physical units and astronomical distances.\n\n* [matplotlib](https://matplotlib.org) for visualisation and reproduction of the tutorials.\n\n* [scipy](https://www.scipy.org/) for interpolation \n"
                },
                "source": "https://raw.githubusercontent.com/cosimoNigro/agnpy/master/README.md",
                "technique": "header_analysis"
                }
            ]
        }
        
        self.create_test_json_file('output_test2.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_requirements_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_requirements_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['requirements']['count'], 1)

###################################################################
    def test_download_detection(self):
        """This is for testing the detection of download"""
        test_data = {
              "download": [
                {
                "confidence": 1,
                "result": {
                    "original_header": "Download",
                    "parent_header": [
                    "R3BRoot Software <a href=\"COPYRIGHT\"><img alt=\"license\" src=\"https://alfa-ci.gsi.de/shields/badge/license-GPL--3.0-orange.svg\" /></a>"
                    ],
                    "type": "Text_excerpt",
                    "value": "~~~bash\ngit clone https://github.com/R3BRootGroup/R3BRoot.git\ncd R3BRoot\ngit clone https://github.com/R3BRootGroup/macros.git\n~~~\n"
                },
                "source": "https://raw.githubusercontent.com/R3BRootGroup/R3BRoot/jun24/README.md",
                "technique": "header_analysis"
                }
            ]
        }
        
        self.create_test_json_file('output_test3.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_download_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_download_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['download']['count'], 1)

#########################################################
    def test_documentation_detection(self):
        """This is for testing the detection of documentation"""
        test_data = {
              "documentation": [
                {
                "confidence": 1,
                "result": {
                    "format": "readthedocs",
                    "type": "Url",
                    "value": "https://freesas.readthedocs.io/"
                },
                "source": "https://raw.githubusercontent.com/kif/freesas/main/README.md",
                "technique": "regular_expression"
                }
            ]
        }
        
        self.create_test_json_file('output_test4.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_documentation_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_documentation_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['documentation']['count'], 1)

#######################################################
    def test_spdx_detection(self):
        """This is for testing the detection of spdx in a license"""
        test_data = { 
            "license": [
                {
                "confidence": 1,
                "result": {
                    "name": "MIT License",
                    "spdx_id": "MIT",
                    "type": "License",
                    "url": "https://api.github.com/licenses/mit",
                    "value": "https://api.github.com/licenses/mit"
                },
                "technique": "GitHub_API"
                },
                {
                "confidence": 1,
                "result": {
                    "type": "File_dump",
                    "value": "The MIT License (MIT)\n\nCopyright (c) 2014 Jerome Kieffer\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the \"Software\"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n"
                },
                "source": "https://raw.githubusercontent.com/kif/freesas/main/LICENSE",
                "technique": "file_exploration"
                }
            ],
        }
        
        self.create_test_json_file('output_test5.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_spdx_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_spdx_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['license']['spdx']['count'], 1)

#######################################################
    def test_no_spdx_detection(self):
        """This is for testing the detection of no_spdx in a license"""
        test_data = {
             "license": [
                {
                "confidence": 1,
                "result": {
                    "original_header": "License",
                    "type": "Text_excerpt",
                    "value": "\r\nThe project is licensed under the GPL-v3 license.\r\n"
                },
                "source": "https://raw.githubusercontent.com/ElettraSciComp/Pore3D/master/README.md",
                "technique": "header_analysis"
                }
            ]
        }
        
        self.create_test_json_file('output_test6.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_no_spdx_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_no_spdx_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['license']['no_spdx']['count'], 1)

#########################################################
    def test_no_license_detection(self):
        """This is for testing the detection of no license"""
        test_data = {
             "somef_missing_categories": [
                "installation",
                "citation",
                "acknowledgement",
                "run",
                "license",
                "requirements",
                "contact",
                "contributors",
                "usage",
                "faq",
                "support",
                "identifier",
                "has_build_file",
                "executable_example"
            ]
        }
        
        self.create_test_json_file('output_test7.json', test_data)
        
        # Call rq4 function
        rq4.rq4(
            self.temp_input_dir, 
            'somef_missing_categories', 
            'test_output_no_license_rq4.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir,'test_output_no_license_rq4.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(result['license']['no_license']['count'], 1)

if __name__ == '__main__':
    unittest.main()