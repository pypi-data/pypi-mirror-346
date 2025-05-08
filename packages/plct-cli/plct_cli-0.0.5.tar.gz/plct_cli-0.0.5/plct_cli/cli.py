
from typing import Union
from importlib import import_module
import click
import shutil
import os

from paver.easy import sh

from .project_config import ProjectConfig, get_project_config, ProjectConfigError

EXTENSIONS = (".rst", ".md", ".txt")

@click.group()
def main():
    """
    Petlja learning content tool command-line interface.

    For help on specific command, use: plct [COMMAND] --help
    """
    pass


@main.command()
@click.option("-so", "--sphinx-options", default=[], multiple=True, help="Sphinx options")
@click.option("-sf", "--sphinx-files", default=[],  multiple=True, help="Sphinx-build filenames")
def build(sphinx_options, sphinx_files) -> None:
    project_config = _get_source_and_output_dirs_or_print_error()
    if project_config is None:
        return
    source_dir = project_config.source_dir
    output_dir = project_config.output_dir
    builder = project_config.builder
    options = " ".join(sphinx_options)
    files = " ".join(sphinx_files)
    sh(f'sphinx-build -M {builder} {options} "{source_dir}" "{output_dir}" {files}')


@main.command()
@click.option("-so", "--sphinx-options", default=[], multiple=True, help="Sphinx options")
def preview(sphinx_options) -> None:
    project_config = _get_source_and_output_dirs_or_print_error()
    if project_config is None:
        return
    source_dir = project_config.source_dir
    output_dir = project_config.output_dir
    builder = project_config.builder

    options = " ".join(sphinx_options)
    options += f" -b {builder}"
    options += f" -d {output_dir}/doctrees"
    options += f" --open-browser"

    # mimicing sphinx-build -M option
    if builder != "plct_builder":
        output_dir = os.path.join(output_dir, builder)
    else:
        #hacking since sphinx autobuild does not support difrent arguments for build and serve
        output_dir = os.path.join(output_dir, builder, "static_website")

    sh(f'sphinx-autobuild "{source_dir}" "{output_dir}" {options} ')

@main.command()
def publish() -> None:
    project_config = _get_source_and_output_dirs_or_print_error()
    if project_config is None:
        return
    if project_config.builder == "plct_builder":
        static_website_root = os.path.join(project_config.output_dir, "plct_builder", "static_website")
    else:
        static_website_root = os.path.join(project_config.output_dir, project_config.builder)
    shutil.copytree(static_website_root, "docs", dirs_exist_ok=True)
    if not os.path.isfile("docs/.nojekyll"):
        with open("docs/.nojekyll", "w") as nojekyll_file:
            nojekyll_file.write("")


@main.command()
def clean() -> None:
    project_config = _get_source_and_output_dirs_or_print_error()
    if project_config is None:
        return
    shutil.rmtree(project_config.output_dir, ignore_errors=True)

@main.command()
def get_markdown() -> None:
    project_dir = os.getcwd()
    project_config = _get_source_and_output_dirs_or_print_error()
    if project_config is None:
        return
    build_dir_source_copy_path = os.path.join(project_config.output_dir, "_sources")
    source_dir = build_dir_source_copy_path if os.path.isdir(build_dir_source_copy_path) else project_config.source_dir
    package_dir = os.path.join(project_dir, "markdown_files")
    if not os.path.isdir(package_dir):
        os.makedirs(package_dir)
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(EXTENSIONS):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(package_dir, file)
                shutil.copy2(src_file, dst_file)
    shutil.make_archive("package", "zip", package_dir)
    shutil.rmtree(package_dir, ignore_errors=True)

def load_extension_commands():
    try:
        extension = import_module('plct_server')
        extension.register_extension_command(main)
    except ImportError:
        pass

load_extension_commands()

def _get_source_and_output_dirs_or_print_error() -> Union[ProjectConfig, None]:
    project_dir = os.getcwd()
    try:
        project_config = get_project_config(project_dir)
    except ProjectConfigError as error:
        print(error)
        return None
    return project_config