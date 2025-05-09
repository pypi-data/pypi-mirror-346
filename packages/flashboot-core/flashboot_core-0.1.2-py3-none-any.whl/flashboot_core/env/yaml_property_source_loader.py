import typing

from flashboot_core.env.property_source import PropertySource
from flashboot_core.env.property_source_loader import PropertySourceLoader
from flashboot_core.io.resource import Resource


# TODO 使用YamlPropertySourceLoader而不是SimpleYamlLoader
class YamlPropertySourceLoader(PropertySourceLoader):

    def get_file_extensions(self) -> typing.List[str]:
        return ["yml", "yaml"]

    def load(self, name: str, source: Resource) -> PropertySource:
        pass
