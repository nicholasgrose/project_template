import os
import subprocess
import sys

from scripts.venv.run import find_repo_root, venv_python


def main() -> None:
    """
    A wrapper around mkdocs in the docs/ virtual environment.
    :return: None
    """
    root = find_repo_root()
    docs_dir = root / "docs"
    venv_dir = docs_dir / ".venv"
    python_executable = venv_python(venv_dir)
    mkdocs_command = [python_executable, "-m", "mkdocs"]

    if not os.path.exists(python_executable):
        print("MkDocs environment missing. Run: task docs:bootstrap", file=sys.stderr)
        sys.exit(1)

    try:
        # We need to redirect stderr to stdout because mkdocs prints logs to stderr.
        subprocess.call(mkdocs_command + sys.argv[1:], cwd=docs_dir, stderr=sys.stdout)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
