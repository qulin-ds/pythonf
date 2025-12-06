import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App
from controllers import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from utils import get_currencies


# --------- Инициализация моделей и БД ---------

main_author = Author("Masterov Artem", "P3122")
app = App("CurrenciesListApp", "1.0", main_author)

# База в памяти
conn = sqlite3.connect(":memory:", check_same_thread=False)
db_controller = CurrencyRatesCRUD(conn)

# Попытаемся получить курсы USD, EUR, GBP из API
api_data = get_currencies(["USD", "EUR", "GBP"])
if api_data:
    # конвертируем в формат для _create
    data = []
    for code, v in api_data.items():
        data.append(
            {
                "num_code": v["num_code"],
                "char_code": v["char_code"],
                "name": v["name"],
                "value": v["value"],
                "nominal": v["nominal"],
            }
        )
    db_controller._create(data)

# Тестовые данные (пользователи, подписки, базовые валюты, если их нет)
db_controller.seed_test_data()

currency_controller = CurrencyController(db_controller)

# --------- Jinja2 Environment ---------

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_author = env.get_template("author.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")


# --------- HTTP обработчик ---------

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Главная
        if path == "/":
            html = template_index.render(
                app_name=app.name,
                app_version=app.version,
                author_name=main_author.name,
                group=main_author.group,
            )
            self._send_html(html)
            return

        # Автор
        if path == "/author":
            html = template_author.render(
                author_name=main_author.name,
                group=main_author.group,
            )
            self._send_html(html)
            return

        # Список пользователей
        if path == "/users":
            users = db_controller.get_users()
            html = template_users.render(users=users)
            self._send_html(html)
            return

        # Один пользователь
        if path == "/user":
            try:
                user_id = int(params.get("id", [0])[0])
            except ValueError:
                user_id = 0

            user_info = db_controller.get_user_with_currencies(user_id)
            if not user_info:
                self._send_html("<h1>Пользователь не найден</h1>", status=404)
                return

            html = template_user.render(user=user_info)
            self._send_html(html)
            return

        # Список валют
        if path == "/currencies":
            currencies = currency_controller.list_currencies()
            html = template_currencies.render(currencies=currencies)
            self._send_html(html)
            return

        # Удаление валюты
        if path == "/currency/delete":
            try:
                currency_id = int(params.get("id", [0])[0])
                currency_controller.delete_currency(currency_id)
            except ValueError:
                pass
            # редирект обратно на список
            self.send_response(303)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        # Обновление курса валюты
        if path == "/currency/update":
            changes = {}

            # Вариант 1: /currency/update?code=USD&value=100
            code = params.get("code", [None])[0]
            value = params.get("value", [None])[0]
            if code and value:
                try:
                    changes[code.upper()] = float(value)
                except ValueError:
                    pass

            # Вариант 2: /currency/update?USD=100
            if not changes:
                for k, v in params.items():
                    # k = 'USD', v = ['100']
                    try:
                        changes[k.upper()] = float(v[0])
                    except ValueError:
                        continue

            if changes:
                currency_controller.update_currency(
                    list(changes.keys())[0],
                    list(changes.values())[0],
                )

            self.send_response(303)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        # Показать валюты в консоль (для отладки)
        if path == "/currency/show":
            print("Текущие валюты в БД:")
            for row in db_controller._read():
                print(row)
            self._send_html("<h1>См. консоль сервера</h1>")
            return

        # Если маршрут не найден
        self._send_html("<h1>404 Not Found</h1>", status=404)


if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    print("Сервер запущен: http://localhost:8080")
    print("Маршруты:")
    print("  /             - главная")
    print("  /author       - автор")
    print("  /users        - список пользователей")
    print("  /user?id=1    - пользователь и его валюты")
    print("  /currencies   - список валют")
    print("  /currency/delete?id=...   - удалить валюту")
    print("  /currency/update?USD=100  - обновить курс")
    print("  /currency/show            - вывести валюты в консоль")
    httpd.serve_forever()