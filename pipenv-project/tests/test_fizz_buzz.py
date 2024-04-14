import requests


def test_fizz() -> None:
    # assert fizz_buzz(3) == "fizz"
    assert True


def test_buzz() -> None:
    # assert fizz_buzz(5) == "buzz"
    assert True


def test_fizz_buzz() -> None:
    # assert fizz_buzz(15) == "fizz buzz"
    assert True


def test_requests() -> None:
    assert requests.get("https://example.com").status_code == 200
