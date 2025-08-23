# Usage

This project provides a self-bootstrapping CLI. On first use it creates and manages an isolated virtual environment for
its own dependencies, so you don’t need to manually install libraries like Jinja.

## Requirements

- [Git](https://git-scm.com)
- [Python](https://www.python.org)
- [Task](https://taskfile.dev)

## Quickstart

### Clone the template repository:

```shell
git clone git@github.com:nicholasgrose/palimpsest.git
cd palimpsest
```

### Use the CLI from the repo root

You can see the help text by running:

```shell
python -m pal --help
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
python -m pal new --path projects/new_repo
```

#### CLI Options

| Option            | Default?     | Description                                                          |
|-------------------|--------------|----------------------------------------------------------------------|
| --template        | `general`    | The project template to use (only "general" is valid at this time)   |
| --path            | Prompts User | Specifies the path to create to the new project                      |
| --project-name    | Prompts User | The name of the project to create                                    |
| --repo-name       | Prompts User | The name of the repo to create                                       |
| --author          | Prompts User | The name of the repo's author                                        |
| --repo-url        | Prompts User | The URL to the repo                                                  |
| --repo-remote-url | Prompts User | The remote URL for pushing the repo to Git                           |
| --repo-docs-url   | Prompts User | The URL for the project docs                                         |
| --contact-email   | Prompts User | The email for contact                                                |
| --security-email  | Prompts User | The email for reporting sensitive issues                             |
| -n                | `None`       | Answer NO to all overwrite prompts                                   |
| -y                | `None`       | Answer YES to all overwrite prompts                                  |
| --dry-run         | `False`      | Whether to describe the changes that will be made without making any |

### Add to an existing project

/// warning
This has the potential to overwrite files in the project.
If you are doing this, have any changes committed so you can revert any unintentional changes.
///

You can add the template to an existing project by running the following command:

```shell
python -m pal add --path projects/existing_repo
```

#### CLI Options

| Option            | Default?     | Description                                                          |
|-------------------|--------------|----------------------------------------------------------------------|
| --template        | `general`    | The project template to use (only "general" is valid at this time)   |
| --path            | `.`          | Specifies the path to the project to add the template to             |
| --project-name    | Prompts User | The name of the project being added to                               |
| --repo-name       | Prompts User | The name of the repo                                                 |
| --author          | Prompts User | The name of the repo's author                                        |
| --repo-url        | Prompts User | The URL to the repo                                                  |
| --repo-remote-url | Prompts User | The remote URL for pushing the repo to Git                           |
| --repo-docs-url   | Prompts User | The URL for the project docs                                         |
| --contact-email   | Prompts User | The email for contact                                                |
| --security-email  | Prompts User | The email for reporting sensitive issues                             |
| -n                | `None`       | Answer NO to all overwrite prompts                                   |
| -y                | `None`       | Answer YES to all overwrite prompts                                  |
| --dry-run         | `False`      | Whether to describe the changes that will be made without making any |
