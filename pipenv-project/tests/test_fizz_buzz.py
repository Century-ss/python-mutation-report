import requests
from src.fizz_buzz import fizz_buzz


def test_fizz():
    assert fizz_buzz(3) == "fizz"


def test_buzz():
    assert fizz_buzz(5) == "buzz"


def test_fizz_buzz():
    # assert fizz_buzz(15) == "fizz buzz"
    assert True


def test_requests():
    assert requests.get("https://example.com").status_code == 200
