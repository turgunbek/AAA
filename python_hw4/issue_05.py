import unittest
from unittest.mock import patch, Mock
from what_is_year_now import what_is_year_now


class TestWhatIsYearNow(unittest.TestCase):
    def test_valid_yyyy_mm_dd_format(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = \
                b'{"currentDateTime": "2023-10-30"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            year = what_is_year_now()
            self.assertEqual(year, 2023)

    def test_valid_dd_mm_yyyy_format(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = \
                b'{"currentDateTime": "30.10.2023"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            year = what_is_year_now()
            self.assertEqual(year, 2023)

    def test_invalid_format(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = \
                b'{"currentDateTime": "2023/10/30"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            with self.assertRaises(ValueError):
                what_is_year_now()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
