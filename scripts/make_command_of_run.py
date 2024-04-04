import glob
import os


def main(src_directory, test_directory, workspace_path, temporary_directory) -> None:
    with open(os.path.join(temporary_directory, "PR_diff_filenames.txt"), "r") as f:
        changed_file_paths = [s.rstrip() for s in f.readlines()]

    changed_py_files_except_init = [
        {"name": os.path.basename(file_path), "relative_path": file_path}
        for file_path in changed_file_paths
        if file_path.endswith(".py") and not file_path.endswith("__init__.py")
    ]

    changed_src_files = [
        file
        for file in changed_py_files_except_init
        if file["relative_path"].startswith(src_directory) and not file["name"].startswith("test_")
    ]

    all_test_files = [
        {"name": os.path.basename(file_path), "relative_path": file_path}
        for file_path in glob.glob(os.path.join(test_directory, "**/*.py"), recursive=True)
        if os.path.basename(file_path).startswith("test_")
    ]

    file_paths_to_mutate = []
    file_paths_to_run_test = []

    for changed_src_file in changed_src_files:
        test_file_paths_match_to_src_filename = [
            test_file["relative_path"]
            for test_file in all_test_files
            if test_file["name"] == f"test_{changed_src_file['name']}"
        ]
        if len(test_file_paths_match_to_src_filename) > 0:
            file_paths_to_mutate.append(changed_src_file["relative_path"])
            file_paths_to_run_test.extend(test_file_paths_match_to_src_filename)
        else:
            print(f"Test file not found for {changed_src_file['name']}.")

    if len(file_paths_to_mutate) == 0 or len(file_paths_to_run_test) == 0:
        raise ValueError("Not found files to mutate or tests.")

    # NOTE: Use a path from root for cases where the src is outside the path of the test to be run.
    absolute_file_paths_to_mutate = [
        os.path.join(workspace_path, path) for path in file_paths_to_mutate
    ]
    absolute_file_paths_to_run_test = [
        os.path.join(workspace_path, path) for path in file_paths_to_run_test
    ]

    command = (
        f"mutmut run --paths-to-mutate {','.join(absolute_file_paths_to_mutate)}"
        + f" --tests-dir {','.join(absolute_file_paths_to_run_test)}"
        + f" --runner 'python -m pytest -x --assert=plain {' '.join(absolute_file_paths_to_run_test)}'"
        + f" > {temporary_directory}/run.txt"
    )
    # NOTE: python -m means to run the module,　for the explicitness of module execution and to automate path resolution.
    # NOTE: pytest -x means to stop running tests after the first failure.
    # NOTE: --assert=plain means to disable the assertion rewriting of pytest.

    with open(os.path.join(temporary_directory, "mutmut-run.sh"), "w") as f:
        f.write(command)


if __name__ == "__main__":
    SRC_DIRECTORY = os.environ.get("SRC_DIRECTORY")
    TEST_DIRECTORY = os.environ.get("TEST_DIRECTORY")
    COMPOSITE_ACTION_PATH = os.environ.get("COMPOSITE_ACTION_PATH")
    WORKSPACE_PATH = os.environ.get("WORKSPACE_PATH")

    if SRC_DIRECTORY is None:
        raise ValueError("src_directory is not set.")
    if TEST_DIRECTORY is None:
        raise ValueError("test_directory is not set.")
    if COMPOSITE_ACTION_PATH is None:
        raise ValueError("actions_path of github context is not found.")
    if WORKSPACE_PATH is None:
        raise ValueError("workspace of github context is not found.")

    SRC_DIRECTORY = SRC_DIRECTORY.removeprefix("./").removesuffix("/")
    TEST_DIRECTORY = TEST_DIRECTORY.removeprefix("./").removesuffix("/")

    TEMPORARY_DIRECTORY = os.path.join(COMPOSITE_ACTION_PATH, "temporary")

    main(
        src_directory=SRC_DIRECTORY,
        test_directory=TEST_DIRECTORY,
        workspace_path=WORKSPACE_PATH,
        temporary_directory=TEMPORARY_DIRECTORY,
    )
