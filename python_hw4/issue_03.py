from one_hot_encoder import fit_transform
import unittest


class TestFitTransformFunction(unittest.TestCase):

    def test_empty_input(self):
        """
        Проверка на случай пустого аргумента - должен вызвать TypeError
        """
        with self.assertRaises(TypeError):
            fit_transform()

    def test_single_arg_input(self):
        """
        Проверка на случай одного аргумента в виде строки
        """
        input_data = 'Moscow'
        expected_output = [('Moscow', [1])]
        self.assertEqual(fit_transform(input_data), expected_output)

    def test_multiple_args_input(self):
        """
        Проверка на случай нескольких аргументов в виде кортежа строк
        """
        input_data = ('Moscow', 'New York', 'Moscow', 'London')
        expected_output = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        self.assertEqual(fit_transform(*input_data), expected_output)

    def test_unique_args_input(self):
        """
        Проверка на случай, когда все токены уникальные"""
        input_data = ('Moscow', 'New York', 'London', 'Paris')
        expected_output = [
            ('Moscow', [0, 0, 0, 1]),
            ('New York', [0, 0, 1, 0]),
            ('London', [0, 1, 0, 0]),
            ('Paris', [1, 0, 0, 0]),
        ]
        self.assertEqual(fit_transform(*input_data), expected_output)

    def test_AssertionError(self):
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
        with self.assertRaises(AssertionError):
            self.assertEqual(fit_transform(*input_data), expected_output)

    def test_out_datatype(self):
        """
        Проверка на корректность типов данных резуьтата
        """
        input_data = ('Moscow', 'New York', 'Moscow', 'London')
        result = fit_transform(*input_data)
        for item in result:
            self.assertTrue(isinstance(item, tuple))
            self.assertTrue(isinstance(item[0], str))
            self.assertTrue(isinstance(item[1], list))
            self.assertTrue(all(isinstance(bit, int) for bit in item[1]))

    def test_mixed_input_types(self):
        """
        Проверка на случай некорректного формата входных данных.
        Должен вызвать TypeError
        """
        input_data = ('Moscow', ['New York', 'Paris'])
        with self.assertRaises(TypeError):
            fit_transform(*input_data)

    def test_element_not_in_result(self):
        """
        Проверка на случай AssertNotIn
        """
        input_data = ('Moscow', 'New York', 'Moscow', 'London')
        result = fit_transform(*input_data)
        element_to_check = ('Berlin', [1, 0, 0])  # не должен быть в результате
        self.assertNotIn(element_to_check, result)


if __name__ == '__main__':
    pass
