import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import sqlite3

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import CurrencyRatesCRUD

# Если пакет называется "utilits", используйте следующий импорт:
from utilits.currencies_api import get_currencies
# Если у вас папка называется "utils", замените строку выше на:
# from utils import get_currencies


class TestCurrencyController(unittest.TestCase):
    """Тесты контроллера валют CurrencyController (работа с абстрактной БД)."""

    def setUp(self):
        self.mock_db = MagicMock(spec=CurrencyRatesCRUD)
        self.controller = CurrencyController(self.mock_db)

    def test_list_currencies_calls_db_read(self):
        """Проверяем, что list_currencies делегирует вызов в db._read."""
        fake_rows = [
            {"id": 1, "num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
            {"id": 2, "num_code": "978", "char_code": "EUR", "name": "Евро", "value": 95.0, "nominal": 1},
        ]
        self.mock_db._read.return_value = fake_rows

        result = self.controller.list_currencies()

        self.mock_db._read.assert_called_once()
        self.assertEqual(result, fake_rows)
        self.assertEqual(len(result), 2)

    def test_update_currency_calls_db_update(self):
        """Проверяем, что update_currency вызывает db._update с правильными данными."""
        self.controller.update_currency("USD", 101.5)

        self.mock_db._update.assert_called_once_with({"USD": 101.5})

    def test_delete_currency_calls_db_delete(self):
        """Проверяем, что delete_currency вызывает db._delete с правильным id."""
        self.controller.delete_currency(3)

        self.mock_db._delete.assert_called_once_with(3)


class TestCurrencyRatesCRUD(unittest.TestCase):
    """Тесты работы с реальной in-memory SQLite для CurrencyRatesCRUD."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.crud = CurrencyRatesCRUD(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_create_and_read_currencies(self):
        """Проверяем, что _create добавляет валюты и _read их возвращает."""
        data = [
            {
                "num_code": "840",
                "char_code": "USD",
                "name": "Доллар США",
                "value": 90.0,
                "nominal": 1,
            },
            {
                "num_code": "978",
                "char_code": "EUR",
                "name": "Евро",
                "value": 95.0,
                "nominal": 1,
            },
        ]
        self.crud._create(data)

        rows = self.crud._read()

        self.assertEqual(len(rows), 2)
        codes = {r["char_code"] for r in rows}
        self.assertIn("USD", codes)
        self.assertIn("EUR", codes)

    def test_update_currency(self):
        """Проверяем, что _update обновляет курс по коду валюты."""
        data = [
            {
                "num_code": "840",
                "char_code": "USD",
                "name": "Доллар США",
                "value": 90.0,
                "nominal": 1,
            }
        ]
        self.crud._create(data)

        self.crud._update({"USD": 100.5})

        rows = self.crud._read()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["char_code"], "USD")
        self.assertEqual(rows[0]["value"], 100.5)

    def test_delete_currency(self):
        """Проверяем, что _delete удаляет валюту по id."""
        data = [
            {
                "num_code": "840",
                "char_code": "USD",
                "name": "Доллар США",
                "value": 90.0,
                "nominal": 1,
            }
        ]
        self.crud._create(data)
        rows = self.crud._read()
        self.assertEqual(len(rows), 1)
        currency_id = rows[0]["id"]

        self.crud._delete(currency_id)

        rows_after = self.crud._read()
        self.assertEqual(len(rows_after), 0)

    def test_seed_test_data_creates_users_and_subscriptions(self):
        """Проверяем, что seed_test_data создаёт пользователей, валюты и подписки."""
        self.crud.seed_test_data()

        cur = self.conn.cursor()

        cur.execute("SELECT COUNT(*) FROM user")
        users_count = cur.fetchone()[0]
        self.assertGreaterEqual(users_count, 2)

        cur.execute("SELECT COUNT(*) FROM currency")
        currencies_count = cur.fetchone()[0]
        self.assertGreater(currencies_count, 0)

        cur.execute("SELECT COUNT(*) FROM user_currency")
        subs_count = cur.fetchone()[0]
        self.assertGreater(subs_count, 0)

    def test_get_users(self):
        """Проверяем, что get_users возвращает список словарей с id и name."""
        self.crud.seed_test_data()
        users = self.crud.get_users()

        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIn("id", users[0])
        self.assertIn("name", users[0])

    def test_get_user_with_currencies_existing(self):
        """Пользователь существует — должны получить его и список валют."""
        self.crud.seed_test_data()
        users = self.crud.get_users()
        user_id = users[0]["id"]

        result = self.crud.get_user_with_currencies(user_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["id"], user_id)
        self.assertIn("currencies", result)
        self.assertIsInstance(result["currencies"], list)

    def test_get_user_with_currencies_not_existing(self):
        """Несуществующий пользователь — должно вернуться None."""
        result = self.crud.get_user_with_currencies(9999)
        self.assertIsNone(result)


class TestGetCurrenciesUtil(unittest.TestCase):
    """Тесты функции get_currencies из utilits.currencies_api."""

    @patch("utilits.currencies_api.requests.get")
    def test_get_currencies_success(self, mock_get):
        """Успешный ответ API — корректный парсинг валют."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Valute": {
                "USD": {
                    "NumCode": "840",
                    "CharCode": "USD",
                    "Name": "Доллар США",
                    "Value": 90.5,
                    "Nominal": 1,
                },
                "EUR": {
                    "NumCode": "978",
                    "CharCode": "EUR",
                    "Name": "Евро",
                    "Value": 98.2,
                    "Nominal": 1,
                },
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])

        mock_get.assert_called_once()
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertEqual(result["USD"]["num_code"], "840")
        self.assertEqual(result["USD"]["value"], 90.5)
        self.assertEqual(result["EUR"]["name"], "Евро")

    @patch("utilits.currencies_api.requests.get")
    def test_get_currencies_no_valute_section(self, mock_get):
        """Если в ответе нет 'Valute', функция должна вернуть пустой словарь."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = get_currencies(["USD"])

        self.assertEqual(result, {})

    @patch("utilits.currencies_api.requests.get")
    def test_get_currencies_exception(self, mock_get):
        """При ошибке запроса функция должна вернуть пустой словарь."""
        mock_get.side_effect = Exception("Network error")

        result = get_currencies(["USD"])

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()