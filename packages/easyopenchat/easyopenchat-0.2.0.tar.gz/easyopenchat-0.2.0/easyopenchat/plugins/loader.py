
import importlib, os

def load_plugins():
    plugins = {}
    path = os.path.dirname(__file__)
    for file in os.listdir(path):
        if file.endswith("_plugin.py"):
            name = file[:-3]
            module = importlib.import_module(f"easyopenchat.plugins.{name}")
            plugins[name.replace("_plugin", "")] = module.run
    return plugins
