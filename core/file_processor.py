import os
import zipfile
import threading
import mmap
from typing import Dict, Generator
import concurrent.futures
import tempfile
import re
from utils.memory_optimizer import MemoryOptimizer

class FileProcessor:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.cancel_flag = threading.Event()
        self.delimiter_pattern = self.settings_manager.get_setting("delimiter_pattern", r'^/project_root/')

    def process_file(self, file_path: str, progress_callback=None) -> Dict[str, str]:
        self.cancel_flag.clear()
        print(f"Starting to process file: {file_path}")
        
        file_structure = {}
        total_size = os.path.getsize(file_path)
        processed_size = 0

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_chunk = {executor.submit(self._process_chunk, chunk): chunk 
                                   for chunk in self._read_file_chunks(file_path)}
                
                for future in concurrent.futures.as_completed(future_to_chunk):
                    if self.cancel_flag.is_set():
                        print("File processing cancelled")
                        return {}
                    
                    chunk = future_to_chunk[future]
                    try:
                        chunk_structure = future.result()
                        file_structure.update(chunk_structure)
                    except Exception as exc:
                        print(f"Error processing chunk: {str(exc)}")
                    
                    processed_size += len(chunk)
                    if progress_callback:
                        progress_callback(int(processed_size / total_size * 100))

                    MemoryOptimizer.optimize()

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            raise

        return file_structure

    def _read_file_chunks(self, file_path: str, chunk_size: int = 1024*1024) -> Generator[str, None, None]:
        with open(file_path, 'r') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for i in range(0, len(mm), chunk_size):
                    yield mm[i:i+chunk_size].decode('utf-8')

    def _process_chunk(self, chunk: str) -> Dict[str, str]:
        chunk_structure = {}
        lines = chunk.split('\n')
        current_file = None
        current_content = []

        for line in lines:
            if re.match(self.delimiter_pattern, line):
                if current_file:
                    chunk_structure[current_file] = '\n'.join(current_content)
                current_file = line.strip()
                current_content = []
            else:
                current_content.append(line)

        if current_file:
            chunk_structure[current_file] = '\n'.join(current_content)

        return chunk_structure

    def create_zip_archive(self, directory: str, output_file: str, progress_callback=None):
        print(f"Creating ZIP archive: {output_file}")
        total_files = sum([len(files) for _, _, files in os.walk(directory)])
        processed_files = 0

        try:
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(directory):
                    for file in files:
                        if self.cancel_flag.is_set():
                            print("ZIP creation cancelled")
                            return

                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, directory)
                        
                        try:
                            zipf.write(file_path, arcname)
                        except Exception as e:
                            print(f"Error adding file to ZIP: {str(e)}")
                        
                        processed_files += 1
                        if progress_callback:
                            progress_callback(int(processed_files / total_files * 100))

        except Exception as e:
            print(f"Error creating ZIP archive: {str(e)}")
            raise

        print(f"ZIP archive created successfully: {output_file}")

    def process_large_file(self, file_path: str, output_dir: str, progress_callback=None) -> None:
        print(f"Processing large file: {file_path}")
        total_size = os.path.getsize(file_path)
        processed_size = 0

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                for chunk in self._read_file_chunks(file_path):
                    if self.cancel_flag.is_set():
                        print("Large file processing cancelled")
                        return

                    chunk_structure = self._process_chunk(chunk)
                    self._write_chunk_to_temp(chunk_structure, temp_dir)

                    processed_size += len(chunk)
                    if progress_callback:
                        progress_callback(int(processed_size / total_size * 100))

                    MemoryOptimizer.optimize()

                self._merge_temp_files(temp_dir, output_dir)

        except Exception as e:
            print(f"Error processing large file: {str(e)}")
            raise

        print(f"Large file processed successfully")

    def _write_chunk_to_temp(self, chunk_structure: Dict[str, str], temp_dir: str) -> None:
        for file_path, content in chunk_structure.items():
            temp_file_path = os.path.join(temp_dir, file_path.lstrip('/'))
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            with open(temp_file_path, 'a') as f:
                f.write(content + '\n')

    def _merge_temp_files(self, temp_dir: str, output_dir: str) -> None:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                temp_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(temp_file_path, temp_dir)
                output_file_path = os.path.join(output_dir, relative_path)
                
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                os.rename(temp_file_path, output_file_path)
