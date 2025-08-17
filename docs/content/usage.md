# Usage

## Requirements

Before installing, you need to have the following installed:

| Requirement                      | Why It's Used                                                                                                                |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| [Git](https://git-scm.com)       | Git is the version control system. If you don't know what this is, I wouldn't recommend using this template.                 |
| [Task](https://taskfile.dev)     | Task provides a simple, cross-platform, and declarative way to run setup scripts.                                            |
| [Python](https://www.python.org) | Python is a cross-platform scripting language, and it is required to use [mkdocs](https://www.mkdocs.org) for documentation. |

## Project Template Setup

### Clone the Template Repository

Run the following command to clone the template repository:

`git clone git@github.com:nicholasgrose/project_template.git`

### Bootstrap the Template Tools

Run the following command in your cloned template repo to bootstrap the template tools:

`task cli:bootstrap`

## Using the Template

### To Create a New Project

Run the following command to create a new project:

`task cli:new  --taskfile <TEMPLATE_TASKFILE_PATH>`

### To Add to an Existing Project

!!! warning
    This will potentially clobber existing files if they overlap with the template files.
    Look at the `templates/` directory to see what files are being overwritten.

Run the following command to add to an existing project:

`task cli:add --taskfile <TEMPLATE_TASKFILE_PATH>`
