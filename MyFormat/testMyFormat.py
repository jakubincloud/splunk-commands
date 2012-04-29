
from MyFormat.myformat import MyFormat

__author__ = 'jakub.zygmunt'

import unittest

class TestDiff(unittest.TestCase):

    def setUp(self):
        self.myformat = MyFormat()

    def test_get_no_args(self):
        input = expected = 'value'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_get_2digit_value(self):
        input = expected = '23'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_get_4digit_value(self):
        input = ' 3456'
        expected = ' 3 456'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_get_8digit_value(self):
        input = '12345678'
        expected = '12 345 678'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_get_4digit_with_text_value(self):
        input = '3456 GB'
        expected = '3 456 GB'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_invalid_digit_word(self):
        input = expected = 'db45663'
        output = self.myformat.format(input)
        self.assertEqual(expected, output)

    def test_format_string_invalid_digit_word(self):
        input = 'db45663'
        expected = 'db45 663'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)


    def test_get_2digit_with_sign(self):
        input = '23'
        expected = '+23'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_2digit_with_sign_false(self):
        input = '23'
        expected = '23'
        output = self.myformat.format(input, sign=False)
        self.assertEqual(expected, output)

    def test_get_0_with_sign(self):
        input = expected = '0'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def tet_get_4digit_with_sign(self):
        input = '4567'
        expected = '+4 567'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_invalid_with_sign(self):
        input = expected = 'db342eb'
        output = self.myformat.format(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_minus_2digit(self):
        input = expected = '-23'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_minus_4digit(self):
        input =  '-4567'
        expected = '-4 567'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_minus_8digit_with_suffix(self):
        input = '-12345678GiB'
        expected = '-12 345 678 GiB'
        output = self.myformat.format(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_minus_2digit_with_suffix(self):
        input = '-23'
        expected = "-23 suf"
        output = self.myformat.format_string(input, sign=True, suffix="suf")
        self.assertEqual(expected, output)

    def test_get_minus_4digit_with_word_and_suffix(self):
        input = '-2345GB'
        expected = "-2 345 suf"
        output = self.myformat.format(input, sign=True, suffix="suf")
        self.assertEqual(expected, output)

    def test_get_minus_8digit_with_empty_suffix(self):
        input = '-12345678'
        expected = "-12 345 678"
        output = self.myformat.format(input, sign=True, suffix="")
        self.assertEqual(expected, output)

    def test_get_minus_8digit_with_word_empty_suffix(self):
        input = '-12345678 GB'
        expected = "-12 345 678 GB"
        output = self.myformat.format_string(input, sign=True, suffix="")
        self.assertEqual(expected, output)

    def test_get_8digit_with_word_empty_suffix(self):
        input = '12345678 GB'
        expected = "12 345 678 GB"
        output = self.myformat.format_string(input, sign=False, suffix="")
        self.assertEqual(expected, output)

    def test_get_string_formatted_no_suffix(self):
        input = '8929 (available: 6705, in-use: 2078, error: 146)'
        expected = '8 929 (available: 6 705, in-use: 2 078, error: 146)'
        output = self.myformat.format_string(input)
        self.assertEqual(expected, output)

    def test_get_string_formatted_with_sign(self):
        input = '8929 (available: -6705, in-use: 2078, error: 146)'
        expected = '+8 929 (available: -6 705, in-use: +2 078, error: +146)'
        output = self.myformat.format_string(input, sign=True)
        self.assertEqual(expected, output)

    def test_get_string_formatted_suffix(self):
        input = '8929 (available: 6705, in-use: 2078, error: 146)'
        expected = '8 929 GB (available: 6 705 GB, in-use: 2 078 GB, error: 146 GB)'
        output = self.myformat.format_string(input, suffix='GB')
        self.assertEqual(expected, output)

    def test_get_string_formatted_with_sign_and_suffix(self):
        input = '8929 (available: -6705, in-use: 2078, error: 146)'
        expected = '+8 929 GiB (available: -6 705 GiB, in-use: +2 078 GiB, error: +146 GiB)'
        output = self.myformat.format_string(input, sign=True, suffix="GiB")
        self.assertEqual(expected, output)




