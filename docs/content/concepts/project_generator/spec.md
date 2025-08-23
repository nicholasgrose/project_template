# Palimpsest Specification (v1)

This document defines the initial schema, features, operations, and workflows for the project generator.

## Versioning

- Schema version: `v1`
- Template features and files should carry their own version hints in comments where useful.
- The answer file records the template commit/version to power controlled updates.

## Answers Schema (v1)

This is the minimal, extensible structure used across stacks.

```yaml
yaml schemaVersion: v1
project:
  name: "awesome-tool"
  description: "One-line description"
  visibility: "public" # public | private | internal
vcs:
  provider: "github" # github | gitlab | gitea | none repo: "me/awesome-tool" # org/name create: false # when true, attempt to create/link the remote defaultBranch: "main"
docs:
  tool: "mkdocs" # mkdocs | none siteName: "Awesome Tool Docs" deploy: true # if supported by CI provider
ci:
  provider: "github" # github | gitlab | gitea | none workflows: - name: test on: [push, pull_request] matrix: python: ["3.12"]
language:
  name: "python" # python | rust | node | none version: "3.12" python: packageManager: "virtualenv" # virtualenv | uv | poetry | pip-tools lint: ["ruff"] typecheck: ["mypy"] test: ["pytest"] rust: edition: "2021" node: packageManager: "npm" # npm | pnpm | yarn
features:
  - editorconfig
  - git_attributes
  - codeowners
  - conventional_commits
  - release_please
  - pre_commit

metadata:
  tags: [ "cli", "tooling" ]
```

Notes:

- The `language.<name>` subsection is optional; only the active language block is relevant.
- `features` is an open-ended list; validation ensures compatibility.

## Validation Rules (partial)

- One of `language.name` in {python,rust,node,none}.
- If `docs.tool == mkdocs`, then `ci.provider` should support a deployment if `docs.deploy == true`.
- If `vcs.create == true`, then `vcs.provider != none` and credentials must be available.
- Feature compatibility:
    - `release_please` requires a supported CI provider.
    - `pre_commit` is language-agnostic but implies generating a .pre-commit-config.yaml.

## Feature Model

A feature:

- Owns the set of files/partials it generates.
- Can depend on other features or providers.
- Is gated by simple conditions in templates (e.g., `if "pre_commit" in features`).

Examples:

- editorconfig: generates `.editorconfig`.
- git_attributes: generates `.gitattributes`.
- pre_commit: generates `.pre-commit-config.yaml` and optional installation instructions.
- release_please: adds CI workflow files and release config.
- codeowners: generates `CODEOWNERS` with templated team values.

## Operations

- copy: create a new project at a target path using the answers file (or a preset).
- update: re-apply the template to an existing project using its recorded answers.
- pretend/plan: show which files and steps would change without applying them.
- validate: check answers against schema and feature compatibility rules.

Optional operations via hooks or a wrapper CLI:

- vcs:create: create remote repository and set git origin.
- deps:init: run initial language-specific bootstrap (e.g., `python -m venv .venv`).
- docs:deploy: ensure CI is set to publish docs if enabled.

## File Generation Guidelines

- Idempotency: running update repeatedly should not produce diffs unless answers change.
- Separation: prefer generating discrete files by feature (e.g., separate CI workflow files).
- Ownership markers: where partial-in-file updates are required, use comment sentinels, e.g.:
    - `# <gen:pre_commit>` ... `# </gen:pre_commit>`
- User override: clearly document safe areas for user edits to avoid merge pain.

## Hooks and Side Effects (Optional)

Hooks should be:

- Guarded by conditions in the answers.
- Idempotent (check before creating resources).
- Transparent (log what is being done and how to undo).

Examples:

- If `vcs.create`: run `gh repo create {{vcs.repo}} ...` and `git remote add origin ...`.
- If `language.name == python` and `packageManager == virtualenv`: create `.venv`.
- If `docs.tool == mkdocs` and `docs.deploy`: ensure CI workflow exists and references appropriate steps.

## Presets

Presets are curated answer files stored in the template repository. Examples:

- python-lib.yml
- python-app.yml
- rust-bin.yml
- node-lib.yml
- homelab-ansible.yml

Usage:

- copy with: `python -m pal new --template general --path <dest> --project-name "Name"`
- update in-place: `python -m pal add --template general --project-name "Name"`

## Workflows

New Project (from preset):

1) Choose preset; copy to destination.
2) (Optional) Create remote repo and set origin.
3) Run initial dependency/bootstrap tasks.
4) Push to remote.

Upgrade Existing Project:

1) Edit the Palimpsest answers file or use the pal CLI to enable/disable features.
2) Run `pretend` to preview changes.
3) Run `update` to apply.
4) Commit and push.

Switching Features:

1) Modify `features` list in answers.
2) Run `pretend` and then `update`.
3) Remove deprecated files if guided by feature rules.

## Security and Privacy

- Never store secrets or tokens in the answers file.
- Reference credentials via environment variables or system keychains.
- Hooks should fail gracefully when credentials are missing and explain resolution.

## AI-Coding Guidance (for tool alignment)

When an AI coding tool contributes to this repository or a generated project, it should:

- Respect the declarative answers as the source of truth.
- Prefer adding new, feature-specific files over modifying shared monoliths.
- Preserve ownership markers and avoid editing outside them.
- Keep hooks idempotent and side effect safe.
- Provide clear diffs and explanations for any template changes.
