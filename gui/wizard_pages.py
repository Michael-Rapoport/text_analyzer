import wx
import wx.adv
from utils.localization import _

class WelcomePage(wx.adv.WizardPageSimple):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label=_("Welcome to Text File Analyzer"))
        title.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        description = wx.StaticText(self, label=_("This wizard will guide you through the process of analyzing and processing your text file."))
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(description, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)

class FileSelectionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, file_processor):
        super().__init__(parent)
        self.file_processor = file_processor
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.file_picker = wx.FilePickerCtrl(self, message=_("Choose a file to analyze"))
        sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer)

    def SetFilePath(self, path):
        self.file_picker.SetPath(path)

class ProcessingOptionsPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, settings_manager):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Delimiter pattern
        delimiter_label = wx.StaticText(self, label=_("Delimiter Pattern:"))
        self.delimiter_input = wx.TextCtrl(self)
        current_delimiter = self.settings_manager.get_setting("delimiter_pattern", r'^/project_root/')
        self.delimiter_input.SetValue(current_delimiter)
        sizer.Add(delimiter_label, 0, wx.ALL, 5)
        sizer.Add(self.delimiter_input, 0, wx.ALL | wx.EXPAND, 5)

        # Output options
        output_label = wx.StaticText(self, label=_("Output Options:"))
        self.create_zip_checkbox = wx.CheckBox(self, label=_("Create ZIP archive"))
        self.create_zip_checkbox.SetValue(True)
        sizer.Add(output_label, 0, wx.ALL, 5)
        sizer.Add(self.create_zip_checkbox, 0, wx.ALL, 5)

        self.SetSizer(sizer)

class PreviewPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, file_processor):
        super().__init__(parent)
        self.file_processor = file_processor
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.preview_tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        sizer.Add(self.preview_tree, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer)

    def UpdatePreview(self, file_structure):
        self.preview_tree.DeleteAllItems()
        root = self.preview_tree.AddRoot("Root")
        self.AddTreeNodes(root, file_structure)

    def AddTreeNodes(self, parent, items):
        for path, content in items.items():
            parts = path.split('/')
            current = parent
            for part in parts[1:]:  # Skip 'project_root'
                child = self.preview_tree.AppendItem(current, part)
                current = child

class ProcessingPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, file_processor):
        super().__init__(parent)
        self.file_processor = file_processor
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.progress_bar = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.status_text = wx.StaticText(self, label=_("Processing..."))
        sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.status_text, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)

    def UpdateProgress(self, value, status=None):
        self.progress_bar.SetValue(value)
        if status:
            self.status_text.SetLabel(status)

class CompletionPage(wx.adv.WizardPageSimple):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetupUI()

    def SetupUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label=_("Processing Complete"))
        title.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        description = wx.StaticText(self, label=_("Your file has been successfully processed and saved."))
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(description, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)
