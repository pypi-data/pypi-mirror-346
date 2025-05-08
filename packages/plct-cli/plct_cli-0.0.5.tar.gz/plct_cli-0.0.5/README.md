# PLCT CLI App

This Command-Line Interface (CLI) app, named PLCT (Petlja Learning Content Tools), provides a set of commands to streamline the management and generation of learning content using Sphinx.

## Installation

1. Clone the repository:

    ```bash
    pip install plct-cli
    ```

## Commands

### `build`

Generate learning content using `sphinx-build`. You have the option to pass specific options to Sphinx using the `-so` flag. If no options are passed, they will be deduced or read from the `plct_config` file.

```bash
plct build [-so <sphinx-options>] [-sf <sphinx-files>]
```

- `-so`, `--sphinx-options`: Specify additional options for Sphinx-build.
- `-sf`, `--sphinx-files`: Specify filenames for Sphinx-build.

### `preview`

Starts a local server using `sphinx-autobuild`. The root of this server corresponds to the root of the generated content. This allows you to edit files in the source directory and see the changes reflected in real-time on the server, as it will automatically refresh the content.

```bash
plct preview [-so <sphinx-options>]
```

- `-so`, `--sphinx-options`: Specify additional options for Sphinx-autobuild.

### `publish`

Publish learning content. Provides an easy way to create doc folder that can be used as the root for git hub pages.

```bash
plct publish
```

### `clean`

Clean the generated output directory.

```bash
plct clean
```

### `get_markdown`

Command zips all markdown files from the source directory.

```bash
plct get_markdown
```

## Configuration

The app tries to determine the command arguments (source and output directories) of the sphinx command based on the project file structure. You can also specify these configurations `plct_config.yaml`.

## License

This CLI app is licensed under the [MIT License](LICENSE). Feel free to customize and extend it according to your needs.