<!--
You can read more about writing a README at https://www.makeareadme.com.
-->

# Palimpsest

## About

Palimpsest is a cross-stack project generator and template orchestrator.
It helps you create new repositories and evolve them over time with consistent standards.
If you like how it works, feel free to use it!

## Documentation

See the [doc site](https://nicholasgrose.github.io/palimpsest/) for the documentation!

## CLI

If you would like to make changes to this repo, you can clone it and follow these instructions.

### Requirements

- [Python](https://www.python.org)
- [Task](https://taskfile.dev)

### Using the CLI

Run the CLI via Python:

```shell
python -m pal --help
```

Create a new project:

```shell
python -m pal new --template general --path ./my-new-project --project-name "My New Project"
```

Preview adding files to an existing project:

```shell
python -m pal add --template general --dry-run --project-name "My Existing Project"
```

### Docs

This repository has a [docs](docs) directory configured with [MkDocs](https://www.mkdocs.org) and
the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

To launch a local version of the documentation, you can run:

```shell
task docs:serve
```

## License

This project is licensed under the [MIT License](LICENSE).

## Funding

This project is not currently accepting monetary donations.

The most valuable contribution you can make is your time and effort.
Contributions of code, documentation, and ideas are what help this project grow and thrive.

If you are interested in making a financial contribution to the open-source community, please consider donating to
non-profit organizations that support open-source software, such as
the [Software Freedom Conservancy](https://sfconservancy.org) or the [Open Source Initiative](https://opensource.org).

If you or your company uses this project, please consider letting us know. We would love to highlight your use case!
