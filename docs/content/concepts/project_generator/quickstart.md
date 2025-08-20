# Quickstart: Using the Project Generator

## Create from a preset

```bash
copier copy -a presets/python-lib.yml <template-repo> ./my-new-lib
```

## Preview changes to an existing repo

### Inside the generated project

```bash
copier update --pretend
```

### Apply updates after editing features

```bash
copier update
```

## Common toggles
- Enable docs: set `docs.tool: mkdocs` and `docs.deploy: true` if supported by your CI provider.
- Switch CI: set `ci.provider` to `github`, `gitlab`, or `gitea`.
- Add code quality: include `pre_commit`, `conventional_commits`, and `release_please` in `features`.
