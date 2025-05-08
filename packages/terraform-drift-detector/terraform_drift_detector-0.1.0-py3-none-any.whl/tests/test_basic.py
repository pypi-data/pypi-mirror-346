import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from terraform_drift_detector.detector import TerraformDriftDetector


class TestTerraformDriftDetector(unittest.TestCase):
    
    def test_terraform_installed_check_success(self):
        """Test that terraform installed check returns True when terraform is installed"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            detector = TerraformDriftDetector('.')
            result = detector.check_terraform_installed()
            self.assertTrue(result)
            mock_run.assert_called_once()
    
    def test_terraform_installed_check_failure(self):
        """Test that terraform installed check returns False when terraform is not installed"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("No terraform")
            detector = TerraformDriftDetector('.')
            result = detector.check_terraform_installed()
            self.assertFalse(result)
            mock_run.assert_called_once()

    def test_get_terraform_directories_empty(self):
        """Test that get_terraform_directories returns empty list when no .tf files found"""
        with patch('os.listdir') as mock_listdir, \
             patch('os.walk') as mock_walk:
            mock_listdir.return_value = ['file1.txt', 'file2.json']
            mock_walk.return_value = []
            detector = TerraformDriftDetector('.')
            result = detector.get_terraform_directories()
            self.assertEqual(result, [])
    
    def test_get_terraform_directories_success(self):
        """Test that get_terraform_directories returns directories with .tf files"""
        with patch('os.listdir') as mock_listdir, \
             patch('os.walk') as mock_walk:
            mock_listdir.return_value = ['main.tf', 'variables.tf']
            mock_walk.return_value = [
                ('/path/to/dir', ['module1'], ['file.txt']),
                ('/path/to/dir/module1', [], ['main.tf'])
            ]
            detector = TerraformDriftDetector('/path/to/dir')
            result = detector.get_terraform_directories()
            self.assertEqual(result, ['/path/to/dir', '/path/to/dir/module1'])


if __name__ == '__main__':
    unittest.main()