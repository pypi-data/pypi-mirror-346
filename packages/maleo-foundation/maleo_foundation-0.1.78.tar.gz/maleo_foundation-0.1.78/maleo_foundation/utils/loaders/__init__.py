from __future__ import annotations
from .json import JSONLoader
from .key import BaseKeyLoaders
from .yaml import YAMLLoader

class BaseLoaders:
    Json = JSONLoader
    Key = BaseKeyLoaders
    Yaml = YAMLLoader