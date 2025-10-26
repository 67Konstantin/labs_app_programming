import unittest
from binary_divisible_by_three import is_divisible_by_three


class TestBinaryDivisibleByThree(unittest.TestCase):
    
    def test_divisible_zero(self):
        # Тестирование числа 0 (делится на 3)
        self.assertTrue(is_divisible_by_three("0"))
    
    def test_not_divisible_one(self):
        # Тестирование числа 1 (не делится на 3)
        with self.assertRaises(ValueError):
            is_divisible_by_three("1")
    
    def test_divisible_three(self):
        # Тестирование числа 3 (11 в двоичной, делится на 3)
        self.assertTrue(is_divisible_by_three("11"))
    
    def test_divisible_six(self):
        # Тестирование числа 6 (110 в двоичной, делится на 3)
        self.assertTrue(is_divisible_by_three("110"))
    
    def test_divisible_nine(self):
        # Тестирование числа 9 (1001 в двоичной, делится на 3)
        self.assertTrue(is_divisible_by_three("1001"))
    
    def test_divisible_twelve(self):
        # Тестирование числа 12 (1100 в двоичной, делится на 3)
        self.assertTrue(is_divisible_by_three("1100"))
    
    def test_divisible_fifteen(self):
        # Тестирование числа 15 (1111 в двоичной, делится на 3)
        self.assertTrue(is_divisible_by_three("1111"))
    
    def test_not_divisible_two(self):
        # Тестирование числа 2 (10 в двоичной, не делится на 3)
        with self.assertRaises(ValueError):
            is_divisible_by_three("10")
    
    def test_not_divisible_five(self):
        # Тестирование числа 5 (101 в двоичной, не делится на 3)
        with self.assertRaises(ValueError):
            is_divisible_by_three("101")
    
    def test_not_divisible_ten(self):
        # Тестирование числа 10 (1010 в двоичной, не делится на 3)
        with self.assertRaises(ValueError):
            is_divisible_by_three("1010")
    
    def test_invalid_characters(self):
        # Тестирование недопустимых символов
        with self.assertRaises(ValueError):
            is_divisible_by_three("123")
        with self.assertRaises(ValueError):
            is_divisible_by_three("abc")
        with self.assertRaises(ValueError):
            is_divisible_by_three("102")
    
    def test_empty_string(self):
        # Тестирование пустой строки
        with self.assertRaises(ValueError):
            is_divisible_by_three("")
    
    def test_ok_large_number(self):
        # Тестирование большого числа, кратного 3
        large_binary = "110"
        self.assertTrue(is_divisible_by_three(large_binary))


if __name__ == '__main__':
    unittest.main()
