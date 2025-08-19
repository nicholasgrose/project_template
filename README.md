# Nicholas's Project Template

## About

This is a repository to help me quickly start new projects.
If you like how it works, feel free to use it, though!

## Documentation

See the [doc site](https://nicholasgrose.github.io/project_template/) for the documentation!

## Setup

If you would like to make changes to this repo, you can clone it and follow these instructions.

### Requirements

- [Python](https://www.python.org)
- [Task](https://taskfile.dev)

### Bootstrapping

After cloning, the project must be bootstrapped.

```shell
task bootstrap
```

### Docs

This repository has a [docs](docs) directory configured with [mkdocs](https://www.mkdocs.org) and
the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

To launch a local version of the documentation, you can run:

```shell
task docs:serve
```
