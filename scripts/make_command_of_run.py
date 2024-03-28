import glob
import os

src_directory = os.environ.get("SRC_DIRECTORY")
test_directory = os.environ.get("TEST_DIRECTORY")
where_to_run_test = os.environ.get("WHERE_TO_RUN_TEST", ".")
composite_action_path = os.environ.get("COMPOSITE_ACTION_PATH")

if src_directory is None:
    raise ValueError("src_directory is not set.")
if test_directory is None:
    raise ValueError("test_directory is not set.")
if composite_action_path is None:
    raise ValueError("actions_path of github context is not set.")

src_directory = src_directory.removeprefix("./")
test_directory = test_directory.removeprefix("./")
where_to_run_test = where_to_run_test.removeprefix("./")

temporary_directory = os.path.join(composite_action_path, "temporary")


with open(os.path.join(temporary_directory, "PR_diff_files.txt"), "r") as f:
    changed_file_paths = [s.rstrip() for s in f.readlines()]

changed_py_files_except_init = [
    {"name": os.path.basename(file_path), "path": file_path}
    for file_path in changed_file_paths
    if file_path.endswith(".py") and not file_path.endswith("__init__.py")
]

changed_src_files = [
    file
    for file in changed_py_files_except_init
    if file["path"].startswith(src_directory) and not file["name"].startswith("test_")
]
changed_test_files = [
    file
    for file in changed_py_files_except_init
    if file["path"].startswith(test_directory) and file["name"].startswith("test_")
]

all_src_files = [
    {"name": os.path.basename(file_path), "path": file_path}
    for file_path in glob.glob(os.path.join(src_directory, "**/*.py"), recursive=True)
    if not os.path.basename(file_path).startswith("test_")
]
all_test_files = [
    {"name": os.path.basename(file_path), "path": file_path}
    for file_path in glob.glob(os.path.join(test_directory, "**/*.py"), recursive=True)
    if os.path.basename(file_path).startswith("test_")
]

file_paths_to_mutate = []
file_paths_to_run_test = []

for changed_src_file in changed_src_files:
    test_file_paths_match_to_src_filename = [
        all_test_file["path"]
        for all_test_file in all_test_files
        if all_test_file["name"] == f"test_{changed_src_file['name']}"
    ]
    if len(test_file_paths_match_to_src_filename) > 0:
        file_paths_to_mutate.append(changed_src_file["path"])
        file_paths_to_run_test.extend(test_file_paths_match_to_src_filename)

for changed_test_file in changed_test_files:
    src_file_paths_match_to_test_filename = [
        all_src_file["path"]
        for all_src_file in all_src_files
        if all_src_file["name"] == changed_test_file["name"].removeprefix("test_")
    ]
    if len(src_file_paths_match_to_test_filename) > 0:
        file_paths_to_run_test.append(changed_test_file["path"])
        file_paths_to_mutate.extend(src_file_paths_match_to_test_filename)

if len(file_paths_to_mutate) == 0 or len(file_paths_to_run_test) == 0:
    raise ValueError("Not found files to mutate or tests.")

if where_to_run_test != ".":
    file_paths_to_mutate = [
        file_path.removeprefix(where_to_run_test).removeprefix("/")
        for file_path in file_paths_to_mutate
    ]
    file_paths_to_run_test = [
        file_path.removeprefix(where_to_run_test).removeprefix("/")
        for file_path in file_paths_to_run_test
    ]

command = (
    f"mutmut run --paths-to-mutate {','.join(file_paths_to_mutate)}"
    + f" --tests-dir {','.join(file_paths_to_run_test)}"
    + f" --runner 'python -m pytest -x --assert=plain {' '.join(file_paths_to_run_test)}'"
    + f" > {temporary_directory}/run.txt"
)

with open(os.path.join(temporary_directory, "mutmut-run.sh"), "w") as f:
    f.write(command)
