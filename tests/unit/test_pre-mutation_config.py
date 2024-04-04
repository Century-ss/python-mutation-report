import os

from scripts.generate_pre_mutation_config import main

EXPECTED_MUTMUT_CONFIG_CONTENT = """
changed_lines_per_file = {'/workspace/.github/CONTRIBUTING_mv.md': [], '/workspace/.github/workflows/test-actions-on-PR.yml': [5, 6, 7, 8, 12, 20, 21, 22, 23, 24, 25, 26, 27, 28], '/workspace/README.md': [2, 5, 14, 57], '/workspace/action.yml': [], '/workspace/docs/sample_summary_comment.md': [], '/workspace/docs/sample_summary_comment_mv.md': [], '/workspace/pipenv-project/src/calculator.py': [4, 8, 12], '/workspace/pipenv-project/src/domain/book.py': [4, 7], '/workspace/pipenv-project/src/fizz_buzz.py': [2, 3, 8, 9], '/workspace/pipenv-project/src/shop.py': [2, 3, 16], '/workspace/pipenv-project/tests/model/test_book.py': [7], '/workspace/pipenv-project/tests/test_drinv_mv_only.py': [], '/workspace/pipenv-project/tests/test_fizz_buzz.py': [6, 7]}

def pre_mutation(context) -> None:
    if (context.current_line_index + 1) not in changed_lines_per_file[context.filename]:
        context.skip = True


"""


class Test_GenerateMutmutConfig:
    MUTMUT_CONFIG_PATH = os.path.join("tests/data/where-to-run-test", "mutmut_config.py")
    PR_DIFF_CONTENTS_PATH = os.path.join("tests/data/temporary", "pr_diff_contents.txt")
    WORKSPACE_PATH = "/workspace"

    def setup_method(self) -> None:
        if os.path.exists(self.MUTMUT_CONFIG_PATH):
            os.remove(self.MUTMUT_CONFIG_PATH)

    def teardown_method(self) -> None:
        if os.path.exists(self.MUTMUT_CONFIG_PATH):
            os.remove(self.MUTMUT_CONFIG_PATH)

    def _get_expected_mutmut_config_path(self, filename: str) -> str:
        return os.path.join("tests/data/expected", filename)

    def test_configファイルが無かった場合にpre_mutation関数のあるconfigを作成する(
        self,
    ) -> None:
        main(
            workspace_path=self.WORKSPACE_PATH,
            mutmut_config_path=self.MUTMUT_CONFIG_PATH,
            pr_diff_contents_path=self.PR_DIFF_CONTENTS_PATH,
        )
        with open(self.MUTMUT_CONFIG_PATH, "r") as f:
            actual = f.read()

        with open(self._get_expected_mutmut_config_path("created_mutmut_config.py"), "r") as f:
            expected = f.read()

        assert actual == expected

    def test_configファイルが存在しpre_mutation関数がない場合pre_mutation関数を追記する(
        self,
    ) -> None:
        with open(self.MUTMUT_CONFIG_PATH, "w") as f:
            f.write("def init() -> None:\n    pass\n")

        main(
            workspace_path=self.WORKSPACE_PATH,
            mutmut_config_path=self.MUTMUT_CONFIG_PATH,
            pr_diff_contents_path=self.PR_DIFF_CONTENTS_PATH,
        )
        with open(self.MUTMUT_CONFIG_PATH, "r") as f:
            actual = f.read()

        with open(self._get_expected_mutmut_config_path("added_mutmut_config.py"), "r") as f:
            expected = f.read()

        assert actual == expected

    def test_configファイルが存在しpre_mutation関数がある場合は何も追記しない(self) -> None:
        with open(self.MUTMUT_CONFIG_PATH, "w") as f:
            f.write("def pre_mutation() -> None:\n    pass\n")

        main(
            workspace_path=self.WORKSPACE_PATH,
            mutmut_config_path=self.MUTMUT_CONFIG_PATH,
            pr_diff_contents_path=self.PR_DIFF_CONTENTS_PATH,
        )
        with open(self.MUTMUT_CONFIG_PATH, "r") as f:
            actual = f.read()

        with open(self._get_expected_mutmut_config_path("do_nothing_mutmut_config.py"), "r") as f:
            expected = f.read()

        assert actual == expected
