from datetime import datetime


def filter_by_state(dict_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in dict_list if item.get("state") == state]


def sort_by_date(transactions: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате.
    """
    return sorted(transactions, key=lambda x: datetime.fromisoformat(x["date"]), reverse=descending)
