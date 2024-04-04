import os
import re
from typing import Dict, List


def extract_changed_lines(diff_text_lines: list, prefix_path: str) -> Dict[str, List[int]]:
    changed_lines: Dict[str, List[int]] = {}

    for line in diff_text_lines:
        if line.startswith("diff --git"):
            current_file = None
            current_line = None
            changed_start_line = None
            changed_end_line = None
            is_code_block = False

            matched_current_file = re.search(r"^diff --git a/.+ b/(.+)", line)
            if matched_current_file is None:
                raise ValueError(f"「{line}」 is invalid diff format.")
            current_file = os.path.join(prefix_path, matched_current_file.group(1))
            changed_lines[current_file] = []
            continue

        if line.startswith("@@"):
            match = re.search(r"^@@ -\d+,\d+ \+(\d+),(\d+) @@", line)
            if match is not None:
                changed_start_line = int(match.group(1))
                changed_end_line = int(match.group(1)) + int(match.group(2)) - 1
                current_line = changed_start_line
                is_code_block = True
                continue

        if is_code_block and isinstance(current_line, int) and isinstance(current_file, str):
            if line.startswith("-"):
                continue
            if not line.startswith("+"):
                current_line += 1
            else:
                if isinstance(changed_end_line, int) and current_line > changed_end_line:
                    raise ValueError(
                        f"filename:{current_file} current_line:{current_line} beyond the end of code block line:{changed_end_line}."
                    )

                changed_lines[current_file].append(current_line)
                current_line += 1

    return changed_lines


def get_pre_mutation_func_content(
    PR_diff_txt_path: str, prefix_path_to_convert_absolutely: str
) -> str:
    with open(PR_diff_txt_path, "r") as f:
        diff_text_lines = [line.strip() for line in f.readlines()]

    changed_lines_per_file = extract_changed_lines(
        diff_text_lines=diff_text_lines, prefix_path=prefix_path_to_convert_absolutely
    )

    file_content = f"""
changed_lines_per_file = {changed_lines_per_file}

def pre_mutation(context) -> None:
    if (context.current_line_index + 1) not in changed_lines_per_file[context.filename]:
        context.skip = True

"""

    return file_content


def main(workspace_path: str, mutmut_config_path: str, pr_diff_contents_path: str) -> None:
    if os.path.exists(mutmut_config_path):
        with open(mutmut_config_path, "r") as f:
            mutmut_config_content = f.read()

        if "def pre_mutation(" in mutmut_config_content:
            print("pre_mutation function already exists in mutmut_config.py.")
            print("So, plant mutants in the whole file, not just the change line.")
        else:
            pre_mutation_content = get_pre_mutation_func_content(
                PR_diff_txt_path=pr_diff_contents_path,
                prefix_path_to_convert_absolutely=workspace_path,
            )
            with open(mutmut_config_path, "a") as f:
                f.write(pre_mutation_content)
    else:
        pre_mutation_content = get_pre_mutation_func_content(
            PR_diff_txt_path=pr_diff_contents_path,
            prefix_path_to_convert_absolutely=workspace_path,
        )
        with open(mutmut_config_path, "w") as f:
            f.write(pre_mutation_content)


if __name__ == "__main__":
    WHERE_TO_RUN_TEST = os.environ.get("WHERE_TO_RUN_TEST", ".")
    WORKSPACE_PATH = os.environ.get("WORKSPACE_PATH")
    COMPOSITE_ACTION_PATH = os.environ.get("COMPOSITE_ACTION_PATH")

    if WORKSPACE_PATH is None:
        raise ValueError("workspace of github context is not found.")
    if COMPOSITE_ACTION_PATH is None:
        raise ValueError("actions_path of github context is not found.")

    MUTMUT_CONFIG_PATH = os.path.join(WHERE_TO_RUN_TEST, "mutmut_config.py")
    PR_DIFF_CONTENTS_PATH = os.path.join(COMPOSITE_ACTION_PATH, "temporary", "PR_diff_contents.txt")

    main(
        workspace_path=WORKSPACE_PATH,
        mutmut_config_path=MUTMUT_CONFIG_PATH,
        pr_diff_contents_path=PR_DIFF_CONTENTS_PATH,
    )
