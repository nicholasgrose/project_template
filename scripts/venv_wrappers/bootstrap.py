import subprocess
import sys
import venv
from pathlib import Path

from scripts.venv_wrappers.path import venv_python, find_repo_root


def create_virtual_environment(directory: Path) -> Path:
    """
    Creates a virtual environment in the specified directory.
    :param directory: The location of the directory to create the virtual environment in.
    :return: The path to the new virtual environment.
    """
    print("Creating virtual environment...")
    venv_dir = directory / ".venv"

    if venv_python(venv_dir).is_file():
        print("Virtual environment already exists.")
        return venv_dir

    venv.create(venv_dir, with_pip=True, clear=False, symlinks=True, upgrade_deps=True)

    return venv_dir


def install_virtual_environment_dependencies(directory: Path, venv_dir: Path) -> None:
    """
    Installs the dependencies for the virtual environment.
    :param directory: The location of the directory.
    :param venv_dir: The location of the virtual environment.
    :return: None
    """
    print("Installing dependencies...")
    venv_python_path = venv_python(venv_dir)
    subprocess.run([venv_python_path, "-m", "pip", "install", "-r", directory / "requirements.txt"], cwd=directory)


def build_configured_virtual_environment(directory: Path) -> None:
    """
    Builds and configures a virtual environment in a directory.

    This assumes the presence of a requirements.txt file in the directory.
    :param directory: The directory to build the environment in.
    :return: None
    """
    venv_dir = create_virtual_environment(directory)
    install_virtual_environment_dependencies(directory, venv_dir)


def build_configured_venv_from_repo_root(path: str) -> None:
    """
    Builds and configures a virtual environment in a directory relative to the repo root.
    :param path: The path to the directory relative to the repo root.
    :return: None
    """
    repo_root = find_repo_root()
    directory = repo_root / path if len(path.strip()) > 0 else repo_root
    build_configured_virtual_environment(directory)


def run() -> None:
    """
    Bootstraps the virtual environment at the specified path or the repo root if no path is specified.
    Returns: None
    """
    path = sys.argv[1] if len(sys.argv) > 1 else ""

    build_configured_venv_from_repo_root(path)


if __name__ == "__main__":
    run()
