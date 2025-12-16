import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма транзакции в рублях (float)
    """
    # Извлекаем сумму и валюту
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]
    exchange_date = transaction["date"]

    # Если валюта уже в рублях - возвращаем как есть
    if currency_code == "RUB":
        return amount

    # Получаем курс валюты через API
    api_key = os.getenv("ForexAPIKey")
    url = "https://data.fixer.io/api/convert?access_key={api_key}"

    querystring = {"from": "currency_code", "to": "RUB", "amount": "amount", "date": "exchange_date"}

    response = requests.get(url, params=querystring)
    data = response.json()

    return data["result"]
