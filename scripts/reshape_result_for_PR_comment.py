with open("results/run_result.txt", "r") as f:
    run_result_rows = [s.rstrip() for s in f.readlines()]

with open("results/show_all_result.txt", "r") as f:
    show_all_result_rows = f.readlines()

final_run_result = run_result_rows[-1].split("  ")[1:]
number_of_legend = len(final_run_result)
summary_text = "Mutation Test Result　　" + "　　".join(final_run_result)

# TODO: no need to check if the legend is in the file, just add it?
# LEGEND_MARKER = "Legend for output:"
# if LEGEND_MARKER in run_result_rows:
#     legend_index = run_result_rows.index(LEGEND_MARKER)
#     legend_description = "\n".join(
#         run_result_rows[legend_index : legend_index + number_of_legend + 1]
#     )
# else:
legend_description = (
    "Legend for output:\n"
    + "🎉 Killed mutants.   The goal is for everything to end up in this bucket.\n"
    + "⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.\n"
    + "🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.\n"
    + "🙁 Survived.         This means your tests need to be expanded.\n"
    + "🔇 Skipped.          Skipped.\n"
)

mutant_codes = "".join(show_all_result_rows[7:])
####
contents = (
    "<details><summary>"
    + summary_text
    + "</summary>\n\n"
    + "```txt\n"
    + legend_description
    + "\n\n"
    + mutant_codes
    + "</details>"
)

with open("PR_comment.txt", "w") as f:
    f.write(contents)
