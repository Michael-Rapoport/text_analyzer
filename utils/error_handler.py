import wx
import traceback
import sys

class ErrorHandler:
    @staticmethod
    def setup():
        sys.excepthook = ErrorHandler.handle_exception

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        wx.CallAfter(ErrorHandler.show_error_dialog, error_msg)

    @staticmethod
    def show_error_dialog(error_msg):
        dlg = wx.MessageDialog(None, f"An error occurred:\n\n{error_msg}\n\nPlease report this error to the developers.",
                               "Error", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
