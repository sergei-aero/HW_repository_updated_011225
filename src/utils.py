import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

# Получаем путь к текущему файлу (utils.py)
current_file = Path(__file__).resolve()

project_root = current_file.parent.parent

log_dir = project_root / "logs"
log_file = log_dir / "utils.log"

log_dir.mkdir(exist_ok=True)


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file)
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_json_operations(filepath: str = "data/operations.json") -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    # Проверка существования файла
    if not os.path.exists(filepath):
        logger.warning("Файл по указанному адресу не найден")
        return []

    # Проверка, что это файл, а не директория
    if not os.path.isfile(filepath):
        logger.warning("Файл по указанному адресу не найден")
        return []

    # Проверка размера файла (пустой ли)
    if os.path.getsize(filepath) == 0:
        logger.warning("По указанному адресу найден пустой файл")
        return []

    with open(filepath, "r", encoding="utf-8") as file:
        operations = json.load(file)
    if not isinstance(operations, list):
        return []

    return operations
