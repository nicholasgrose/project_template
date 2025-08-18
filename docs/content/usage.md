# Usage

This project provides a self-bootstrapping CLI. On first use it creates and manages an isolated virtual environment for
its own dependencies, so you don’t need to manually install libraries like Jinja.

## Requirements

- [Git](https://git-scm.com)
- [Python](https://www.python.org) 3.12 or newer is available on your PATH

## Quickstart

### Clone the template repository:

```shell
git clone git@github.com:nicholasgrose/project_template.git
cd project_template
```

### Use the CLI from the repo root

You can see the help text by running:

```shell
python ./generate.py --help
```

On the first run, the CLI will:

- Create a virtual environment in its directory.
- Install the CLI’s pinned dependencies into that environment.
- Re-run the command under that environment automatically.

Subsequent runs reuse the environment.

## Example Usage

### Create a new project from the template

You can create a new project from the template by running the following command:

```shell
python -m project_template new --path projects/new_repo
```

#### CLI Options

| Option            | Default?     | Description                                                          |
|-------------------|--------------|----------------------------------------------------------------------|
| --path            | Prompts User | Specifies the path to create to the new project                      |
| --project_name    | Prompts User | The name of the project to create                                    |
| --repo_name       | Prompts User | The name of the repo to create                                       |
| --author          | Prompts User | The name of the repo's author                                        |
| --repo_url        | Prompts User | The URL to the repo                                                  |
| --repo_remote_url | Prompts User | The remote URL for pushing the repo to Git                           |
| --dry-run         | False        | Whether to describe the changes that will be made without making any |

### Add to an existing project

!!! warning
This has the potential to overwrite files in the project.
If you are doing this, pay attention to the files you are asked whether to overwrite.

You can add the template to an existing project by running the following command:

```shell
python -m project_template add --path projects/existing_repo
```

#### CLI Options

| Option            | Default?     | Description                                                          |
|-------------------|--------------|----------------------------------------------------------------------|
| --path            | `.`          | Specifies the path to the project to add the template to             |
| --project_name    | Prompts User | The name of the project being added to                               |
| --repo_name       | Prompts User | The name of the repo                                                 |
| --author          | Prompts User | The name of the repo's author                                        |
| --repo_url        | Prompts User | The URL to the repo                                                  |
| --repo_remote_url | Prompts User | The remote URL for pushing the repo to Git                           |
| --dry-run         | False        | Whether to describe the changes that will be made without making any |
