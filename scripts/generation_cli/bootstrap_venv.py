from scripts.venv.build import build_configured_venv_from_repo_root


def main() -> None:
    """
    Bootstraps the generation_cli/ environment by creating a virtual environment and installing the dependencies.
    :return: None
    """

    build_configured_venv_from_repo_root("generation_cli")

    print("Generation_cli environment ready.")


if __name__ == "__main__":
    main()
