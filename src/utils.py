import json
import os
from typing import List, Dict, Any


def load_json_operations(filepath: str = 'data/operations.json') -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    # Проверка существования файла
    if not os.path.exists(filepath):
        return []

    # Проверка, что это файл, а не директория
    if not os.path.isfile(filepath):
        return []

    # Проверка размера файла (пустой ли)
    if os.path.getsize(filepath) == 0:
        return []

    with open(filepath, 'r', encoding='utf-8') as file:
        operations = json.load(file)
    if not isinstance(operations, list):
        return []

    return operations
