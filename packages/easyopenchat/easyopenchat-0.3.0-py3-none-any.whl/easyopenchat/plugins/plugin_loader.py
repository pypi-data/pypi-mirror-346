import os
import importlib
import inspect

def load_plugins():
    """
    Load plugins from the plugins directory.
    
    Returns:
        dict: Mapping of plugin names to their functions.
    """
    plugins = {}
    plugin_dir = os.path.join(os.path.dirname(__file__))
    for filename in os.listdir(plugin_dir):
        if filename.endswith("_plugin.py"):
            module_name = filename[:-3]
            module = importlib.import_module(f".{module_name}", package="easyopenchat.plugins")
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and name.startswith("plugin_"):
                    plugin_name = name[len("plugin_"):]
                    plugins[plugin_name] = obj
    return plugins