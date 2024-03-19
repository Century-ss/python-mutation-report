import json
import os

lock_file_path = os.environ.get("LOCK_FILE_PATH", "Pipfile.lock")

with open(lock_file_path, "r") as f:
    lock_file = json.load(f)

""
try:
    packages = dict(**lock_file["default"], **lock_file["develop"])
except TypeError as e:
    print(e)
    print("Duplicate packages have priority over the develop version.")
    packages = lock_file["default"] | lock_file["develop"]


with open("requirements.txt", "w") as f:
    for package, info in packages.items():
        version = info["version"] if "version" in info else ""
        f.write(f"{package}{version}\n")
