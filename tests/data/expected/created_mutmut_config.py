
changed_lines_per_file = {'/workspace/.github/CONTRIBUTING_mv.md': [], '/workspace/.github/workflows/test-actions-on-PR.yml': [5, 6, 7, 8, 12, 20, 21, 22, 23, 24, 25, 26, 27, 28], '/workspace/README.md': [2, 5, 14, 57], '/workspace/action.yml': [], '/workspace/docs/sample_summary_comment.md': [], '/workspace/docs/sample_summary_comment_mv.md': [], '/workspace/pipenv-project/src/calculator.py': [4, 8, 12], '/workspace/pipenv-project/src/domain/book.py': [4, 7], '/workspace/pipenv-project/src/fizz_buzz.py': [2, 3, 8, 9], '/workspace/pipenv-project/src/shop.py': [2, 3, 16], '/workspace/pipenv-project/tests/model/test_book.py': [7], '/workspace/pipenv-project/tests/test_drinv_mv_only.py': [], '/workspace/pipenv-project/tests/test_fizz_buzz.py': [6, 7]}

def pre_mutation(context) -> None:
    if (context.current_line_index + 1) not in changed_lines_per_file[context.filename]:
        context.skip = True

