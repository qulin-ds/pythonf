import sys
from typing import List, Dict, Any

import requests


def get_currencies(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
    handle=sys.stdout,
) -> Dict[str, Any]:
    """
    Получает курсы валют с API ЦБ РФ.
    Возвращает словарь: код -> словарь с полями num_code, char_code, name, value, nominal.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        result: Dict[str, Any] = {}

        if "Valute" not in data:
            raise ValueError("В ответе API нет секции 'Valute'")

        for code in currency_codes:
            code = code.upper()
            if code in data["Valute"]:
                v = data["Valute"][code]
                result[code] = {
                    "num_code": v["NumCode"],
                    "char_code": v["CharCode"],
                    "name": v["Name"],
                    "value": float(v["Value"]),
                    "nominal": int(v["Nominal"]),
                }
        if not result:
            raise ValueError("Не найдено ни одной запрошенной валюты")
        return result

    except Exception as e:
        handle.write(f"Ошибка при запросе к API: {e}\n")
        # Можно вернуть пустой словарь — тогда дальше подставим тестовые данные
        return {}