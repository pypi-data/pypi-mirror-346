def read_requirements(file_path: str) -> dict[str, str]:
    """
    Reads the requirements.txt and returns a dictionary with package and version.
    """
def read_excluded_packages(config_path: str) -> set[str]:
    """
    Reads the cupdate.config.txt and returns a set of packages that should not be updated.
    """
def get_latest_versions(packages: list[str]) -> dict[str, dict[str, str]]:
    """
    Determines the latest versions for a list of packages with additional information.
    """
def update_requirements(requirements_path: str, config_path: str | None = None) -> None:
    """
    Updates the requirements.txt with the latest versions, except for excluded packages.
    """
def main() -> None:
    """
    Main function that is executed when the command is called.
    """
def cli_main() -> None: ...
