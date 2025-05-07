from calc_lib_jonathancastrosilva import adicao, subtracao, multiplicacao, divisao

def test_add():
    assert adicao(2, 3) == 5
    assert adicao(-1, 1) == 0
    assert adicao(0, 0) == 0

def subtracao():
    assert subtracao(5, 3) == 2
    assert subtracao(0, 4) == -4

def test_multiply():
    assert multiplicacao(3, 4) == 12
    assert multiplicacao(0, 10) == 0

def test_divide():
    assert divisao(10, 2) == 5
    assert divisao(9, 3) == 3

def test_divide_by_zero():
    with calc_lib_jonathancastrosilva.raises(ValueError, match="Divisão por zero não é permitida."):
        divisao(10, 0)