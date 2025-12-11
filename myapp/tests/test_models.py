import unittest
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from models.currency import Currency
from models.author import Author


class TestUserModel(unittest.TestCase):
    """Тесты модели User."""

    def test_user_creation(self):
        """Тест создания пользователя."""
        user = User(1, "Артём")

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Артём")

    def test_user_id_validation(self):
        """Тест валидации id пользователя."""
        # id должен быть положительным целым числом
        with self.assertRaises(ValueError) as ctx:
            User(0, "Артём")
        self.assertEqual(
            str(ctx.exception),
            "ID пользователя должен быть положительным целым числом"
        )

        user = User(1, "Артём")
        with self.assertRaises(ValueError) as ctx2:
            user.id = -5
        self.assertEqual(
            str(ctx2.exception),
            "ID пользователя должен быть положительным целым числом"
        )

    def test_user_name_validation(self):
        """Тест валидации имени пользователя."""
        with self.assertRaises(ValueError) as ctx:
            User(1, "")
        self.assertEqual(
            str(ctx.exception),
            "Имя пользователя не может быть пустым"
        )

        user = User(1, "Артём")
        with self.assertRaises(ValueError) as ctx2:
            user.name = "   "
        self.assertEqual(
            str(ctx2.exception),
            "Имя пользователя не может быть пустым"
        )

        # Корректное изменение имени
        user.name = "Мария"
        self.assertEqual(user.name, "Мария")


class TestCurrencyModel(unittest.TestCase):
    """Тесты модели Currency."""

    def test_currency_creation(self):
        """Тест создания валюты."""
        curr = Currency("840", "usd", "Доллар США", 90.5, 1)

        self.assertEqual(curr.num_code, "840")
        self.assertEqual(curr.char_code, "USD")  # код должен быть приведён к верхнему регистру
        self.assertEqual(curr.name, "Доллар США")
        self.assertEqual(curr.value, 90.5)
        self.assertEqual(curr.nominal, 1)

    def test_char_code_validation(self):
        """Тест валидации кода валюты (3 символа)."""
        with self.assertRaises(ValueError) as ctx:
            Currency("840", "US", "Доллар США", 90.5, 1)
        self.assertEqual(
            str(ctx.exception),
            "Код валюты должен состоять из 3 символов"
        )

        curr = Currency("840", "USD", "Доллар США", 90.5, 1)
        with self.assertRaises(ValueError) as ctx2:
            curr.char_code = "EURO"
        self.assertEqual(
            str(ctx2.exception),
            "Код валюты должен состоять из 3 символов"
        )

    def test_name_validation(self):
        """Тест валидации названия валюты."""
        with self.assertRaises(ValueError) as ctx:
            Currency("840", "USD", "", 90.5, 1)
        self.assertEqual(
            str(ctx.exception),
            "Название валюты не может быть пустым"
        )

        curr = Currency("840", "USD", "Доллар США", 90.5, 1)
        with self.assertRaises(ValueError) as ctx2:
            curr.name = "   "
        self.assertEqual(
            str(ctx2.exception),
            "Название валюты не может быть пустым"
        )

    def test_value_validation(self):
        """Тест валидации курса валюты (неотрицательный)."""
        with self.assertRaises(ValueError) as ctx:
            Currency("840", "USD", "Доллар США", -1.0, 1)
        self.assertEqual(
            str(ctx.exception),
            "Курс валюты не может быть отрицательным"
        )

        curr = Currency("840", "USD", "Доллар США", 0.0, 1)
        with self.assertRaises(ValueError) as ctx2:
            curr.value = -5
        self.assertEqual(
            str(ctx2.exception),
            "Курс валюты не может быть отрицательным"
        )

    def test_nominal_validation(self):
        """Тест валидации номинала (положительное целое)."""
        with self.assertRaises(ValueError) as ctx:
            Currency("840", "USD", "Доллар США", 90.0, 0)
        self.assertEqual(
            str(ctx.exception),
            "Номинал должен быть положительным целым числом"
        )

        curr = Currency("840", "USD", "Доллар США", 90.0, 1)
        with self.assertRaises(ValueError) as ctx2:
            curr.nominal = -10
        self.assertEqual(
            str(ctx2.exception),
            "Номинал должен быть положительным целым числом"
        )


class TestAuthorModel(unittest.TestCase):
    """Тесты модели Author."""

    def test_author_creation(self):
        """Тест создания автора."""
        author = Author("Мастеров Артём", "P3122")

        self.assertEqual(author.name, "Мастеров Артём")
        self.assertEqual(author.group, "P3122")

    def test_author_name_validation(self):
        """Тест валидации имени автора."""
        with self.assertRaises(ValueError) as ctx:
            Author("", "P3122")
        self.assertEqual(
            str(ctx.exception),
            "Имя автора не может быть пустым"
        )

        author = Author("Мастеров Артём", "P3122")
        with self.assertRaises(ValueError) as ctx2:
            author.name = "   "
        self.assertEqual(
            str(ctx2.exception),
            "Имя автора не может быть пустым"
        )

    def test_author_group_validation(self):
        """Тест валидации группы автора (не пустая строка)."""
        with self.assertRaises(ValueError) as ctx:
            Author("Мастеров Артём", "")
        self.assertEqual(
            str(ctx.exception),
            "Группа не может быть пустой"
        )

        author = Author("Мастеров Артём", "P3122")
        with self.assertRaises(ValueError) as ctx2:
            author.group = "   "
        self.assertEqual(
            str(ctx2.exception),
            "Группа не может быть пустой"
        )


if __name__ == '__main__':
    unittest.main()