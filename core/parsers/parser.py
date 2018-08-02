# USED A LOT OF CODE FROM 'MASTERING PYTHON'

import abc
import fnmatch
import importlib
import re
import os

MODULE_NAME_RE = re.compile('[a-z][a-z0-9_]*', re.IGNORECASE)


class PluginsSeeker(abc.ABCMeta):
    plugins = dict()

    def __new__(mcs, name, bases, namespace):
        cls = abc.ABCMeta.__new__(mcs, name, bases, namespace)
        if isinstance(cls.name, str):
            mcs.plugins[cls.name] = cls
        return cls

    @classmethod
    def get(cls, name):
        return cls.plugins[name]

    @classmethod
    def find_handler(cls, document):
        for plugin in cls.plugins:
            if fnmatch.fnmatch(document, cls.plugins[plugin].handles):
                return cls.plugins[plugin]

    @classmethod
    def load(cls, * plugin_modules):
        for plugin_module in plugin_modules:
            __plugin = importlib.import_module(plugin_module)

    @classmethod
    def load_core_plugins(cls):
        module = 'core.parsers.plugins'
        core_plugin_directory = os.path.dirname(__file__)

        for file_ in os.listdir("{0}/plugins".format(core_plugin_directory)):
            name, ext = os.path.splitext(file_)
            full_path = os.path.join(core_plugin_directory, file_)
            import_path = [module]
            if name == "__pycache__":
                continue
            elif os.path.isdir(full_path):
                import_path.append(file_)
            elif ext == ".py" and MODULE_NAME_RE.match(name):
                import_path.append(name)
            else:
                continue

            __plugin = importlib.import_module('.'.join(import_path))


class PluginParser(metaclass=PluginsSeeker):
    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()

    @property
    @abc.abstractmethod
    def handles(self):
        raise NotImplemented()

    @abc.abstractmethod
    def parse_document(self):
        raise NotImplemented()
