import wx
from gui.main_frame import MainFrame
from core.file_processor import FileProcessor
from utils.settings_manager import SettingsManager
from utils.theme_manager import ThemeManager
from utils.error_handler import ErrorHandler
from utils.localization import setup_localization

class TextFileAnalyzerApp(wx.App):
    def OnInit(self):
        ErrorHandler.setup()
        setup_localization()
        
        self.settings_manager = SettingsManager()
        self.theme_manager = ThemeManager(self)
        self.file_processor = FileProcessor(self.settings_manager)
        
        self.main_frame = MainFrame(None, title="Text File Analyzer", 
                                    file_processor=self.file_processor,
                                    settings_manager=self.settings_manager,
                                    theme_manager=self.theme_manager)
        self.main_frame.Show()
        return True

if __name__ == "__main__":
    app = TextFileAnalyzerApp()
    app.MainLoop()
