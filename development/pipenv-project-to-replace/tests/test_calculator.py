from src.calculator import Calculator


def test_add() -> None:
    assert Calculator.add(1, 2) == 3


def test_subtract() -> None:
    assert Calculator.subtract(2, 1) == 1


def test_multiple() -> None:
    assert Calculator.multiple(2, 3) == 6
