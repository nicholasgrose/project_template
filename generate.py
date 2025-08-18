import os
import sys
import subprocess
from pathlib import Path

import scripts.generation_cli.venv_bootstrap
from scripts.venv_wrappers.get_path import venv_python

GENERATOR_MODULE = "generation_cli"  # what will be run via python -m
LAUNCHER_VERSION = "2025.08.17.1"  # bump to force reinstallation of dependencies


def read_marker(venv_dir: Path) -> str | None:
    marker = venv_dir / ".version"
    return marker.read_text().strip() if marker.exists() else None


def write_marker(venv_dir: Path, value: str) -> None:
    (venv_dir / ".version").write_text(value)


def bootstrap_generator() -> None:
    scripts.generation_cli.venv_bootstrap.main()


def needs_reinstall(venv_dir: Path) -> bool:
    return read_marker(venv_dir) != LAUNCHER_VERSION


def main() -> None:
    project_root = Path(__file__).resolve().parent
    virtual_directory = project_root / GENERATOR_MODULE / ".venv"

    if needs_reinstall(virtual_directory):
        print("Setting up CLI environment (one-time)...", file=sys.stderr)
        bootstrap_generator()
        write_marker(virtual_directory, LAUNCHER_VERSION)

    virtual_python = venv_python(virtual_directory)

    # If we aren't already running under the venv interpreter, re-exec
    if Path(sys.executable).resolve() != virtual_python.resolve():
        os.execv(str(virtual_python), [str(virtual_python), "-m", GENERATOR_MODULE, *sys.argv[1:]])

    # If already in the venv (e.g., developer invoked with the venv python), just run it:
    subprocess.check_call([str(virtual_python), "-m", GENERATOR_MODULE, *sys.argv[1:]])


if __name__ == "__main__":
    main()
