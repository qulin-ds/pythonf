import sqlite3
from typing import List, Dict, Any, Tuple


class CurrencyRatesCRUD:
    """
    Контроллер работы с БД (SQLite в памяти) для таблиц user, currency, user_currency.
    """

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._cursor = conn.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            );
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
            """
        )
        self._conn.commit()

    # ----------------- CRUD для currency -----------------

    def _create(self, data: List[Dict[str, Any]]) -> None:
        """
        Создание нескольких валют.
        data: список словарей с ключами num_code, char_code, name, value, nominal.
        """
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        self._cursor.executemany(sql, data)
        self._conn.commit()

    def _read(self) -> List[Dict[str, Any]]:
        """Чтение всех валют (SELECT * FROM currency)."""
        sql = "SELECT id, num_code, char_code, name, value, nominal FROM currency"
        cur = self._cursor.execute(sql)
        rows = cur.fetchall()
        result: List[Dict[str, Any]] = []
        for r in rows:
            result.append(
                {
                    "id": r[0],
                    "num_code": r[1],
                    "char_code": r[2],
                    "name": r[3],
                    "value": r[4],
                    "nominal": r[5],
                }
            )
        return result

    def _update(self, changes: Dict[str, float]) -> None:
        """
        Обновление курса валют по коду.
        Пример: _update({'USD': 101.1, 'EUR': 90.5})
        """
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        params: List[Tuple[float, str]] = []
        for code, val in changes.items():
            params.append((float(val), code.upper()))
        self._cursor.executemany(sql, params)
        self._conn.commit()

    def _delete(self, currency_id: int) -> None:
        """Удаление валюты по id."""
        sql = "DELETE FROM currency WHERE id = ?"
        self._cursor.execute(sql, (currency_id,))
        self._conn.commit()

    # ----------------- Пользователи и подписки -----------------

    def seed_test_data(self) -> None:
        """Создаём тестовые данные: пользователя, валюты и подписки."""
        # 1. Пользователи
        self._cursor.execute("INSERT INTO user(name) VALUES (?)", ("Иван",))
        self._cursor.execute("INSERT INTO user(name) VALUES (?)", ("Мария",))
        self._conn.commit()

        # 2. Если валют ещё нет — создадим простые для примера
        cur = self._cursor.execute("SELECT COUNT(*) FROM currency")
        count = cur.fetchone()[0]
        if count == 0:
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
                    "value": 91.0,
                    "nominal": 1,
                },
                {
                    "num_code": "826",
                    "char_code": "GBP",
                    "name": "Фунт стерлингов",
                    "value": 100.0,
                    "nominal": 1,
                },
            ]
            self._create(data)

        # 3. Подписки: Иван -> USD, EUR; Мария -> EUR, GBP
        # Получаем id пользователей
        self._cursor.execute("SELECT id, name FROM user")
        users = {row[1]: row[0] for row in self._cursor.fetchall()}

        # Получаем id валют
        self._cursor.execute("SELECT id, char_code FROM currency")
        currencies = {row[1]: row[0] for row in self._cursor.fetchall()}

        subs = [
            (users["Иван"], currencies["USD"]),
            (users["Иван"], currencies["EUR"]),
            (users["Мария"], currencies["EUR"]),
            (users["Мария"], currencies["GBP"]),
        ]
        self._cursor.executemany(
            "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)", subs
        )
        self._conn.commit()

    def get_users(self) -> List[Dict[str, Any]]:
        cur = self._cursor.execute("SELECT id, name FROM user")
        return [{"id": row[0], "name": row[1]} for row in cur.fetchall()]

    def get_user_with_currencies(self, user_id: int) -> Dict[str, Any] | None:
        # Информация о пользователе
        cur = self._cursor.execute("SELECT id, name FROM user WHERE id = ?", (user_id,))
        user_row = cur.fetchone()
        if not user_row:
            return None

        # Валюты, на которые он подписан
        sql = """
            SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
            FROM user_currency uc
            JOIN currency c ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """
        cur = self._cursor.execute(sql, (user_id,))
        currencies = []
        for r in cur.fetchall():
            currencies.append(
                {
                    "id": r[0],
                    "num_code": r[1],
                    "char_code": r[2],
                    "name": r[3],
                    "value": r[4],
                    "nominal": r[5],
                }
            )
        return {
            "id": user_row[0],
            "name": user_row[1],
            "currencies": currencies,
        }