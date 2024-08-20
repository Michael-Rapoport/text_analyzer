import unittest
from unittest.mock import MagicMock, patch
import wx
from gui.main_frame import MainFrame

class TestMainFrame(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.file_processor = MagicMock()
        self.settings_manager = MagicMock()
        self.theme_manager = MagicMock()
        self.frame = MainFrame(None, "Test Frame", self.file_processor, self.settings_manager, self.theme_manager)

    def tearDown(self):
        self.frame.Destroy()
        self.app.MainLoop()

    def test_create_menu_bar(self):
        menu_bar = self.frame.GetMenuBar()
        self.assertIsNotNone(menu_bar)
        self.assertEqual(menu_bar.GetMenuCount(), 5)  # File, Edit, View, Plugins, Help

    @patch('wx.FileDialog')
    def test_on_open_file(self, mock_file_dialog):
        mock_file_dialog.return_value.ShowModal.return_value = wx.ID_OK
        mock_file_dialog.return_value.GetPath.return_value = "test_file.txt"
        
        with patch.object(self.frame, 'ProcessFile') as mock_process_file:
            self.frame.OnOpenFile(None)
            mock_process_file.assert_called_once_with("test_file.txt")

    def test_toggle_dark_mode(self):
        with patch.object(self.theme_manager, 'set_theme') as mock_set_theme:
            event = MagicMock()
            event.IsChecked.return_value = True
            self.frame.OnToggleDarkMode(event)
            mock_set_theme.assert_called_once_with("dark")

    def test_check_for_updates(self):
        with patch.object(self.frame.updater, 'check_for_updates', return_value=True):
            with patch('wx.MessageDialog') as mock_dialog:
                mock_dialog.return_value.ShowModal.return_value = wx.ID_YES
                with patch.object(self.frame, 'DownloadAndInstallUpdate') as mock_download:
                    self.frame.CheckForUpdates()
                    mock_download.assert_called_once()

if __name__ == '__main__':
    unittest.main()
