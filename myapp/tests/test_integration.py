import unittest
from unittest.mock import MagicMock
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMyAppPages(unittest.TestCase):
    """
    Интеграционные тесты верхнего уровня для маршрутов в myapp:
    проверяем, что вызываются нужные шаблоны и контроллеры.
    """

    @classmethod
    def setUpClass(cls):
        # Импортируем myapp один раз
        # ВАЖНО: если на импортe идёт реальный запрос к API,
        # временно подставьте в myapp пустой dict для api_data
        import myapp
        cls.myapp = myapp

    def setUp(self):
        # Каждый тест будет работать с "пустым" обработчиком,
        # чтобы не поднимать реальный HTTP-сервер.
        from myapp import SimpleHTTPRequestHandler

        class DummyHandler(SimpleHTTPRequestHandler):
            def __init__(self):
                # Не вызываем родительский __init__, чтобы не требовался сокет
                pass

        self.HandlerClass = DummyHandler

        # Переопределяем глобальные шаблоны и контроллеры на моки
        self.myapp.template_index = MagicMock()
        self.myapp.template_author = MagicMock()
        self.myapp.template_users = MagicMock()
        self.myapp.template_user = MagicMock()
        self.myapp.template_currencies = MagicMock()

        self.myapp.db_controller = MagicMock()
        self.myapp.currency_controller = MagicMock()

    def _make_handler(self, path):
        """Создает фейковый обработчик с переопределённым _send_html."""
        handler = self.HandlerClass()
        handler.path = path
        handler._send_html = MagicMock()
        return handler

    def test_index_page_renders_index_template(self):
        """GET / должен рендерить index.html с данными приложения/автора."""
        handler = self._make_handler("/")

        # Настраиваем возвращаемое значение шаблона
        self.myapp.template_index.render.return_value = "<html>index</html>"

        handler.do_GET()

        # Проверяем, что шаблон вызван с правильными аргументами
        self.myapp.template_index.render.assert_called_once()
        kwargs = self.myapp.template_index.render.call_args.kwargs

        self.assertIn("app_name", kwargs)
        self.assertIn("app_version", kwargs)
        self.assertIn("author_name", kwargs)
        self.assertIn("group", kwargs)

        handler._send_html.assert_called_once_with("<html>index</html>")

    def test_author_page_renders_author_template(self):
        """GET /author должен рендерить author.html."""
        handler = self._make_handler("/author")
        self.myapp.template_author.render.return_value = "<html>author</html>"

        handler.do_GET()

        self.myapp.template_author.render.assert_called_once()
        handler._send_html.assert_called_once_with("<html>author</html>")

    def test_users_page_calls_get_users_and_renders_template(self):
        """GET /users вызывает db_controller.get_users и рендерит users.html."""
        handler = self._make_handler("/users")

        fake_users = [
            {"id": 1, "name": "Иван"},
            {"id": 2, "name": "Мария"},
        ]
        self.myapp.db_controller.get_users.return_value = fake_users
        self.myapp.template_users.render.return_value = "<html>users</html>"

        handler.do_GET()

        self.myapp.db_controller.get_users.assert_called_once()
        self.myapp.template_users.render.assert_called_once_with(users=fake_users)
        handler._send_html.assert_called_once_with("<html>users</html>")

    def test_user_page_success(self):
        """GET /user?id=1 при существующем пользователе рендерит user.html."""
        handler = self._make_handler("/user?id=1")

        fake_user = {
            "id": 1,
            "name": "Иван",
            "currencies": [],
        }
        self.myapp.db_controller.get_user_with_currencies.return_value = fake_user
        self.myapp.template_user.render.return_value = "<html>user</html>"

        handler.do_GET()

        self.myapp.db_controller.get_user_with_currencies.assert_called_once_with(1)
        self.myapp.template_user.render.assert_called_once_with(user=fake_user)
        handler._send_html.assert_called_once_with("<html>user</html>")

    def test_user_page_not_found(self):
        """GET /user?id=999 при отсутствии пользователя возвращает 404."""
        handler = self._make_handler("/user?id=999")

        self.myapp.db_controller.get_user_with_currencies.return_value = None

        handler.do_GET()

        # Проверяем, что _send_html был вызван с 404 статусом
        handler._send_html.assert_called_once()
        args, kwargs = handler._send_html.call_args
        self.assertIn("Пользователь не найден", args[0])
        self.assertEqual(kwargs.get("status"), 404)

    def test_currencies_page_lists_currencies(self):
        """GET /currencies вызывает currency_controller.list_currencies и рендерит currencies.html."""
        handler = self._make_handler("/currencies")

        fake_currencies = [
            {"id": 1, "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
            {"id": 2, "char_code": "EUR", "name": "Евро", "value": 95.0, "nominal": 1},
        ]
        self.myapp.currency_controller.list_currencies.return_value = fake_currencies
        self.myapp.template_currencies.render.return_value = "<html>currencies</html>"

        handler.do_GET()

        self.myapp.currency_controller.list_currencies.assert_called_once()
        self.myapp.template_currencies.render.assert_called_once_with(currencies=fake_currencies)
        handler._send_html.assert_called_once_with("<html>currencies</html>")

    def test_currency_delete_redirect(self):
        """GET /currency/delete?id=1 вызывает delete_currency и делает редирект."""
        handler = self._make_handler("/currency/delete?id=1")

        # Переопределяем методы редиректа
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        handler.do_GET()

        self.myapp.currency_controller.delete_currency.assert_called_once_with(1)
        handler.send_response.assert_called_once_with(303)
        handler.send_header.assert_any_call("Location", "/currencies")

    def test_currency_update_with_params(self):
        """GET /currency/update?code=USD&value=100 вызывает update_currency."""
        handler = self._make_handler("/currency/update?code=USD&value=100")

        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        handler.do_GET()

        self.myapp.currency_controller.update_currency.assert_called_once_with("USD", 100.0)
        handler.send_response.assert_called_once_with(303)
        handler.send_header.assert_any_call("Location", "/currencies")

    def test_not_found_route(self):
        """Неизвестный маршрут возвращает 404."""
        handler = self._make_handler("/unknown")

        handler.do_GET()

        handler._send_html.assert_called_once()
        args, kwargs = handler._send_html.call_args
        self.assertIn("404 Not Found", args[0])
        self.assertEqual(kwargs.get("status"), 404)


if __name__ == "__main__":
    unittest.main()