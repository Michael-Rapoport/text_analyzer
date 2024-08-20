import wx
from utils.localization import _

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, settings_manager):
        super().__init__(parent, title=_("Settings"))
        self.settings_manager = settings_manager
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Theme selection
        theme_label = wx.StaticText(self, label=_("Theme:"))
        self.theme_choice = wx.Choice(self, choices=[_("Light"), _("Dark")])
        current_theme = self.settings_manager.get_setting("theme", "Light")
        self.theme_choice.SetStringSelection(_(current_theme))
        sizer.Add(theme_label, 0, wx.ALL, 5)
        sizer.Add(self.theme_choice, 0, wx.ALL | wx.EXPAND, 5)
        
        # Delimiter pattern
        delimiter_label = wx.StaticText(self, label=_("Delimiter Pattern:"))
        self.delimiter_input = wx.TextCtrl(self)
        current_delimiter = self.settings_manager.get_setting("delimiter_pattern", r'^/project_root/')
        self.delimiter_input.SetValue(current_delimiter)
        sizer.Add(delimiter_label, 0, wx.ALL, 5)
        sizer.Add(self.delimiter_input, 0, wx.ALL | wx.EXPAND, 5)
        
        # Auto-update settings
        self.auto_update_checkbox = wx.CheckBox(self, label=_("Check for updates automatically"))
        self.auto_update_checkbox.SetValue(self.settings_manager.get_setting("auto_update", True))
        sizer.Add(self.auto_update_checkbox, 0, wx.ALL, 5)
        
        # Buttons
        button_sizer = wx.StdDialogButtonSizer()
        save_button = wx.Button(self, wx.ID_SAVE)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(save_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()
        sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)
        
        self.SetSizer(sizer)
        save_button.Bind(wx.EVT_BUTTON, self.OnSave)
        
    def OnSave(self, event):
        self.settings_manager.set_setting("theme", self.theme_choice.GetStringSelection())
        self.settings_manager.set_setting("delimiter_pattern", self.delimiter_input.GetValue())
        self.settings_manager.set_setting("auto_update", self.auto_update_checkbox.GetValue())
        self.EndModal(wx.ID_SAVE)
