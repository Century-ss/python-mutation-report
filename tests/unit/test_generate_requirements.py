import os

import pytest

from scripts.generate_requirements import main


class Test_GenerateRequirements:
    OUTPUT_FILE_PATH = "requirements.txt"

    def setup_method(self) -> None:
        if os.path.exists(self.OUTPUT_FILE_PATH):
            os.remove(self.OUTPUT_FILE_PATH)

    def teardown_method(self) -> None:
        if os.path.exists(self.OUTPUT_FILE_PATH):
            os.remove(self.OUTPUT_FILE_PATH)

    def _get_input_lock_file_path(self, lock_file_name: str) -> str:
        return os.path.join("tests/data/input/lockfile", lock_file_name)

    def test_pipenvのlockファイルはdevelopを優先してrequirementsを生成する(self) -> None:
        input_lock_file_path = self._get_input_lock_file_path("Pipfile.lock")
        main(lock_file_path=input_lock_file_path)
        with open(self.OUTPUT_FILE_PATH, "r") as f:
            actual = f.read()
        assert actual == ("beautifulsoup4==4.11.2\n" + "click==8.1.7\n" + "prettytable==3.10.0\n")

    def test_pipのlockファイルは同じ内容のファイルを生成する(
        self,
    ) -> None:
        input_lock_file_path = self._get_input_lock_file_path("requirements.txt")
        main(input_lock_file_path)
        with open(self.OUTPUT_FILE_PATH, "r") as f:
            actual = f.read()
        assert actual == ("beautifulsoup4==4.12.3\n" + "mutmut==2.4.4\n")

    def test_システム用のryeのlockファイルからmoduleのバージョンだけを抽出してrequirementsを生成する(
        self,
    ) -> None:
        input_lock_file_path = self._get_input_lock_file_path("requirements.lock")
        main(input_lock_file_path)
        with open(self.OUTPUT_FILE_PATH, "r") as f:
            actual = f.read()
        assert actual == ("beautifulsoup4==4.10.0\n" + "soupsieve==2.2\n")

    def test_開発用のryeのlockファイルからmoduleのバージョンだけを抽出してrequirementsを生成する(
        self,
    ) -> None:
        input_lock_file_path = self._get_input_lock_file_path("requirements-dev.lock")
        main(input_lock_file_path)
        with open(self.OUTPUT_FILE_PATH, "r") as f:
            actual = f.read()
        assert actual == (
            "beautifulsoup4==4.12.3\n"
            + "packaging==24.0\n"
            + "pytest==8.1.1\n"
            + "soupsieve==2.5\n"
        )

    def test_未知のlockファイルを指定するとValueErrorを送出する(self) -> None:
        input_lock_file_path = self._get_input_lock_file_path("unknown.lock")
        with pytest.raises(ValueError):
            main(input_lock_file_path)
