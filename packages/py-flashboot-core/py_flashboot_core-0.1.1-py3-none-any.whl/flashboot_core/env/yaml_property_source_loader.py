import typing

from flashboot_core.env import Environment
from flashboot_core.env.property_source import PropertySource
from flashboot_core.env.property_source_loader import PropertySourceLoader
from flashboot_core.io.resource import Resource


class SimpleYamlLoader:
    configs = {}

    def __init__(self):
        self.env = Environment()

    def load(self, source: Resource) -> None:
        profiles = self.env.get_active_profiles()
        for profile in profiles:
            pass


class ResourceDecorator:

    def __init__(self, property_path: str):
        self.property_path = property_path

    def __call__(self, *args, **kwargs):
        class WrapperClass:
            def __init__(self, *args, **kwargs):
                ...

        return WrapperClass


# TODO 使用YamlPropertySourceLoader而不是SimpleYamlLoader
class YamlPropertySourceLoader(PropertySourceLoader):

    def get_file_extensions(self) -> typing.List[str]:
        return ["yml", "yaml"]

    def load(self, name: str, source: Resource) -> PropertySource:
        pass
