import requests
import os
import sys
import wx
import threading

class Updater:
    def __init__(self, current_version, update_url, parent_window):
        self.current_version = current_version
        self.update_url = update_url
        self.parent_window = parent_window

    def check_for_updates(self):
        try:
            response = requests.get(self.response = requests.get(self.update_url)
            latest_version = response.json()['version']
            return latest_version > self.current_version
        except Exception as e:
            wx.MessageBox(f"Error checking for updates: {str(e)}", "Update Check Failed", wx.OK | wx.ICON_ERROR)
            return False

    def download_update(self, download_url):
        try:
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB

            with open('update.zip', 'wb') as f:
                downloaded = 0
                for data in response.iter_content(block_size):
                    f.write(data)
                    downloaded += len(data)
                    progress = int(50 * downloaded / total_size)
                    self.parent_window.UpdateProgress(progress)

            return True
        except Exception as e:
            wx.MessageBox(f"Error downloading update: {str(e)}", "Download Failed", wx.OK | wx.ICON_ERROR)
            return False

    def apply_update(self):
        # This is a placeholder implementation. The actual update process would depend on your application's structure.
        try:
            # Simulating update process
            import time
            for i in range(100):
                time.sleep(0.05)
                self.parent_window.UpdateProgress(i)
            
            wx.MessageBox("Update applied successfully. Please restart the application.", "Update Complete", wx.OK | wx.ICON_INFORMATION)
            return True
        except Exception as e:
            wx.MessageBox(f"Error applying update: {str(e)}", "Update Failed", wx.OK | wx.ICON_ERROR)
            return False
