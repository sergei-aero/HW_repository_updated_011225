from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD", "RUB")

    Returns:
        Итератор транзакций с указанной валютой
    """
    # Приводим валюту к верхнему регистру для регистронезависимого сравнения
    target_currency = currency.upper()

    # Итерируем по списку транзакций
    for transaction in transactions:
        # Получаем код валюты из транзакции
        currency_code = transaction["operationAmount"]["currency"]["code"]

        # Сравниваем валюты (регистронезависимо)
        if currency_code.upper() == target_currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        Итератор строк с описаниями транзакций
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение (последние 4 цифры)
        end: Конечное значение (последние 4 цифры, включительно)

    Yields:
        Номера карт в формате "0000 0000 0000 XXXX"
    """
    for number in range(start, end + 1):
        yield f"0000 0000 0000 {number:04d}"
