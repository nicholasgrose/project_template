from scripts.venv_wrappers.build import build_configured_venv_from_repo_root


def main() -> None:
    """
    Bootstraps the generation_cli/ environment by creating a virtual environment and installing the dependencies.
    :return: None
    """
    build_configured_venv_from_repo_root("")

    print("Root environment ready.")


if __name__ == "__main__":
    main()
