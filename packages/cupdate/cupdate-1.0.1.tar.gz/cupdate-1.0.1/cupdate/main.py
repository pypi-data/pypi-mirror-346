import contextlib
import os
import re
import subprocess
from datetime import datetime
from typing import Any, Optional

import requests
from tabulate import tabulate


def read_requirements(file_path: str) -> dict[str, str]:
    """
    Reads the requirements.txt and returns a dictionary with package and version.
    """
    requirements: dict[str, str] = {}
    if not os.path.exists(file_path):
        return requirements

    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "==" in line:
                package, version = line.split("==", 1)
                requirements[package.strip()] = version.strip()
            elif ">=" in line:
                package, version = line.split(">=", 1)
                requirements[package.strip()] = f">={version.strip()}"
            elif "<=" in line:
                package, version = line.split("<=", 1)
                requirements[package.strip()] = f"<={version.strip()}"
            else:
                requirements[line.strip()] = ""

    return requirements


def read_excluded_packages(config_path: str) -> set[str]:
    """
    Reads the cupdate.config.txt and returns a set of packages that should not be updated.
    """
    excluded: set[str] = set()
    if not os.path.exists(config_path):
        return excluded

    with open(config_path) as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                excluded.add(line)

    return excluded


def get_latest_versions(packages: list[str]) -> dict[str, dict[str, str]]:
    """
    Determines the latest versions for a list of packages with additional information.
    """
    package_info: dict[str, dict[str, str]] = {}

    for package in packages:
        try:
            # Get latest version
            result = subprocess.run(
                ["pip", "index", "versions", package], capture_output=True, text=True, check=True
            )
            output = result.stdout

            version_match = re.search(r"Available versions: ([\d\.]+)", output)
            latest_version = version_match.group(1) if version_match else None

            if latest_version:
                # Get package info from PyPI
                try:
                    response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
                    if response.status_code == 200:
                        pypi_data = response.json()

                        # Get project URL
                        project_url = (
                            pypi_data.get("info", {}).get("project_urls", {}).get("Homepage")
                            or pypi_data.get("info", {}).get("home_page")
                            or f"https://pypi.org/project/{package}/"
                        )

                        # Calculate release age
                        release_date = None
                        release_info: list[dict[str, str]] = pypi_data.get("releases", {}).get(
                            latest_version, []
                        )
                        if release_info and isinstance(release_info, list) and len(release_info) > 0:  # type: ignore[assignment]
                            upload_time = release_info[0].get("upload_time")
                            if upload_time:
                                try:
                                    # Try the format with seconds
                                    release_date = datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S")
                                except ValueError:
                                    with contextlib.suppress(ValueError):
                                        release_date = datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S.%f")

                        age = ""
                        if release_date:
                            delta = datetime.now() - release_date
                            days_ago = delta.days

                            if days_ago == 0:
                                # Check if it's truly today or just within 24h
                                hours_ago = delta.seconds // 3600
                                if hours_ago == 0:
                                    minutes_ago = (delta.seconds % 3600) // 60
                                    age = f"{minutes_ago} {'minute' if minutes_ago == 1 else 'minutes'}"
                                else:
                                    age = f"{hours_ago} {'hour' if hours_ago == 1 else 'hours'}"
                            elif days_ago == 1:
                                age = "1 day"
                            elif days_ago < 7:
                                age = f"{days_ago} days"
                            elif days_ago < 31:
                                weeks = days_ago // 7
                                age = f"{weeks} {'week' if weeks == 1 else 'weeks'}"
                            elif days_ago < 365:
                                months = days_ago // 30
                                age = f"{months} {'month' if months == 1 else 'months'}"
                            else:
                                years = days_ago // 365
                                age = f"{years} {'year' if years == 1 else 'years'}"

                        package_info[package] = {"version": latest_version, "url": project_url, "age": age}
                    else:
                        package_info[package] = {
                            "version": latest_version,
                            "url": f"https://pypi.org/project/{package}/",
                            "age": "",
                        }
                except Exception as e:
                    print(f"Warning: Error getting info for {package}: {str(e)}")
                    package_info[package] = {
                        "version": latest_version,
                        "url": f"https://pypi.org/project/{package}/",
                        "age": "",
                    }

        except subprocess.SubprocessError:
            print(f"Warning: Could not determine latest version for {package}.")

    return package_info


def update_requirements(requirements_path: str, config_path: Optional[str] = None) -> None:
    """
    Updates the requirements.txt with the latest versions, except for excluded packages.
    """
    requirements = read_requirements(requirements_path)
    excluded_packages: set[str] = read_excluded_packages(config_path) if config_path else set()

    packages_to_update: list[str] = [pkg for pkg in requirements if pkg not in excluded_packages]
    latest_packages_info = get_latest_versions(packages_to_update)

    updated_requirements: dict[str, str] = {}
    update_table: list[Any] = []
    updates_count = 0

    for package, version in requirements.items():
        if package in latest_packages_info:
            package_info = latest_packages_info[package]
            latest_version = package_info["version"]

            if latest_version and latest_version != version.replace(">=", "").replace("<=", ""):
                # Package needs update
                updates_count += 1

                # Store new version (preserve operators)
                if version.startswith(">="):
                    updated_requirements[package] = f">={latest_version}"
                elif version.startswith("<="):
                    updated_requirements[package] = f"<={latest_version}"
                else:
                    updated_requirements[package] = latest_version

                # Add row to update table
                update_table.append(
                    [
                        package,
                        version,
                        latest_version,
                        package_info.get("age", ""),
                        package_info.get("url", ""),
                    ]
                )
            else:
                # No update needed or same version
                updated_requirements[package] = version
        else:
            # Package not in updates (either excluded or error occurred)
            updated_requirements[package] = version

    # Write updated requirements
    with open(requirements_path, "w") as file:
        for package, version in updated_requirements.items():
            if version:
                operator = ""
                if version.startswith(">=") or version.startswith("<="):
                    operator = version[:2]
                    version = version[2:]
                else:
                    operator = "=="
                file.write(f"{package}{operator}{version}\n")
            else:
                file.write(f"{package}\n")

    # Print update table
    if update_table:
        headers = ["NAME", "OLD", "NEW", "AGE", "INFO"]
        print(tabulate(update_table, headers=headers, tablefmt="simple"))
        print(
            f"\n✨ requirements.txt updated with {updates_count} package{'s' if updates_count != 1 else ''}"
        )
    else:
        print("All packages are already up to date!")


def main():
    """
    Main function that is executed when the command is called.
    """
    cwd = os.getcwd()
    requirements_path = os.path.join(cwd, "requirements.txt")
    config_path = os.path.join(cwd, "cupdate.config.txt")

    if not os.path.exists(requirements_path):
        print(f"Error: {requirements_path} does not exist.")
        return

    config_exists = os.path.exists(config_path)
    if not config_exists:
        print(f"Note: {config_path} not found. All packages will be updated.")
    else:
        excluded = read_excluded_packages(config_path)
        if excluded:
            print(f"Note: {len(excluded)} package(s) excluded from update.")

    update_requirements(requirements_path, config_path if config_exists else None)


def cli_main():
    main()


if __name__ == "__main__":
    main()
