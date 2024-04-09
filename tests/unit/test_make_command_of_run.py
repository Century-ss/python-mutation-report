import os

from scripts.make_command_of_run import main


class Test_MakeCommand:
    MUTMUT_RUN_SH_PATH = "tests/data/temporary/mutmut-run.sh"
    WORKSPACE_PATH = "/home/runner/work/python-mutation-report/python-mutation-report"

    def setup_method(self) -> None:
        if os.path.exists(self.MUTMUT_RUN_SH_PATH):
            os.remove(self.MUTMUT_RUN_SH_PATH)

    def test_pipenv_project(self) -> None:
        main(
            src_directory="pipenv-project/src",
            test_directory="pipenv-project/tests",
            workspace_path=self.WORKSPACE_PATH,
            temporary_directory="tests/data/temporary",
        )
        with open(self.MUTMUT_RUN_SH_PATH, "r") as f:
            actual = f.read()

        expected = (
            "mutmut run "
            + "--paths-to-mutate "
            + f"{self.WORKSPACE_PATH}/pipenv-project/src/calculator.py,"
            + f"{self.WORKSPACE_PATH}/pipenv-project/src/domain/book.py,"
            + f"{self.WORKSPACE_PATH}/pipenv-project/src/fizz_buzz.py "
            + "--tests-dir "
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/test_calculator.py,"
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/model/test_book.py,"
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/test_fizz_buzz.py "
            + "--runner "
            + "'python -m pytest -x --assert=plain "
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/test_calculator.py "
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/model/test_book.py "
            + f"{self.WORKSPACE_PATH}/pipenv-project/tests/test_fizz_buzz.py' "
            + "> tests/data/temporary/run.txt"
        )
        assert actual == expected
