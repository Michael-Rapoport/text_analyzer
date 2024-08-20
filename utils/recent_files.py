import json
import os

class RecentFiles:
    def __init__(self, max_files=5, file_path='recent_files.json'):
        self.max_files = max_files
        self.file_path = file_path
        self.files = self.load_recent_files()

    def load_recent_files(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def save_recent_files(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.files, f)

    def add_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)
        self.files.insert(0, file_path)
        if len(self.files) > self.max_files:
            self.files.pop()
        self.save_recent_files()

    def get_recent_files(self):
        return self.files

    def clear(self):
        self.files = []
        self.save_recent_files()
