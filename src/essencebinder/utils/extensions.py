"""
This module is responsible for managing the loading and unloading of extensions to EssenceBinder.
"""
import os
from pathlib import Path
from typing import List, Any, Union

from forged.commons.utilities.text import CaseTransformer
from forged.elements.reporting.reported import logger as log

from essencebinder.commons.patterns.decorators import hasmetadata

NATIVE_EXTENSIONS = {
    "plugin": [],
    "expansion": [],
    "localizer": [],
}

EXTENSION_DEF_META = {
    "name": "unknown",
    "label": "unknown",
    "version": "v0.1.0",
    "description": "an EssenceBinder extension.",
    "author": "unknown",
    "license": "MIT",
}


@hasmetadata(EXTENSION_DEF_META)
class BaseExtension:
    _TYPES = ["plugin", "expansion", "localizer"]
    _STATUSES = ["unloaded", "loading", "loaded", "unloading", "active", "inactive", "error"]

    def __init__(self):
        self._metadata = EXTENSION_DEF_META.copy()
        self._versions = {}
        self.dependencies = []
        self._status = "unloaded"

    @property
    def name(self):
        return self._metadata["name"]

    @name.setter
    def name(self, name: str):
        self._metadata["name"] = CaseTransformer.to_snake_case(name)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: str):
        if status not in self._STATUSES:
            raise ValueError(f"Invalid status: {status}. Valid statuses are: {', '.join(self._STATUSES)}")
        else:
            self._status = status

    @property
    def version(self):
        if self._metadata["version"] not in self._versions.keys():
            log.debug(f"Current version not in plugin versioning. Adding {self._metadata['version']} to {self.name} versioning.")
            self._versions[self._metadata["version"]] = self
        return self._metadata["version"]

    @property
    def desc(self):
        return self._metadata["description"]


class Plugin(BaseExtension):
    def __init__(self):
        super().__init__()
        log.warning("Plugin class is not implemented yet.")


class Expansion(BaseExtension):
    def __init__(self):
        super().__init__()
        log.warning("Expansion class is not implemented yet.")


class Localizer(BaseExtension):
    def __init__(self):
        super().__init__()
        log.warning("Localizer class is not implemented yet.")


class ExtensionManager:
    def __init__(self):
        self._plugins = {}
        self._expansions = {}
        self._localizers = {}

    def load_extension(self, extension: Union[Plugin, Expansion, Localizer]) -> None:
        if isinstance(extension, Plugin):
            self._plugins[extension.name] = extension
        elif isinstance(extension, Expansion):
            self._expansions[extension.name] = extension
        elif isinstance(extension, Localizer):
            self._localizers[extension.name] = extension
        else:
            raise TypeError("Unsupported extension type")


def _is_plugin_dir(path: str) -> bool:
    path = Path(path)
    if not path.is_dir():
        log.debug(f"{path} does not exist or is not a directory.")
        return False
    elif not (path / "extension.yaml").is_file():
        log.debug(f"Couldn't find Extension profile in {path}")
        return False
    elif not ((path / "plug.py").is_file() or (path / "extension.py").is_file()):
        log.debug(f"Couldn't find Extension entry code in {path}")
        return False
    else:
        return True


def load_plugin(source: Union[str, Path]):
    log.info(f"Loading plugin from {source}")
    if not _is_plugin_dir(source):
        raise ValueError(f"Invalid plugin directory: {source}")
    else:
        plugin = Plugin()
        plugin.name = os.path.basename(source)
    log.success(f"Loaded plugin: {plugin.name} ({plugin.version})")


def load_expansion(source: Union[str, Path]) -> None:
    log.info(f"Loading expansion from {source}")
    if not _is_plugin_dir(source):
        raise ValueError(f"Invalid expansion directory: {source}")
    else:
        expansion = Expansion()
        expansion.name = os.path.basename(source)
    log.success(f"Loaded expansion: {expansion.name} ({expansion.version})")


def load_localizer(source: Union[str, Path]) -> None:
    log.info(f"Loading localizer from {source}")
    if not _is_plugin_dir(source):
        raise ValueError(f"Invalid localizer directory: {source}")
    else:
        localizer = Localizer()
        localizer.name = os.path.basename(source)
    log.success(f"Loaded localizer: {localizer.name} ({localizer.version})")


def discover_extensions(path: str) -> List[str]:
    discovered = []
    for directory in os.listdir(path):
        if _is_plugin_dir(os.path.join(path, directory)):
            log.info(f"Found plugin directory: {directory}")
            discovered.append(directory)
    return discovered


def download_expansion(source: str, destination: str) -> None:
    log.info(f"Downloading expansion from {source} to {destination}")
    # Placeholder for actual download logic
    log.success(f"Downloaded expansion to {destination}")


if __name__ == '__main__':
    plugin_path = "C:/Users/aidan/PycharmProjects/EssenceBinder/.forged/extensions/plugins"
    found = discover_extensions(plugin_path)
    for plugin in found:
        load_plugin(os.path.join(plugin_path, plugin))