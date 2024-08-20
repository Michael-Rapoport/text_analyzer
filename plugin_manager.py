import os
import importlib.util
import wx

class Plugin:
    def __init__(self, name, description, main, config_ui=None):
        self.name = name
        self.description = description
        self.main = main
        self.config_ui = config_ui

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        plugin_dir = "plugins"
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py"):
                plugin_path = os.path.join(plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'PLUGIN_NAME') and hasattr(module, 'PLUGIN_DESCRIPTION') and hasattr(module, 'main'):
                    config_ui = getattr(module, 'config_ui', None)
                    plugin = Plugin(module.PLUGIN_NAME, module.PLUGIN_DESCRIPTION, module.main, config_ui)
                    self.plugins.append(plugin)

    def get_plugins(self):
        return self.plugins

    def run_plugin(self, plugin, *args, **kwargs):
        return plugin.main(*args, **kwargs)

    def configure_plugin(self, plugin, parent):
        if plugin.config_ui:
            dialog = plugin.config_ui(parent)
            dialog.ShowModal()
            dialog.Destroy()