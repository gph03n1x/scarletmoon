# USED A LOT OF CODE FROM 'MASTERING PYTHON'

import abc
import fnmatch
import importlib
import os
import re
from collections import defaultdict

MODULE_NAME_RE = re.compile('[a-z][a-z0-9_]*', re.IGNORECASE)


class PluginsSeeker(abc.ABCMeta):
    plugins = defaultdict(dict)

    def __new__(mcs, name, bases, namespace):
        cls = abc.ABCMeta.__new__(mcs, name, bases, namespace)
        if isinstance(cls.name, str):
            mcs.plugins[cls.TYPE][cls.name] = cls
        return cls

    @classmethod
    def get_query_plugin(cls, name):
        return cls.plugins["QUERY"][name]

    @classmethod
    def get_parser_plugin(cls, name):
        return cls.plugins["PARSER"][name]

    @classmethod
    def find_appropriate_parser(cls, document):
        for plugin in cls.plugins["PARSER"]:
            if fnmatch.fnmatch(document, cls.plugins["PARSER"][plugin].handles):
                return cls.plugins["PARSER"][plugin]

    @classmethod
    def process_query(cls, query):
        for plugin in cls.plugins["QUERY"]:
            if cls.plugins["QUERY"][plugin].can_handle(query):
                return cls.plugins["QUERY"][plugin].reconstruct_query(query)
        return query

    @classmethod
    def load(cls, * plugin_modules):
        for plugin_module in plugin_modules:
            __plugin = importlib.import_module(plugin_module)

    @classmethod
    def load_all_plugins(cls):
        cls.load_core_plugins('parsers')
        cls.load_core_plugins('query')

    @classmethod
    def load_core_plugins(cls, sub_plugin):
        module = 'plugins.{0}'.format(sub_plugin)

        for file_ in os.listdir("{0}/plugins/{1}/".format(os.getcwd(), sub_plugin)):
            name, ext = os.path.splitext(file_)
            full_path = os.path.join(os.getcwd(), file_)
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
    TYPE = "PARSER"

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()

    @property
    @abc.abstractmethod
    def handles(self):
        raise NotImplemented()

    @staticmethod
    @abc.abstractmethod
    def parse_document(file_name):
        raise NotImplemented()


class PluginQuery(metaclass=PluginsSeeker):
    TYPE = "QUERY"

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()

    @staticmethod
    @abc.abstractmethod
    def can_handle(query):
        raise NotImplemented()

    @staticmethod
    @abc.abstractmethod
    def reconstruct_query(query):
        raise NotImplemented()
