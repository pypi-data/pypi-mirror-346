import typing
from abc import ABC, abstractmethod
from typing import Optional

from flashboot_core.env.environment import Environment
from flashboot_core.env.property_source import PropertySource
from flashboot_core.io.resource import Resource


class PropertySourceLoader(ABC):

    @abstractmethod
    def get_file_extensions(self) -> typing.List[str]:
        pass

    @abstractmethod
    def load(self, name: str, source: Resource) -> PropertySource:
        pass


class SimpleYamlLoader:
    configs = {}

    def __init__(self):
        self.env = Environment()

    def load(self, source: Optional[Resource]) -> None:
        profiles = self.env.get_active_profiles()
        for profile in profiles:
            pass

#
# yaml_loader = SimpleYamlLoader()
# yaml_loader.load("")


def property_bind(property_path: str):
    def decorator(cls):
        if property_path is None:
            return

        setattr(cls, "property_path", property_path)
        pass

    return decorator
