import json
import os
import re


def get_package_versions_from_pipenv(lock_file_path: str) -> str:
    with open(lock_file_path, "r") as f:
        lock_file = json.load(f)

    try:
        packages = dict(**lock_file["default"], **lock_file["develop"])
    except TypeError as e:
        print(e)
        print("Duplicate packages have priority over the develop version.")
        packages = lock_file["default"] | lock_file["develop"]

    package_versions = [
        f"{package}{info['version'] if 'version' in info else ''}\n"
        for package, info in packages.items()
    ]
    #
    return "".join(package_versions)


def get_package_versions_from_rye(lock_file_path: str) -> str:
    with open(lock_file_path, "r") as f:
        file_content = f.read()

    pattern = re.compile(r"^[^\s#][^\n]+==[^\n]+$", re.MULTILINE)
    matches = pattern.findall(file_content)

    return "\n".join(matches) + "\n"


def get_package_versions_from_pip(lock_file_path: str) -> str:
    with open(lock_file_path, "r") as f:
        file_contents = f.read()
    return file_contents


def main(lock_file_path) -> None:
    filename = os.path.basename(lock_file_path)

    if filename == "Pipfile.lock":
        package_versions = get_package_versions_from_pipenv(lock_file_path)
    elif filename == "requirements-dev.lock" or filename == "requirements.lock":
        package_versions = get_package_versions_from_rye(lock_file_path)
    elif filename == "requirements.txt":
        package_versions = get_package_versions_from_pip(lock_file_path)
    else:
        raise ValueError("Unknown lock file. Only pip, pipenv and rye lock files are supported.")

    with open("requirements.txt", "w") as f:
        f.write(package_versions)


if __name__ == "__main__":
    LOCK_FILE_PATH = os.environ.get("LOCK_FILE_PATH")
    if LOCK_FILE_PATH is None:
        raise ValueError("LOCK_FILE_PATH is not set.")

    main(lock_file_path=LOCK_FILE_PATH)
