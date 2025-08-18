# Nicholas's Project Template

## About

This is a repository to help me quickly start new projects.
If you like how it works, feel free to use it, though!

## Usage (minimal)

- Ensure Python 3.11+ is installed.
- Install Jinja2 in your environment (or run the Task that bootstraps the CLI env):
    - pip install jinja2
    - or: task cli:bootstrap

### Create a new project

- Run: python -m generation_cli.new_repo --project-name MyApp --repo-url https://github.com/me/myapp
- Options:
    - --template general (default)
    - --dest <path> (default creates a subdir under current working directory)
    - --author, --description, --extra KEY=VALUE ...
    - -o/--overwrite, -n/--dry-run

### Add to an existing repo

- From the target repository directory: python -m generation_cli.existing_repo --template general --overwrite

### Using Taskfile tasks

- task cli:new — bootstraps CLI env (if needed) and runs the new project generator.
- task cli:add — bootstraps CLI env (if needed) and adds the template to the current directory.

Templates are read from templates/<template_name> and rendered into the destination using Jinja2.
Files with extensions .j2/.jinja/.jinja2 have their extension stripped in output.


## Overwrite behavior

- If a destination file exists:
  - Protected files are never overwritten and you will not be prompted: LICENSE, README.md, .gitignore, .gitattributes, .idea/**
  - Otherwise you will be prompted to overwrite (default is No).
  - Passing -o/--overwrite overwrites without prompting.
- With -n/--dry-run, no prompts are shown; potential overwrites are shown as [OVERWRITE?], defaulting to No.
