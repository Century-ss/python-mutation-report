import glob
import os

src_directory = os.environ.get("SRC_DIRECTORY")
test_directory = os.environ.get("TEST_DIRECTORY")
where_to_run_test = os.environ.get("WHERE_TO_RUN_TEST", ".")
actions_path = os.environ.get("COMPOSITE_ACTIONS_PATH")

if src_directory is None:
    raise ValueError("src_directory is not set.")
if test_directory is None:
    raise ValueError("test_directory is not set.")
if actions_path is None:
    raise ValueError("actions_path of github context is not set.")

temporary_directory = os.path.join(actions_path, "temporary")


with open(os.path.join(temporary_directory, "PR_diff_files.txt"), "r") as f:
    changed_files = [s.rstrip() for s in f.readlines()]

changed_py_files = [
    file for file in changed_files if file.endswith(".py") and not file.endswith("__init__.py")
]

changed_src_file_paths = [file for file in changed_py_files if file.startswith(src_directory)]
changed_test_file_paths = [file for file in changed_py_files if file.startswith(test_directory)]

changed_src_files = [
    {"filename": os.path.basename(file_path), "file_path": file_path}
    for file_path in changed_src_file_paths
]
changed_test_files = [
    {"filename": os.path.basename(file_path), "file_path": file_path}
    for file_path in changed_test_file_paths
]

all_src_file_paths = glob.glob(f"{src_directory}/**/*.py", recursive=True)
all_test_file_paths = glob.glob(f"{test_directory}/**/*.py", recursive=True)

file_paths_to_mutate = []
file_paths_to_run_test = []

for src_file in changed_src_files:
    test_file_paths_match_to_src_filename = [
        test_file_path
        for test_file_path in all_test_file_paths
        if test_file_path.endswith(f"test_{src_file['filename']}")
    ]
    if len(test_file_paths_match_to_src_filename) > 0:
        file_paths_to_mutate.append(src_file["file_path"])
        file_paths_to_run_test.extend(test_file_paths_match_to_src_filename)

for test_file in changed_test_files:
    src_file_paths_match_to_test_filename = [
        src_file_path
        for src_file_path in all_src_file_paths
        if src_file_path.endswith(test_file["filename"].removeprefix("test_"))
    ]
    if len(src_file_paths_match_to_test_filename) > 0:
        file_paths_to_run_test.append(test_file["file_path"])
        file_paths_to_mutate.extend(src_file_paths_match_to_test_filename)

if len(file_paths_to_mutate) == 0 or len(file_paths_to_run_test) == 0:
    raise ValueError("No files to mutate or tests.")

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
