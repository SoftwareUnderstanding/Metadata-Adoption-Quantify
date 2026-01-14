import unittest
import os
import json
import tempfile
import shutil
from quantify.rqs_scripts import rq3

class TestRQ3Function(unittest.TestCase):

    """Test suite for RQ3 version classification and consistency analysis"""
    def setUp(self):
        self.temp_input_dir = tempfile.mkdtemp()
        self.temp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_input_dir)
        shutil.rmtree(self.temp_output_dir)

    def create_test_json_file(self, filename, content):
        """Helper method to create test JSON files"""
        file_path = os.path.join(self.temp_input_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(content, f)
        return file_path

###################################################################
    def test_semantic_versioning_detection(self):
        """Test detection of semantic versioning (e.g., v1.2.3)"""
        test_data = {
            "releases": [
                {
                    "confidence": 1,
                    "result": {
                        "tag": "v1.0.0",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                },
                {
                    "confidence": 1,
                    "result": {
                        "tag": "v1.2.3",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                },
                {
                    "confidence": 1,
                    "result": {
                        "tag": "v2.0.0-beta",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                }
            ]
        }
        
        self.create_test_json_file('output_test1.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        
        # Verify releases were detected
        self.assertEqual(result['releases']['count'], 1)
        self.assertEqual(len(result['releases']['versions']), 1)
        
        # Process versions for classification
        consistency_results = rq3.process_versions(self.temp_input_dir, result)
        
        # Verify semantic versioning classification
        self.assertEqual(consistency_results['summary']['class_counts']['Semantic'], 1)
        self.assertEqual(consistency_results['summary']['consistent_count'], 1)

###################################################################
    def test_calendar_versioning_detection(self):
        """Test detection of calendar versioning (e.g., 2024.01.15)"""
        test_data = {
            "releases": [
                {
                    "confidence": 1,
                    "result": {
                        "tag": "2024.01",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                },
                {
                    "confidence": 1,
                    "result": {
                        "tag": "2024.02",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                }
            ]
        }
        
        self.create_test_json_file('output_test2.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        
        # Verify releases were detected
        self.assertEqual(result['releases']['count'], 1)
        
        # Process versions for classification
        consistency_results = rq3.process_versions(self.temp_input_dir, result)
        
        # Verify calendar versioning classification
        self.assertEqual(consistency_results['summary']['class_counts']['Calendar'], 1)

###################################################################
    def test_alphanumeric_versioning_detection(self):
        """Test detection of alphanumeric versioning (e.g., release-abc123)"""
        test_data = {
            "releases": [
                {
                    "confidence": 1,
                    "result": {
                        "tag": "release-abc",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                },
                {
                    "confidence": 1,
                    "result": {
                        "tag": "stable_v1",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                }
            ]
        }
        
        self.create_test_json_file('output_test3.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        
        # Verify releases were detected
        self.assertEqual(result['releases']['count'], 1)
        
        # Process versions for classification
        consistency_results = rq3.process_versions(self.temp_input_dir, result)
        
        # Verify alphanumeric versioning classification
        self.assertEqual(consistency_results['summary']['class_counts']['Alphanumeric'], 1)

###################################################################
    def test_inconsistent_versioning(self):
        """Test detection of inconsistent versioning schemes"""
        test_data = {
            "releases": [
                {
                    "confidence": 1,
                    "result": {
                        "tag": "v1.0.0",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                },
                {
                    "confidence": 1,
                    "result": {
                        "tag": "2024.01",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                }
            ]
        }
        
        self.create_test_json_file('output_test4.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        
        # Process versions for classification
        consistency_results = rq3.process_versions(self.temp_input_dir, result)
        
        # Verify inconsistent versioning is detected
        self.assertEqual(consistency_results['summary']['inconsistent_count'], 1)

###################################################################
    def test_no_releases(self):
        """Test handling of repositories with no releases"""
        test_data = {
            "somef_missing_categories": ["releases"]
        }
        
        self.create_test_json_file('output_test5.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        
        # Verify no releases were detected
        self.assertEqual(result['releases']['count'], 0)
        self.assertEqual(result['None']['count'], 1)

###################################################################
    def test_save_results(self):
        """Test that results are saved correctly"""
        test_data = {
            "releases": [
                {
                    "confidence": 1,
                    "result": {
                        "tag": "v1.0.0",
                        "type": "Release"
                    },
                    "technique": "GitHub_API"
                }
            ]
        }
        
        self.create_test_json_file('output_test6.json', test_data)
        
        # Call rq3 function
        result = rq3.rq3(self.temp_input_dir, 'somef_missing_categories')
        consistency_results = rq3.process_versions(self.temp_input_dir, result)
        
        # Save results
        rq3.save_results(
            self.temp_output_dir,
            result,
            consistency_results,
            'test_release_class.json',
            'test_release_const.json'
        )
        
        # Verify output files were created
        class_path = os.path.join(self.temp_output_dir, 'test_release_class.json')
        const_path = os.path.join(self.temp_output_dir, 'test_release_const.json')
        
        self.assertTrue(os.path.exists(class_path))
        self.assertTrue(os.path.exists(const_path))
        
        # Verify content structure
        with open(class_path, 'r') as f:
            class_result = json.load(f)
        self.assertIn('releases', class_result)
        
        with open(const_path, 'r') as f:
            const_result = json.load(f)
        self.assertIn('summary', const_result)

##################################################

if __name__ == '__main__':
    unittest.main()
