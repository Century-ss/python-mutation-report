import os

from scripts.reshape_result_for_PR_comment import main


class Test_ReshapeResult:
    PR_COMMENT_TXT_PATH = "tests/data/temporary/PR_comment.txt"

    def setup_method(self) -> None:
        if os.path.exists(self.PR_COMMENT_TXT_PATH):
            os.remove(self.PR_COMMENT_TXT_PATH)

    def teardown_method(self) -> None:
        if os.path.exists(self.PR_COMMENT_TXT_PATH):
            os.remove(self.PR_COMMENT_TXT_PATH)

    def _update_document(self, document: str) -> None:
        with open("docs/sample_summary_comment.md", "w") as f:
            f.write(document)

    def test_regression(self) -> None:
        main(
            temporary_directory="tests/data/temporary",
            prefix_to_remove="/home/runner/work/python-mutation-report/python-mutation-report"
            + "/",
        )
        with open(self.PR_COMMENT_TXT_PATH, "r") as f:
            actual = f.read()
        with open("tests/data/expected/PR_comment.txt", "r") as f:
            expected = f.read()

        assert actual == expected
        self._update_document(actual)
