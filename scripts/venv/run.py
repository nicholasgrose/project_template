import os
import platform
from pathlib import Path


def venv_python(venv_dir: Path) -> str:
    """
    Given the venv directory, returns the path to the python executable.
    :param venv_dir: The directory to the venv
    :return: The path to the python executable
    """
    return os.path.join(venv_dir, "Scripts" if platform.system() == "Windows" else "bin",
                        "python" + (".exe" if platform.system() == "Windows" else ""))


def find_repo_root() -> Path:
    """
    Finds the root of the repository by walking up directories until it finds the scripts directory.
    :return: The path to the repo root
    """
    file_path = Path(__file__).resolve().parent

    while file_path.name != "scripts":
        file_path = file_path.parent

    return file_path.parent
