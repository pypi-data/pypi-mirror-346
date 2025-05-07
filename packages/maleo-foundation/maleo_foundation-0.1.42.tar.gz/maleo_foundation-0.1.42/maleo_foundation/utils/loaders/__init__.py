from __future__ import annotations
from .json import JSONLoader
from .key import KeyLoader
from .yaml import YAMLLoader

class BaseLoaders:
    Json = JSONLoader
    Key = KeyLoader
    Yaml = YAMLLoader