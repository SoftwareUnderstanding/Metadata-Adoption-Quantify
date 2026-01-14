import unittest
import os
import json
import tempfile
import shutil
from quantify.rqs_scripts import rq2

class TestRQ2Function(unittest.TestCase):

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

    def test_swh(self):

        """This is for testing the detection of SWH"""
        test_data = [
                {
                    "community": "ENVRI",
                    "github_url": "https://github.com/QuantConnect/Research"
                },
                {
                    "community": "ENVRI",
                    "github_url": "https://github.com/unitaryfund/research"
                }

        ]
        
        input_file = self.create_test_json_file('repos_test.json', test_data)
        
        # Call rq2 function
        token = ""            
        rq2.rq2(
            input_file, 
            token,
            'test_output_swh_rq2.json', 
            self.temp_output_dir
        )
        
        # This is  to verify output file was created
        output_path = os.path.join(self.temp_output_dir, 'test_output_swh_rq2.json')
        self.assertTrue(os.path.exists(output_path))
        
        # This is to check the output of the file
        with open(output_path, 'r') as f:
            result = json.load(f)
        
        # Note: Actual SWH API calls may fail in test environment
        # We verify the structure is correct
        self.assertIn('swh', result)
        self.assertIn('summary', result['swh'])

        
if __name__ == '__main__':
    unittest.main()