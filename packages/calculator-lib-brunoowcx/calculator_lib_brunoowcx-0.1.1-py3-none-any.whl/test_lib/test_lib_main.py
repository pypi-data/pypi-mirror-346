import pytest
from calculator_lib.operations import add, subtract, multiply, divide, square_root, power

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 4) == -4

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 10) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Divisão por zero não é permitida."):
        divide(10, 0)

def test_square_root():
    assert square_root(9) == 3.0
    assert square_root(0) == 0.0
    with pytest.raises(ValueError):
        square_root(-1)

def test_power():
    assert power(2, 3) == 8.0
    assert power(5, 0) == 1.0
    assert power(4, 0.5) == 2.0