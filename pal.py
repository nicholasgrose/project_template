import os
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError

from scripts.venv_wrappers.bootstrap import build_configured_venv_from_repo_root
from scripts.venv_wrappers.path import venv_python, find_repo_root

GENERATOR_MODULE = "pal"  # what will be run via python -m
LAUNCHER_VERSION = "2025.08.17.1"  # bump to force reinstallation of dependencies


def read_marker(venv_dir: Path) -> str | None:
    """
    Read the marker file indicating that the virtual environment has been created for a version.
    Args:
        venv_dir: The virtual environment directory.
    Returns: String version if found, None otherwise.
    """
    marker = venv_dir / ".version"
    return marker.read_text().strip() if marker.exists() else None


essential_doc = """
Note: This file replaces the former generate.py launcher. Users should run `python -m pal` normally.
This bootstrapper exists to self-manage the CLI virtualenv and invoke the pal package module.
"""


def write_marker(venv_dir: Path, version: str) -> None:
    """
    Write a marker file indicating that the virtual environment has been created for this version.
    Args:
        venv_dir: The directory of the virtual environment.
        version: The version to write.
    Returns: None
    """
    (venv_dir / ".version").write_text(version)


def needs_reinstall(venv_dir: Path) -> bool:
    """
    Determine if we need to reinstall the virtual environment.
    Args:
        venv_dir: The directory of the virtual environment.
    Returns: True if we need to reinstall, False otherwise.
    """
    return read_marker(venv_dir) != LAUNCHER_VERSION


def main() -> None:
    """
    Bootstrap the virtual environment if needed and run the pal CLI.
    Returns: None
    """
    project_root = find_repo_root()
    virtual_directory = project_root / GENERATOR_MODULE / ".venv"

    if needs_reinstall(virtual_directory):
        print("Setting up CLI environment (one-time)...", file=sys.stderr)
        build_configured_venv_from_repo_root(GENERATOR_MODULE)
        write_marker(virtual_directory, LAUNCHER_VERSION)

    virtual_python = venv_python(virtual_directory)

    try:
        env = dict(os.environ)
        env["PAL_BOOTSTRAPPED"] = "1"
        subprocess.check_call([str(virtual_python), "-m", GENERATOR_MODULE, *sys.argv[1:]], cwd=project_root, env=env)
    except CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
