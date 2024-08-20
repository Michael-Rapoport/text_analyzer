import wx

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.current_theme = "light"
        self.themes = {
            "light": {
                "background": wx.Colour(255, 255, 255),
                "foreground": wx.Colour(0, 0, 0),
                "accent": wx.Colour(0, 120, 215),
            },
            "dark": {
                "background": wx.Colour(30, 30, 30),
                "foreground": wx.Colour(255, 255, 255),
                "accent": wx.Colour(0, 120, 215),
            }
        }

    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.app.SetTopWindow(self.app.main_frame)
        self._apply_theme_to_window(self.app.main_frame, theme)

    def _apply_theme_to_window(self, window, theme):
        window.SetBackgroundColour(theme["background"])
        window.SetForegroundColour(theme["foreground"])
        
        for child in window.GetChildren():
            if isinstance(child, wx.Window):
                child.SetBackgroundColour(theme["background"])
                child.SetForegroundColour(theme["foreground"])
                
                if isinstance(child, wx.Button):
                    child.SetBackgroundColour(theme["accent"])
                    child.SetForegroundColour(theme["background"])
                
                self._apply_theme_to_window(child, theme)
        
        window.Refresh()
