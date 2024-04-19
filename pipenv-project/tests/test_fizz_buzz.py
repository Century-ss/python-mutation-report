import sympy
from src.fizz_buzz import fizz_buzz


def test_fizz() -> None:
    assert fizz_buzz(3) == "fizz"


def test_buzz() -> None:
    assert fizz_buzz(5) == "buzz"


def test_fizz_buzz() -> None:
    assert fizz_buzz(15) == "fizz buzz"


def test_sympy() -> None:
    assert sympy.isprime(3) is True
    assert sympy.isprime(4) is False
