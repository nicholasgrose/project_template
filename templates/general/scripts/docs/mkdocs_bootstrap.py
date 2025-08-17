from scripts.venv_wrappers.build import build_configured_venv_from_repo_root


def main() -> None:
    """
    Bootstraps the docs/ environment by creating a virtual environment and installing the dependencies.
    :return: None
    """
    build_configured_venv_from_repo_root("docs")

    print("Docs environment ready.")


if __name__ == "__main__":
    main()
