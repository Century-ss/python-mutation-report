import glob
import os

src_directory = os.environ.get("SRC_DIRECTORY")
test_directory = os.environ.get("TEST_DIRECTORY")

with open("temporary/PR_diff_files.txt", "r") as f:
    changed_files = [s.rstrip() for s in f.readlines()]

changed_py_files = [
    file for file in changed_files if file.endswith(".py") and not file.endswith("__init__.py")
]

if src_directory is None:
    raise ValueError("src_directory is not set.")
if test_directory is None:
    raise ValueError("test_directory is not set.")

changed_src_files = [file for file in changed_py_files if file.startswith(src_directory)]
changed_test_files = [file for file in changed_py_files if file.startswith(test_directory)]

changed_src_filenames = [file.split("/")[-1] for file in changed_src_files]
changed_test_filenames = [file.split("/")[-1] for file in changed_test_files]

all_src_files = glob.glob(f"{src_directory}/**/*.py", recursive=True)
all_test_files = glob.glob(f"{test_directory}/**/*.py", recursive=True)

# test_files_for_changed_src_filenames = [file for file in changed_src_filenames]
test_files_correspond_to_changed_src_filenames = []
for src_filename in changed_src_filenames:
    test_files_correspond_to_changed_src_filenames.extend(
        [test_file for test_file in all_test_files if test_file.endswith(f"test_{src_filename}")]
    )

src_files_correspond_to_changed_test_filenames = []
for test_filename in changed_test_filenames:
    src_files_correspond_to_changed_test_filenames.extend(
        [
            src_file
            for src_file in all_src_files
            if src_file.endswith(test_filename.replace("test_", ""))
        ]
    )

files_to_mutate = set(changed_src_files + src_files_correspond_to_changed_test_filenames)
files_to_run_test = set(changed_test_files + test_files_correspond_to_changed_src_filenames)

command = (
    f"mutmut run --paths-to-mutate {','.join(files_to_mutate)}"
    + f" --tests-dir {','.join(files_to_run_test)}"
    + f" --runner 'python -m pytest -x --assert=plain {' '.join(files_to_run_test)}'"
    + " > temporary/run.txt"
)

with open("temporary/mutmut-run.sh", "w") as f:
    f.write(command)

print("a")
