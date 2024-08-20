import unittest
from unittest.mock import MagicMock, patch
from core.file_processor import FileProcessor
import tempfile
import os

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        self.settings_manager = MagicMock()
        self.file_processor = FileProcessor(self.settings_manager)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="/project_root/file1.txt\ncontent1\n/project_root/file2.txt\ncontent2\n")
    def test_process_file(self, mock_open):
        result = self.file_processor.process_file('dummy_file.txt')
        expected = {
            '/project_root/file1.txt': 'content1',
            '/project_root/file2.txt': 'content2'
        }
        self.assertEqual(result, expected)

    def test_create_zip_archive(self):
        with patch('zipfile.ZipFile') as mock_zipfile:
            self.file_processor.create_zip_archive('dummy_dir', 'output.zip')
            mock_zipfile.assert_called_once()

    def test_large_file_processing(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            for i in range(1000):
                temp_file.write(f"/project_root/file{i}.txt\ncontent{i}\n")
        
        try:
            result = self.file_processor.process_file(temp_file.name)
            self.assertEqual(len(result), 1000)
            self.assertTrue('/project_root/file0.txt' in result)
            self.assertTrue('/project_root/file999.txt' in result)
        finally:
            os.unlink(temp_file.name)

    def test_cancel_processing(self):
        with patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="/project_root/file1.txt\ncontent1\n/project_root/file2.txt\ncontent2\n"):
            self.file_processor.cancel_flag.set()
            result = self.file_processor.process_file('dummy_file.txt')
            self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
