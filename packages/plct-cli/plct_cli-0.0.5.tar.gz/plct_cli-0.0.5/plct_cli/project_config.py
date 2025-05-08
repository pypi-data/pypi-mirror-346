import os
from typing import Union
from dataclasses import dataclass
import yaml

DEFAULT_BUILDER = "html"

class ProjectConfigError(Exception):
    pass

@dataclass
class ProjectConfig:
    source_dir: str
    output_dir: str
    builder: str

def _get_config_from_yaml(project_dir:str) -> Union[dict[str, str], None]:
    plct_config_path = os.path.join(project_dir, "plct_config.yaml")
    if os.path.isfile(plct_config_path):
        with open(plct_config_path) as f:
            config = yaml.safe_load(f)
        return config
    return None


def _get_config_from_sphinx_project(project_dir: str) -> tuple[str, str, str]:
    source_dir = os.path.join(project_dir, "source")
    build_dir = os.path.join(project_dir, "build")
    if os.path.isdir(source_dir):
        _ensure_dir(build_dir)
        return source_dir, build_dir, DEFAULT_BUILDER
    else:
        source_dir = os.path.join(project_dir)
        build_dir = os.path.join(project_dir, "_build")
        if os.path.isfile(os.path.join(source_dir, "conf.py")):
            _ensure_dir(build_dir)
            return source_dir, build_dir, DEFAULT_BUILDER
        else:
            raise ProjectConfigError(
                "Unknown Sphinx project directory structure. Please specify source and build directories in plct_config.yaml")

def get_project_config(project_dir: str) -> ProjectConfig:
    config = _get_config_from_yaml(project_dir)
    if config:
        source_dir = config.get("source_dir")
        output_dir = config.get("output_dir")
        builder = config.get("builder")
        if source_dir is None or output_dir is None or builder is None:
            raise ProjectConfigError("Invalid configuration file.")
    else:
        source_dir, output_dir, builder = _get_config_from_sphinx_project(project_dir)
    return ProjectConfig(source_dir=source_dir, output_dir=output_dir, builder=builder)

def _ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)