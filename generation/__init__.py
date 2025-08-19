"""
Generation CLI package.

This package is invoked by the repository's self-bootstrapping launcher (generate.py),
which ensures a virtual environment exists in generation_cli/.venv and installs
pinned dependencies from generation_cli/requirements.txt.

Entrypoints:
- python -m generation_cli -> runs the click-based CLI (see __main__.py)

Commands exposed by the CLI (see docs/content/usage.md):
- new: create a new project from templates/<template>
- add: add template files into an existing project directory

Template variables expected by templates/general/*.j2:
- project_name, repo_name, repo_url, author, repo_remote_url (provided even if unused)

Design notes:
- We keep functions short and focused (see guidelines) and document behavior succinctly.
- We avoid tight coupling: template root resolution and file rendering are pure functions.
"""
