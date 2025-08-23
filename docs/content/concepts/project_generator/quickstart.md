# Quickstart: Using Palimpsest

## Create from a preset

Using the built-in CLI:

```bash
python -m pal new --template general --path ./my-new-lib --project-name "My New Lib"
```

Tip: You can add optional metadata, for example:

```bash
python -m pal new \
  --template general \
  --path ./my-new-lib \
  --project-name "My New Lib" \
  --repo-name my-new-lib \
  --author "Your Name" \
  --repo-url "https://github.com/you/my-new-lib"
```

## Preview changes to an existing repo

From inside the target project directory:

```bash
python -m pal add --template general --dry-run --project-name "My Existing Project"
```

## Apply updates after editing features

When ready to write files, drop --dry-run:

```bash
python -m pal add --template general --project-name "My Existing Project"
```

## Common toggles
- Enable docs: set `docs.tool: mkdocs` and `docs.deploy: true` if supported by your CI provider.
- Switch CI: set `ci.provider` to `github`, `gitlab`, or `gitea`.
- Add code quality: include `pre_commit`, `conventional_commits`, and `release_please` in `features`.
