import wx
import wx.adv
import threading
from gui.wizard_pages import (
    WelcomePage, FileSelectionPage, ProcessingOptionsPage, 
    PreviewPage, ProcessingPage, CompletionPage
)
from gui.settings_dialog import SettingsDialog
from utils.drag_drop_target import FileDropTarget
from utils.recent_files import RecentFiles
from utils.updater import Updater
from utils.localization import _
from utils.plugin_manager import PluginManager

class MainFrame(wx.Frame):
    def __init__(self, parent, title, file_processor, settings_manager, theme_manager):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.file_processor = file_processor
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        self.recent_files = RecentFiles()
        self.updater = Updater("1.0", "https://example.com/update_info.json", self)
        self.plugin_manager = PluginManager()
        
        self.SetupUI()
        self.SetDropTarget(FileDropTarget(self))
        
        if self.settings_manager.get_setting("auto_update", True):
            self.CheckForUpdates()
        
        self.plugin_manager.load_plugins()
        
        self.SetupAccelerators()
        
    def SetupUI(self):
        self.CreateStatusBar()
        self.CreateMenuBar()
        
        self.splitter = wx.SplitterWindow(self)
        
        self.wizard_panel = wx.Panel(self.splitter)
        self.wizard = wx.adv.Wizard(self.wizard_panel, -1, _("Text File Analyzer Wizard"))
        self.welcome_page = WelcomePage(self.wizard)
        self.file_selection_page = FileSelectionPage(self.wizard, self.file_processor)
        self.options_page = ProcessingOptionsPage(self.wizard, self.settings_manager)
        self.preview_page = PreviewPage(self.wizard, self.file_processor)
        self.processing_page = ProcessingPage(self.wizard, self.file_processor)
        self.completion_page = CompletionPage(self.wizard)
        
        wx.adv.WizardPageSimple.Chain(self.welcome_page, self.file_selection_page)
        wx.adv.WizardPageSimple.Chain(self.file_selection_page, self.options_page)
        wx.adv.WizardPageSimple.Chain(self.options_page, self.preview_page)
        wx.adv.WizardPageSimple.Chain(self.preview_page, self.processing_page)
        wx.adv.WizardPageSimple.Chain(self.processing_page, self.completion_page)
        
        self.wizard.GetPageAreaSizer().Add(self.welcome_page)
        
        self.plugin_panel = wx.Panel(self.splitter)
        self.plugin_list = wx.ListBox(self.plugin_panel, style=wx.LB_SINGLE)
        self.plugin_description = wx.TextCtrl(self.plugin_panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.run_plugin_button = wx.Button(self.plugin_panel, label=_("Run Plugin"))
        self.configure_plugin_button = wx.Button(self.plugin_panel, label=_("Configure Plugin"))
        
        plugin_sizer = wx.BoxSizer(wx.VERTICAL)
        plugin_sizer.Add(wx.StaticText(self.plugin_panel, label=_("Installed Plugins")), 0, wx.ALL, 5)
        plugin_sizer.Add(self.plugin_list, 1, wx.EXPAND|wx.ALL, 5)
        plugin_sizer.Add(self.plugin_description, 1, wx.EXPAND|wx.ALL, 5)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.run_plugin_button, 0, wx.ALL, 5)
        button_sizer.Add(self.configure_plugin_button, 0, wx.ALL, 5)
        plugin_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)
        self.plugin_panel.SetSizer(plugin_sizer)
        
        self.splitter.SplitVertically(self.wizard_panel, self.plugin_panel)
        self.splitter.SetMinimumPaneSize(200)
        
        self.UpdatePluginList()
        
        self.plugin_list.Bind(wx.EVT_LISTBOX, self.OnPluginSelected)
        self.run_plugin_button.Bind(wx.EVT_BUTTON, self.OnRunPlugin)
        self.configure_plugin_button.Bind(wx.EVT_BUTTON, self.OnConfigurePlugin)
        
    def CreateMenuBar(self):
        menu_bar = wx.MenuBar()
        
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, _("Open File") + "\tCtrl+O")
        
        self.recent_menu = wx.Menu()
        file_menu.AppendSubMenu(self.recent_menu, _("Recent Files"))
        self.UpdateRecentFilesMenu()
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, _("Exit") + "\tCtrl+Q")
        
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_PREFERENCES, _("Settings") + "\tCtrl+,")
        
        view_menu = wx.Menu()
        view_menu.Append(wx.ID_ANY, _("Toggle Dark Mode") + "\tCtrl+T", kind=wx.ITEM_CHECK)
        
        plugins_menu = wx.Menu()
        plugins_menu.Append(wx.ID_ANY, _("Manage Plugins") + "\tCtrl+M")
        
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, _("About"))
        help_menu.Append(wx.ID_ANY, _("Check for Updates") + "\tCtrl+U")
        
        menu_bar.Append(file_menu, _("File"))
        menu_bar.Append(edit_menu, _("Edit"))
        menu_bar.Append(view_menu, _("View"))
        menu_bar.Append(plugins_menu, _("Plugins"))
        menu_bar.Append(help_menu, _("Help"))
        
        self.SetMenuBar(menu_bar)
        
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=wx.ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.OnToggleDarkMode, id=view_menu.FindItem(_("Toggle Dark Mode")))
        self.Bind(wx.EVT_MENU, self.OnManagePlugins, id=plugins_menu.FindItem(_("Manage Plugins")))
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnCheckForUpdates, id=help_menu.FindItem(_self.Bind(wx.EVT_MENU, self.OnCheckForUpdates, id=help_menu.FindItem(_("Check for Updates")))

    def SetupAccelerators(self):
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
            (wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
            (wx.ACCEL_CTRL, ord(','), wx.ID_PREFERENCES),
            (wx.ACCEL_CTRL, ord('T'), self.GetMenuBar().FindMenuItem(_("View"), _("Toggle Dark Mode"))),
            (wx.ACCEL_CTRL, ord('M'), self.GetMenuBar().FindMenuItem(_("Plugins"), _("Manage Plugins"))),
            (wx.ACCEL_CTRL, ord('U'), self.GetMenuBar().FindMenuItem(_("Help"), _("Check for Updates"))),
        ])
        self.SetAcceleratorTable(accel_tbl)

    def UpdatePluginList(self):
        self.plugin_list.Clear()
        for plugin in self.plugin_manager.get_plugins():
            self.plugin_list.Append(plugin.name)

    def OnPluginSelected(self, event):
        selected_plugin = self.plugin_manager.get_plugins()[event.GetSelection()]
        self.plugin_description.SetValue(selected_plugin.description)

    def OnRunPlugin(self, event):
        selected_index = self.plugin_list.GetSelection()
        if selected_index != wx.NOT_FOUND:
            selected_plugin = self.plugin_manager.get_plugins()[selected_index]
            try:
                result = self.plugin_manager.run_plugin(selected_plugin, self)
                wx.MessageBox(str(result), _("Plugin Result"), wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(str(e), _("Plugin Error"), wx.OK | wx.ICON_ERROR)

    def OnConfigurePlugin(self, event):
        selected_index = self.plugin_list.GetSelection()
        if selected_index != wx.NOT_FOUND:
            selected_plugin = self.plugin_manager.get_plugins()[selected_index]
            self.plugin_manager.configure_plugin(selected_plugin, self)

    def OnManagePlugins(self, event):
        dlg = wx.Dialog(self, title=_("Manage Plugins"))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        plugin_list = wx.CheckListBox(dlg, choices=[p.name for p in self.plugin_manager.get_plugins()])
        sizer.Add(plugin_list, 1, wx.EXPAND | wx.ALL, 10)
        
        btn_sizer = dlg.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        dlg.SetSizer(sizer)
        dlg.Fit()
        
        if dlg.ShowModal() == wx.ID_OK:
            # Here you would typically save the enabled/disabled state of plugins
            pass
        
        dlg.Destroy()

    def OnOpenFile(self, event):
        with wx.FileDialog(self, _("Open Text File"), wildcard=_("Text files (*.txt)|*.txt"),
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.ProcessFile(pathname)

    def OnExit(self, event):
        self.Close(True)

    def OnSettings(self, event):
        with SettingsDialog(self, self.settings_manager) as dlg:
            if dlg.ShowModal() == wx.ID_SAVE:
                self.ApplySettings()

    def OnToggleDarkMode(self, event):
        is_checked = event.IsChecked()
        new_theme = "dark" if is_checked else "light"
        self.theme_manager.set_theme(new_theme)
        self.settings_manager.set_setting("theme", new_theme)

    def OnAbout(self, event):
        wx.MessageBox(_("Text File Analyzer\nVersion 1.0\n\nCreated by Your Company"), 
                    _("About Text File Analyzer"), wx.OK | wx.ICON_INFORMATION)

    def OnCheckForUpdates(self, event):
        self.CheckForUpdates()

    def ProcessFile(self, file_path):
        self.recent_files.add_file(file_path)
        self.UpdateRecentFilesMenu()
        self.file_selection_page.SetFilePath(file_path)
        if self.wizard.RunWizard(self.welcome_page):
            wx.MessageBox(_("File processing completed successfully!"), _("Success"), wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(_("File processing was cancelled."), _("Cancelled"), wx.OK | wx.ICON_INFORMATION)

    def UpdateRecentFilesMenu(self):
        self.recent_menu.Clear()
        for i, file_path in enumerate(self.recent_files.get_recent_files()):
            self.recent_menu.Append(wx.ID_FILE1 + i, file_path)
            self.Bind(wx.EVT_MENU, lambda evt, path=file_path: self.OnRecentFile(evt, path), id=wx.ID_FILE1 + i)

    def OnRecentFile(self, event, file_path):
        self.ProcessFile(file_path)

    def CheckForUpdates(self):
        if self.updater.check_for_updates():
            dlg = wx.MessageDialog(self, _("An update is available. Would you like to download and install it?"),
                                _("Update Available"), wx.YES_NO | wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_YES:
                self.DownloadAndInstallUpdate()
            dlg.Destroy()
        else:
            wx.MessageBox(_("You're running the latest version."), _("No Updates Available"), wx.OK | wx.ICON_INFORMATION)

    def DownloadAndInstallUpdate(self):
        progress_dlg = wx.ProgressDialog(_("Updating"), _("Downloading update..."), maximum=100, parent=self, 
                                        style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        
        def update_progress(value):
            wx.CallAfter(progress_dlg.Update, value)

        self.UpdateProgress = update_progress

        threading.Thread(target=self._download_and_install, args=(progress_dlg,)).start()

    def _download_and_install(self, progress_dlg):
        if self.updater.download_update("https://example.com/update.zip"):
            wx.CallAfter(progress_dlg.Update, 50, _("Applying update..."))
            if self.updater.apply_update():
                wx.CallAfter(progress_dlg.Destroy)
                wx.CallAfter(wx.MessageBox, _("Update completed successfully. Please restart the application."), _("Update Complete"), wx.OK | wx.ICON_INFORMATION)
            else:
                wx.CallAfter(progress_dlg.Destroy)
        else:
            wx.CallAfter(progress_dlg.Destroy)

    def ApplySettings(self):
        # Apply any settings that need immediate effect
        theme = self.settings_manager.get_setting("theme", "light")
        self.theme_manager.set_theme(theme)
        
        # Update the delimiter pattern in the file processor
        delimiter_pattern = self.settings_manager.get_setting("delimiter_pattern", r'^/project_root/')
        self.file_processor.delimiter_pattern = delimiter_pattern
        
        # Other settings can be applied here