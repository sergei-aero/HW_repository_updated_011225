import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


def __init__(self):
    self.api_key = os.getenv("ForexAPIKey")
    self.base_url = "https://api.apilayer.com/exchangerates_data/latest"


def _get_exchange_rate(self, from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает курс обмена валюты к рублю через внешнее API

    Args:
        from_currency: Исходная валюта (например, "USD", "EUR", "GBP", "CNY")
        to_currency: Целевая валюта (по умолчанию "RUB")

    Returns:
        Курс обмена или None в случае ошибки

    Raises:
        ConnectionError: Если не удалось подключиться к API
        ValueError: Если API вернул некорректный ответ
    """
    if from_currency == to_currency:
        return 1.0

    if not self.api_key:
        raise ValueError("API ключ не найден. Установите ForexAPIKey в .env файле")

    headers = {"apikey": self.api_key}
    params = {"base": from_currency, "symbols": to_currency}

    try:
        response = requests.get(self.base_url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            raise ConnectionError(f"API вернул статус {response.status_code}. " f"Ответ: {response.text}")

        data = response.json()

        rates = data.get("rates", {})
        if to_currency not in rates:
            raise ValueError(
                f"Валюта {to_currency} не найдена в ответе API. " f"Доступные валюты: {list(rates.keys())}"
            )

        return float(rates[to_currency])

    except requests.exceptions.Timeout:
        raise ConnectionError("Превышено время ожидания ответа от API")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Не удалось подключиться к API. Проверьте интернет-соединение")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к API: {str(e)}")
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Некорректный ответ от API: {str(e)}")


def process_transaction(self, transaction: Dict[str, Any]) -> float:
    """
    Обрабатывает транзакцию и возвращает сумму в рублях

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма транзакции в рублях (float)

    Raises:
        ValueError: Если транзакция имеет неверный формат или отсутствуют данные
        ConnectionError: Если не удалось получить курс валюты от API
    """
    try:
        # Извлекаем данные о сумме операции
        operation_amount = transaction.get("operationAmount", {})

        if not operation_amount:
            raise ValueError("Отсутствует поле 'operationAmount' в транзакции")

        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency", {})

        if amount_str is None:
            raise ValueError("Отсутствует поле 'amount' в operationAmount")
        if not currency_info:
            raise ValueError("Отсутствует поле 'currency' в operationAmount")

        currency_code = currency_info.get("code")
        if not currency_code:
            raise ValueError("Отсутствует поле 'code' в currency")

        # Преобразуем сумму в float
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            raise ValueError(f"Некорректный формат суммы: {amount_str}")

        # Проверяем, что сумма не отрицательна
        if amount < 0:
            raise ValueError(f"Сумма не может быть отрицательной: {amount}")

        # Если валюта уже в рублях, возвращаем сумму
        if currency_code.upper() == "RUB":
            return amount

        # Получаем курс валюты и конвертируем
        exchange_rate = self._get_exchange_rate(currency_code.upper(), "RUB")

        if exchange_rate <= 0:
            raise ValueError(f"Некорректный курс обмена: {exchange_rate}")

        result = amount * exchange_rate
        return round(result, 2)  # Округляем до копеек
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле в транзакции: {e}")
