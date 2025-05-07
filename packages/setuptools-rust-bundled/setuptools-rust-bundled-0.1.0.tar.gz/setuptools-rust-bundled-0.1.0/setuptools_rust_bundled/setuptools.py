from . import _wrapper
from typing import Optional, Mapping, Any

try:
    from setuptools import build_meta
except ImportError:
    raise ImportError("Setuptools is not installed.")


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    return _wrapper(lambda: build_meta.build_wheel(wheel_directory, config_settings, metadata_directory))

def build_sdist(sdist_directory, config_settings=None) -> str:
    return _wrapper(lambda: build_meta.build_sdist(sdist_directory, config_settings))

def get_requires_for_build_wheel(config_settings=None) -> list[str]:
    return _wrapper(lambda: build_meta.get_requires_for_build_wheel(config_settings))

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str:
    return _wrapper(lambda: build_meta.prepare_metadata_for_build_wheel(metadata_directory, config_settings))

def prepare_metadata_for_build_editable(metadata_directory, config_settings=None) -> str:
    return _wrapper(lambda: build_meta.prepare_metadata_for_build_editable(metadata_directory, config_settings))

def get_requires_for_build_sdist(config_settings=None) -> list[str]:
    return _wrapper(lambda: build_meta.get_requires_for_build_sdist(config_settings))

def build_editable(
    wheel_directory: str,
    config_settings: Optional[Mapping[str, Any]] = None,
    metadata_directory: Optional[str] = None,
) -> str:
    return _wrapper(lambda: build_meta.build_editable(
        wheel_directory,
        config_settings,
        metadata_directory
    ))
