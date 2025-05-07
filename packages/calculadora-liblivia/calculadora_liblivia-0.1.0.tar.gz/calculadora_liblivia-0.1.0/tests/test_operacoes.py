from calculadora import soma, subtracao, multiplicacao, divisao
import pytest

def test_soma():
    assert soma(2, 3) == 5

def test_subtracao():
    assert subtracao(5, 3) == 2

def test_multiplicacao():
    assert multiplicacao(2, 3) == 6

def test_divisao():
    assert divisao(6, 3) == 2

def test_divisao_zero():
    with pytest.raises(ValueError):
        divisao(5, 0)
