import xml.etree.ElementTree as ET

import bs4

with open("temporary/run.txt", "r") as f:
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
tree = ET.parse("temporary/junit.xml")
root = tree.getroot()
line_number_dict = {
    testcase.attrib["name"]: testcase.attrib["line"] for testcase in root.iter("testcase")
}  # {"Mutant #3": "3"} Key: mutant id(ex.3), Value: line number

soup = bs4.BeautifulSoup(open("html/index.html"), "html.parser")
file_list = [{"href": a_tag["href"], "file_name": a_tag.get_text()} for a_tag in soup.find_all("a")]

for a_tag in soup.find_all("a"):
    a_tag.replace_with(a_tag.get_text())
sub_summary = str(soup)

mutants_per_file = ""
for file in file_list:
    content = bs4.BeautifulSoup(open(f"html/{file['href']}"), "html.parser")
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
            element = f"### Mutant id:{mutant_id}　Line:{line_number}\n```"

        if (
            content_children[index - 1].startswith("Mutant ")
            and content_children[index - 1][7:].isdigit()
        ):
            element = f"{element}\n```"

        code_blocks += element + "\n"

    mutants_per_file += (
        "<details><summary>" + file["file_name"] + "</summary>\n\n" + code_blocks + "</details>\n\n"
    )


PR_comment = (
    "<details><summary>"
    + main_summary
    + "</summary>\n\n"
    + "<br>\n\n"
    + legend_description
    + "\n\n"
    + sub_summary
    + "※ ⏰Timeout, 🤔Suspicious and 🔇Skipped are not shown in the table."
    + "\n<br>\n"
    + "\n<br>\n"
    + "※ 🔇Skipped are not shown in the list of mutants"
    + "\n\n"
    + mutants_per_file
    + "</details>"
)

with open("PR_comment.txt", "w") as f:
    f.write(PR_comment)
