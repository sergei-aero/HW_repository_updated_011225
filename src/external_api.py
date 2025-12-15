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

    # Если валюта уже в рублях - возвращаем как есть
    if currency_code == "RUB":
        return amount

    # Получаем курс валюты через API
    api_key = os.getenv("ForexAPIKey")
    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {"apikey": api_key}
    params = {"base": currency_code, "symbols": "RUB"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Извлекаем курс
    rate = data["rates"]["RUB"]

    # Конвертируем
    return amount * rate
