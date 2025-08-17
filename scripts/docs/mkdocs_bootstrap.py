import subprocess
import sys
from pathlib import Path

from scripts.venv.run import find_repo_root, venv_python


def main() -> None:
    """
    Bootstraps the docs/ environment by creating a virtual environment and installing the dependencies.
    :return: None
    """
    root = find_repo_root()
    docs_dir = root / "docs"

    venv_dir = create_virtual_environment(docs_dir)
    install_virtual_environment_dependencies(docs_dir, venv_dir)

    print("Docs environment ready.")


def create_virtual_environment(docs_dir: Path) -> Path:
    """
    Creates a virtual environment in the docs/ directory.
    :param docs_dir: The location of the docs/ directory.
    :return: The path to the new virtual environment.
    """
    print("Creating virtual environment...")
    venv_dir = docs_dir / ".venv"
    subprocess.run([sys.executable, "-m", "venv", venv_dir])

    return venv_dir


def install_virtual_environment_dependencies(docs_dir: Path, venv_dir: Path) -> None:
    """
    Installs the dependencies for the virtual environment.
    :param docs_dir: The location of the docs directory.
    :param venv_dir: The location of the virtual environment.
    :return: None
    """
    print("Installing dependencies...")
    venv_python_path = venv_python(venv_dir)
    subprocess.run([venv_python_path, "-m", "pip", "install", "-r", docs_dir / "requirements.txt"])


if __name__ == "__main__":
    main()
