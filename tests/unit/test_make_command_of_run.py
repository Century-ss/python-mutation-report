import os

from scripts.make_command_of_run import main


class Test_MakeCommand:
    MUTMUT_RUN_SH_PATH = "tests/data/temporary/mutmut-run.sh"

    def setup_method(self) -> None:
        if os.path.exists(self.MUTMUT_RUN_SH_PATH):
            os.remove(self.MUTMUT_RUN_SH_PATH)

    def teardown_method(self) -> None:
        if os.path.exists(self.MUTMUT_RUN_SH_PATH):
            os.remove(self.MUTMUT_RUN_SH_PATH)

    def test_pipenv_project(self) -> None:
        main(
            src_directory="pipenv-project/src",
            test_directory="pipenv-project/tests",
            workspace_path="/workspace",
            temporary_directory="tests/data/temporary",
        )
        with open(self.MUTMUT_RUN_SH_PATH, "r") as f:
            actual = f.read()

        expected = (
            "mutmut run "
            + "--paths-to-mutate "
            + "/workspace/pipenv-project/src/calculator.py,"
            + "/workspace/pipenv-project/src/domain/book.py,/workspace/pipenv-project/src/fizz_buzz.py "
            + "--tests-dir "
            + "/workspace/pipenv-project/tests/test_calculator.py,"
            + "/workspace/pipenv-project/tests/model/test_book.py,"
            + "/workspace/pipenv-project/tests/test_fizz_buzz.py "
            + "--runner "
            + "'python -m pytest -x --assert=plain "
            + "/workspace/pipenv-project/tests/test_calculator.py "
            + "/workspace/pipenv-project/tests/model/test_book.py "
            + "/workspace/pipenv-project/tests/test_fizz_buzz.py' "
            + "> tests/data/temporary/run.txt"
        )
        assert actual == expected
