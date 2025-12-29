"""
Модуль для чтения CSV и XLSX файлов с транзакциями.
"""

import os
from typing import Any, Dict, List

import pandas as pd


def get_file_path(filename: str) -> str:
    """
    Возвращает абсолютный путь к файлу в директории data.

    Args:
        filename: Имя файла (например, 'transactions.csv')

    Returns:
        Абсолютный путь к файлу
    """
    # Получаем корневую директорию проекта (на уровень выше src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Формируем путь к файлу в директории data
    return os.path.join(project_root, "data", filename)


def read_csv_file(filename: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл и возвращает список словарей с транзакциями.

    Args:
        filename: Имя CSV файла

    Returns:
        Список словарей с транзакциями
    """
    file_path = get_file_path(filename)
    df_csv = pd.read_csv(file_path, header=0)
    df_csv.columns = df_csv.columns.astype(str)
    transactions_csv = df_csv.to_dict(orient="records")

    result: List[Dict[str, Any]] = []
    for record in transactions_csv:
        str_record: Dict[str, Any] = {}
        for key, value in record.items():
            str_key = str(key) if not isinstance(key, str) else key
            str_record[str_key] = value
        result.append(str_record)

    return result


def read_excel_file(filename: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл и возвращает список словарей с транзакциями.

    Args:
        filename: Имя Excel файла

    Returns:
        Список словарей с транзакциями
    """
    file_path = get_file_path(filename)
    df_xlsx = pd.read_excel(file_path, engine="openpyxl", header=0)
    df_xlsx.columns = df_xlsx.columns.astype(str)

    transactions_xlsx = df_xlsx.to_dict(orient="records")

    result: List[Dict[str, Any]] = []
    for record in transactions_xlsx:
        str_record: Dict[str, Any] = {}
        for key, value in record.items():
            str_key = str(key) if not isinstance(key, str) else key
            str_record[str_key] = value
        result.append(str_record)

    return result
