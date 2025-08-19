import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# Constants
DEFAULT_TEMPLATE = "general"


@dataclass(frozen=True)
class RenderPlan:
    """Represents a single file render/copy action.

    Attributes:
        source: The source file in the templates tree
        target: The destination file path in the output tree
        is_template: Whether the source has a .j2 suffix and should be rendered
    """
    source: Path
    target: Path
    is_template: bool


def find_repo_root(start: Path) -> Path:
    """Ascend from the start until a directory containing 'templates' exists.

    This keeps the CLI resilient to being run from different working directories,
    but still within the repository checked out. If not found, falls back to start.
    """
    cur = start.resolve()
    for _ in range(10):  # safeguard to avoid walking the whole drive
        if (cur / "templates").is_dir():
            return cur
        nxt = cur.parent
        if nxt == cur:
            break
        cur = nxt
    return start.resolve()


def template_root(repo_root: Path, template: str) -> Path:
    """Return the path to the template directory, validating it exists."""
    root = repo_root / "templates" / template
    if not root.is_dir():
        raise click.ClickException(f"Template '{template}' not found at {root}")
    return root


def build_render_plan(src_root: Path, dest_root: Path) -> list[RenderPlan]:
    """Walk the template tree and produce a render plan for all files.

    - .j2 files are rendered, and the .j2 suffix is removed at destination.
    - Other files are copied verbatim.
    - Skips Python cache artifacts (e.g., __pycache__/ and *.pyc).
    - Directories are mirrored implicitly by ensuring parent dirs exist during application.
    """
    plans: list[RenderPlan] = []
    for path in src_root.rglob("*"):
        if path.is_dir():
            continue
        # Skip cache artifacts from accidentally committed sources in templates
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(src_root)
        is_tmpl = path.suffix == ".j2"
        target_rel = rel.with_suffix("") if is_tmpl else rel
        plans.append(RenderPlan(source=path, target=dest_root / target_rel, is_template=is_tmpl))
    return plans


def ensure_destination_for_new(dest: Path) -> None:
    """Ensure destination directory exists for 'new' command.

    Creates the directory if missing; raises if a non-directory exists.
    """
    if dest.exists() and not dest.is_dir():
        raise click.ClickException(f"Destination path exists and is not a directory: {dest}")
    dest.mkdir(parents=True, exist_ok=True)


def jinja_env(root: Path) -> Environment:
    """Create a strict Jinja2 environment rooted at the given template directory."""
    return Environment(
        loader=FileSystemLoader(root),
        undefined=StrictUndefined,  # error on missing variables to catch mismatches early
        autoescape=False,
        keep_trailing_newline=True,
        lstrip_blocks=False,
        trim_blocks=False,
    )


def apply_plan(
        env: Environment,
        plan: Iterable[RenderPlan],
        context: dict,
        dry_run: bool,
        confirm_overwrite: bool,
        always_overwrite: bool,
) -> None:
    """Apply the render plan to disk.

    - If dry_run, prints actions and returns without writing.
    - If `confirm_overwrite` is True, asks before replacing existing files.
    """
    for item in plan:
        action = "render" if item.is_template else "copy"
        exists = item.target.exists()
        if dry_run:
            click.echo(f"[DRY-RUN] {action}: {item.source} -> {item.target}")
            continue

        # Ensure directory exists
        item.target.parent.mkdir(parents=True, exist_ok=True)

        if exists and confirm_overwrite:
            if not click.confirm(f"File exists: {item.target}. Overwrite?", default=False):
                click.echo(f"Skipped existing file: {item.target}")
                continue

        if not confirm_overwrite and not always_overwrite:
            continue

        if item.is_template:
            template_rel = str(item.source)
            # Convert absolute path to loader-relative path
            # The loader is configured at the template root, so compute the relative path
            loader_root = Path(env.loader.searchpath[0])  # type: ignore[attr-defined]
            # This must be a POSIX path for Jinja to parse it properly
            template_name = Path(template_rel).resolve().relative_to(loader_root).as_posix()
            tpl = env.get_template(str(template_name))
            rendered = tpl.render(**context)
            item.target.write_text(rendered, encoding="utf-8")
        else:
            shutil.copy2(item.source, item.target)
        click.echo(f"Wrote {item.target}")


def normalize_context(
        project_name: str,
        repo_name: str,
        author: str,
        repo_url: str,
        repo_remote_url: str,
        repo_docs_url: str,
        contact_email: str,
        security_email: str,
) -> dict:
    """Build the context dict passed to templates, ensuring all expected keys exist.

    The templates currently reference: project_name, repo_name, repo_url, author.
    We also include repo_remote_url even if not used, to future-proof templates.
    """
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "project_name": project_name,
        "repo_name": repo_name if len(repo_name.strip()) < 0 else project_name,
        "author": author,
        "repo_url": repo_url,
        "repo_remote_url": repo_remote_url,
        "repo_docs_url": repo_docs_url,
        "contact_email": contact_email,
        "security_email": security_email,
    }


def prompt_missing_context(
        project_name: str,
        repo_name: str | None,
        author: str | None,
        repo_url: str | None,
        repo_remote_url: str | None,
        repo_docs_url: str | None,
        contact_email: str | None,
        security_email: str | None,
) -> dict:
    """Prompt the user for any missing context fields and return a normalized context dict.

    Rules:
    - repo_name defaults to project_name if not provided; we show that default in the prompt.
    - author, repo_url, repo_remote_url: prompt when missing; allow empty responses.
    """
    # repo_name: offer project_name as default if missing
    if repo_name in (None, ""):
        repo_name = click.prompt("Repository name", default=project_name, show_default=True)

    # author: prompt, allow empty
    if author is None:
        author = click.prompt("Author", default="", show_default=False)

    # repo_url: prompt, allow empty
    if repo_url is None:
        repo_url = click.prompt("Repository URL", default="", show_default=False)

    # repo_remote_url: prompt, allow empty
    if repo_remote_url is None:
        repo_remote_url = click.prompt("Remote URL for git origin", default="", show_default=False)

    # repo_docs_url: prompt, allow empty
    if repo_docs_url is None:
        repo_docs_url = click.prompt("URL for project docs", default="", show_default=False)

    # contact_email: prompt, allow empty
    if contact_email is None:
        contact_email = click.prompt("The email to suggest for contact", default="", show_default=False)

    # security_email: prompt, allow empty
    if security_email is None:
        security_email = click.prompt("The email to suggest for reporting sensitive issues", default="", show_default=False)

    return normalize_context(project_name, repo_name, author, repo_url, repo_remote_url, repo_docs_url, contact_email,
                             security_email)


def execute_render(template_name: str, dest_path: Path, context: dict, dry_run: bool,
                   always_overwrite: bool | None) -> None:
    """
    Common execution for both 'new' and 'add' commands: resolve paths, build plan, apply.
    Args:
        template_name: The name of the template to render.
        dest_path: The path to the destination directory.
        context: The context dict to pass to the template.
        dry_run: Whether to just show the proposed changes without executing them.
        always_overwrite: Whether to always overwrite existing files. None to prompt.
    Returns: None
    """
    repo_root = find_repo_root(Path.cwd())
    src_root = template_root(repo_root, template_name)

    env = jinja_env(src_root)
    plan = build_render_plan(src_root, dest_path)

    # Always confirm overwriting for safety in both commands
    apply_plan(env, plan, context, dry_run=dry_run, confirm_overwrite=always_overwrite is None,
               always_overwrite=always_overwrite if always_overwrite is not None else False)


@click.group(help="Project templating CLI. Creates or adds files from templates/ into a target directory.")
@click.version_option(package_name="generation_cli")
def cli() -> None:
    """Entrypoint for the click group."""
    pass


def validate_overwrite_behavior(answer_no: bool | None, answer_yes: bool | None) -> bool | None:
    """
    Validate the file overwrite behavior from the command line arguments.
    Args:
        answer_no: Whether the no flag was passed
        answer_yes: Whether the yes flag was passed
    Returns: The value to use for always_overwrite
    """
    will_always_overwrite = None

    if answer_yes and answer_no:
        raise click.ClickException("Cannot specify both --yes and --no to all overwrite prompts")
    elif answer_yes is not None:
        will_always_overwrite = True
    elif answer_no is not None:
        will_always_overwrite = False

    return will_always_overwrite


@cli.command(help="Create a new project from a template into a destination directory.")
@click.option("--template", "template_name", default=DEFAULT_TEMPLATE, show_default=True, help="Template to use")
@click.option("--path", "dest_path", type=click.Path(path_type=Path), help="Destination directory for the new project")
@click.option("--project-name", prompt=True, help="Project name to use in templating")
@click.option("--repo-name", default=None, help="Repository name (defaults to project_name)")
@click.option("--author", default=None, help="Author name")
@click.option("--repo-url", default=None, help="Repository URL")
@click.option("--repo-remote-url", default=None, help="Remote URL for git origin")
@click.option("--repo-docs-url", default=None, help="URL for the git docs")
@click.option("--contact-email", default=None, help="Email for contact")
@click.option("--security-email", default=None, help="Email for reporting security issues for git origin")
@click.option("-n", "--no", "answer_no", is_flag=True, default=None,
              help="Whether to answer NO to all overwrite prompts")
@click.option("-y", "--yes", "answer_yes", is_flag=True, default=None,
              help="Whether to answer YES to all overwrite prompts")
@click.option("--dry-run", is_flag=True, default=False, help="Describe actions without making any changes")
def new(template_name: str, dest_path: Path | None, project_name: str, repo_name: str | None, author: str | None,
        repo_url: str | None, repo_remote_url: str | None, repo_docs_url: str | None, contact_email: str | None,
        security_email: str | None, answer_no: bool | None, answer_yes: bool | None,
        dry_run: bool) -> None:
    always_overwrite = validate_overwrite_behavior(answer_no, answer_yes)

    if dest_path is None:
        dest_path = click.prompt("Destination path", type=click.Path(path_type=Path))

    dest_path = Path(dest_path)

    if not dry_run:
        ensure_destination_for_new(dest_path)

    # Prompt for missing optional fields and normalize context
    ctx = prompt_missing_context(project_name, repo_name, author, repo_url, repo_remote_url, repo_docs_url,
                                 contact_email, security_email)

    execute_render(template_name, dest_path, ctx, dry_run, always_overwrite)

    if not dry_run:
        run_bootstrap_task(dest_path)


def run_bootstrap_task(dest_path: Path) -> None:
    task_boostrap_command = [
        "task",
        "bootstrap",
    ]
    subprocess.check_call(task_boostrap_command, cwd=dest_path)


@cli.command(help="Add template files into an existing project directory.")
@click.option("--template", "template_name", default=DEFAULT_TEMPLATE, show_default=True, help="Template to use")
@click.option("--path", "dest_path", type=click.Path(path_type=Path), default=Path("."), show_default=True,
              help="Target project directory")
@click.option("--project-name", prompt=True, help="Project name to use in templating")
@click.option("--repo-name", default=None, help="Repository name (defaults to project_name)")
@click.option("--author", default=None, help="Author name")
@click.option("--repo-url", default=None, help="Repository URL")
@click.option("--repo-remote-url", default=None, help="Remote URL for git origin")
@click.option("--repo-docs-url", default=None, help="URL for the git docs")
@click.option("--contact-email", default=None, help="Email for contact")
@click.option("--security-email", default=None, help="Email for reporting security issues for git origin")
@click.option("-n", "--no", "answer_no", is_flag=True, default=None,
              help="Whether to answer NO to all overwrite prompts")
@click.option("-y", "--yes", "answer_yes", is_flag=True, default=None,
              help="Whether to answer YES to all overwrite prompts")
@click.option("--dry-run", is_flag=True, default=False, help="Describe actions without making any changes")
def add(template_name: str, dest_path: Path, project_name: str, repo_name: str | None, author: str | None,
        repo_url: str | None, repo_remote_url: str | None, repo_docs_url: str | None, contact_email: str | None,
        security_email: str | None, answer_no: bool | None, answer_yes: bool | None,
        dry_run: bool) -> None:
    always_overwrite = validate_overwrite_behavior(answer_no, answer_yes)

    dest_path = Path(dest_path)

    if not dest_path.exists() or not dest_path.is_dir():
        raise click.ClickException(f"Path does not exist or is not a directory: {dest_path}")

    # Prompt for missing optional fields and normalize context
    ctx = prompt_missing_context(project_name, repo_name, author, repo_url, repo_remote_url, repo_docs_url,
                                 contact_email, security_email)

    execute_render(template_name, dest_path, ctx, dry_run, always_overwrite)

    if not dry_run:
        run_bootstrap_task(dest_path)


def main() -> None:
    """Entrypoint for python -m generation_cli"""
    cli(standalone_mode=True)


if __name__ == "__main__":
    main()
