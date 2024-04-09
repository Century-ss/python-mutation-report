import os
import re
import xml.etree.ElementTree as ET

import bs4


def main(temporary_directory, prefix_to_remove) -> None:
    with open(os.path.join(temporary_directory, "run.txt"), "r") as f:
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
    soup = bs4.BeautifulSoup(
        open(os.path.join(temporary_directory, "html/index.html")), "html.parser"
    )
    files = [
        {"href": a_tag["href"], "relative_path": a_tag.get_text().removeprefix(prefix_to_remove)}
        for a_tag in soup.find_all("a")
    ]

    COLUMNS_TO_DELETE = ["Total", "% killed"]
    COLUMNS_TO_CONVERT = {"Killed": "🎉 Killed", "Survived": "🙁 Survived"}
    table_contents = []

    for tr in soup.find_all("tr"):
        if tr.find("td") is None:
            # NOTE: Skip the first row because it is the header of the table.
            continue
        row_element = {
            column.get_text(): content.get_text()
            for column, content in zip(soup.find_all("th"), tr.find_all("td"))
        }
        table_contents.append(row_element)

    for row in table_contents:
        for column in COLUMNS_TO_DELETE:
            del row[column]

        row["File"] = row["File"].removeprefix(prefix_to_remove)

        for key, key_to_convert in COLUMNS_TO_CONVERT.items():
            row[key_to_convert] = row.pop(key)

        killed = int(row[COLUMNS_TO_CONVERT["Killed"]])
        survived = int(row[COLUMNS_TO_CONVERT["Survived"]])
        if killed + survived == 0:
            row["% killed/(killed + survived)"] = "-"
            continue

        row["% killed / (killed + survived)"] = "{:.2f}".format(
            (killed / (killed + survived) * 100)
        )

    table = bs4.BeautifulSoup(features="html.parser")
    table_tag = soup.new_tag("table", border="1")

    header_row = soup.new_tag("tr")
    for column in table_contents[0].keys():
        th_tag = soup.new_tag("th")
        th_tag.string = column
        header_row.append(th_tag)
    table_tag.append(header_row)

    for row in table_contents:
        row_tag = soup.new_tag("tr")
        for value in row.values():
            td_tag = soup.new_tag("td")
            td_tag.string = str(value)
            row_tag.append(td_tag)
        table_tag.append(row_tag)

    table.append(table_tag)
    sub_summary = str(table)

    with open(os.path.join(temporary_directory, "mutmut-run.sh"), "r") as f:
        run_command = f.read()
    matched_tests_dir = re.search(r"--tests-dir\s+([^ ]*)", run_command)
    if matched_tests_dir is not None:
        matched_absolute_test_paths = matched_tests_dir.group(1).split(",")
        matched_test_paths = [
            path.removeprefix(prefix_to_remove) for path in matched_absolute_test_paths
        ]
        test_paths_to_show = "- " + "\n- ".join(matched_test_paths)
    else:
        test_paths_to_show = "Not matched test directory"

    test_paths_of_sub_summary = (
        "<details><summary>"
        + "List of tests used for mutation"
        + "</summary>\n\n"
        + test_paths_to_show
        + "\n</details>\n\n"
    )

    tree = ET.parse(os.path.join(temporary_directory, "junit.xml"))
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
            if element == prefix_to_remove + file["relative_path"]:
                # NOTE: Skip the first line because it is the file path as below.
                # '/home/runner/work/python-mutation-report/python-mutation-report/pipenv-project/src/calculator.py'
                continue
            if re.match(r"Killed \d+ out of \d+ mutants", element) is not None:
                # NOTE: Skip the line because it is the summary of the file as below.
                # 'Killed 2 out of 6 mutants'
                continue
            if element in ["Survived", "Timeouts", "Suspicious"]:
                element = f"## {element}"

            if element.startswith("Mutant ") and element[7:].isdigit():
                mutant_id = int(element[7:])
                line_number = line_number_dict[f"Mutant #{mutant_id}"]
                element = f"### Line number:{line_number}\n```python"

            if (
                content_children[index - 1].startswith("Mutant ")
                and content_children[index - 1][7:].isdigit()
            ):
                diff_file_pattern = re.compile(r"^[-+]{3} " + re.escape(prefix_to_remove))
                code_block = "\n".join(
                    line for line in element.split("\n") if not diff_file_pattern.match(line)
                )
                element = f"{code_block}\n```"

            code_blocks += element + "\n"

        if code_blocks == "":
            continue
        else:
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
        # + "※ ⏰Timeout, 🤔Suspicious and 🔇Skipped are not shown in the table."
        + "\n<br>\n"
        + "※ 🙁 Survived, ⏰Timeout, 🤔Suspicious are shown below."
        + "\n\n"
        + mutants_per_file
        + "</details>"
    )

    with open(os.path.join(temporary_directory, "PR_comment.txt"), "w") as f:
        f.write(PR_comment)


if __name__ == "__main__":
    COMPOSITE_ACTION_PATH = os.environ.get("COMPOSITE_ACTION_PATH")
    WORKSPACE_PATH = os.environ.get("WORKSPACE_PATH")

    if COMPOSITE_ACTION_PATH is None:
        raise ValueError("actions_path of github context is not found.")
    if WORKSPACE_PATH is None:
        raise ValueError("workspace of github context is not found.")

    TEMPORARY_DIRECTORY = os.path.join(COMPOSITE_ACTION_PATH, "temporary")
    PREFIX_TO_REMOVE = WORKSPACE_PATH + "/"

    main(
        temporary_directory=TEMPORARY_DIRECTORY,
        prefix_to_remove=PREFIX_TO_REMOVE,
    )
