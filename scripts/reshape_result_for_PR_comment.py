import os
import re
import xml.etree.ElementTree as ET

import bs4

composite_action_path = os.environ.get("COMPOSITE_ACTION_PATH")
workspace_path = os.environ.get("WORKSPACE_PATH")

if composite_action_path is None:
    raise ValueError("actions_path of github context is not found.")
if workspace_path is None:
    raise ValueError("workspace of github context is not found.")

TEMPORARY_DIRECTORY = os.path.join(composite_action_path, "temporary")
PREFIX_TO_REMOVE = workspace_path + "/"

with open(os.path.join(TEMPORARY_DIRECTORY, "run.txt"), "r") as f:
    run_result_rows = [s.rstrip() for s in f.readlines()]

""" Make main summary text
"""
final_run_result = run_result_rows[-1].split("  ")[1:]
main_summary = "Mutation Test Result　　" + "　　".join(final_run_result)


legend_description = (
    "Legend for output:\n"
    + "🎉 Killed mutants.   The goal is for everything to end up in this bucket.\n"
    + "⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.\n"
    + "🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.\n"
    + "🙁 Survived.         This means your tests need to be expanded.\n"
    + "🔇 Skipped.          Skipped.\n"
)


""" Make sub summary and mutants
"""
soup = bs4.BeautifulSoup(open(os.path.join(TEMPORARY_DIRECTORY, "html/index.html")), "html.parser")
files = [
    {"href": a_tag["href"], "relative_path": a_tag.get_text().removeprefix(PREFIX_TO_REMOVE)}
    for a_tag in soup.find_all("a")
]

for a_tag in soup.find_all("a"):
    a_tag.replace_with(a_tag.get_text().removeprefix(PREFIX_TO_REMOVE))
sub_summary = str(soup)

with open(os.path.join(TEMPORARY_DIRECTORY, "mutmut-run.sh"), "r") as f:
    run_command = f.read()
matched_tests_dir = re.search(r"--tests-dir\s+([^ ]*)", run_command)
if matched_tests_dir is not None:
    matched_absolute_test_paths = matched_tests_dir.group(1).split(",")
    matched_test_paths = [
        path.removeprefix(PREFIX_TO_REMOVE) for path in matched_absolute_test_paths
    ]
    test_paths_to_show = "- " + "\n- ".join(matched_test_paths)
else:
    test_paths_to_show = "Not matched test directory"

test_paths_of_sub_summary = (
    "<details><summary>"
    + "List of test used for mutation"
    + "</summary>\n\n"
    + test_paths_to_show
    + "\n</details>\n\n"
)

tree = ET.parse(os.path.join(TEMPORARY_DIRECTORY, "junit.xml"))
root = tree.getroot()
line_number_dict = {
    testcase.attrib["name"]: testcase.attrib["line"] for testcase in root.iter("testcase")
}  # {"Mutant #3": "3"} Key: mutant id(ex.3), Value: line number

mutants_per_file = ""
for file in files:
    content = bs4.BeautifulSoup(open(file["href"]), "html.parser")
    content_children = list(content.stripped_strings)
    code_blocks = ""
    for index, element in enumerate(content_children):
        if index == 0:
            continue
        if element in ["Survived", "Timeouts", "Suspicious"]:
            element = f"## {element}"

        if element.startswith("Mutant ") and element[7:].isdigit():
            mutant_id = int(element[7:])
            line_number = line_number_dict[f"Mutant #{mutant_id}"]
            element = f"### Line number:{line_number}\n```"

        if (
            content_children[index - 1].startswith("Mutant ")
            and content_children[index - 1][7:].isdigit()
        ):
            code_block = element.replace(PREFIX_TO_REMOVE, "")
            element = f"{code_block}\n```"

        code_blocks += element + "\n"

    mutants_per_file += (
        "<details><summary>"
        + file["relative_path"]
        + "</summary>\n\n"
        + code_blocks
        + "</details>\n\n"
    )


PR_comment = (
    "<details><summary>"
    + main_summary
    + "</summary>\n\n"
    + "<br>\n\n"
    + legend_description
    + "\n\n"
    + sub_summary
    + "\n\n"
    + test_paths_of_sub_summary
    + "※ ⏰Timeout, 🤔Suspicious and 🔇Skipped are not shown in the table."
    + "\n<br>\n"
    + "※ 🔇Skipped are not shown in the list of mutants"
    + "\n\n"
    + mutants_per_file
    + "</details>"
)

with open(os.path.join(composite_action_path, "PR_comment.txt"), "w") as f:
    f.write(PR_comment)
