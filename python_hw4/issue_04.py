from one_hot_encoder import fit_transform
import pytest


def test_empty_input():
    """
    Тест на случай TypeError - когда функция вызывается без аргументов
    """
    with pytest.raises(TypeError):
        fit_transform()


def test_single_arg_input():
    """
    Тест для случая, когда передается один аргумент
    """
    input_data = 'Moscow'
    expected_output = [('Moscow', [1])]
    assert fit_transform(input_data) == expected_output


def test_multiple_args_input():
    """Тест для случая, когда передаются несколько аргументов
    """
    input_data = ('Moscow', 'New York', 'Moscow', 'London')
    expected_output = [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]
    assert fit_transform(*input_data) == expected_output


def test_AssertionError():
    """
    Проверка на случай AssertionError - ошибка в длине бинарного
    представления
    """
    input_data = ('Moscow', 'New York', 'Moscow', 'London')
    expected_output = [
        ('Moscow', [0, 0, 0, 1]),
        ('New York', [0, 0, 1, 0]),
        ('Moscow', [0, 0, 0, 1]),
        ('London', [0, 1, 0, 0]),
    ]
    with pytest.raises(AssertionError):
        assert fit_transform(*input_data) == expected_output


def test_mixed_input_types():
    """
    Проверка на случай некорректного формата входных данных.
    Должен вызвать TypeError
    """
    input_data = ('Moscow', ['New York', 'Paris'])
    with pytest.raises(TypeError):
        fit_transform(*input_data)
