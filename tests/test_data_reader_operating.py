"""
Тесты для модуля чтения данных с использованием pytest.
"""

import pytest
import pandas as pd
from typing import List, Dict, Any
from unittest.mock import patch, MagicMock
from src.data_reader_operating import read_csv_file, read_excel_file, get_file_path


# Фикстуры для тестовых данных
@pytest.fixture
def test_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "date": "2023-01-15", "amount": 100.50, "currency": "USD", "status": "COMPLETED"},
        {"id": 2, "date": "2023-01-16", "amount": 2000.00, "currency": "RUB", "status": "COMPLETED"},
        {"id": 3, "date": "2023-01-17", "amount": 50.00, "currency": "EUR", "status": "PENDING"},
    ]


@pytest.fixture
def test_dataframe(test_transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """Фикстура с тестовым DataFrame."""
    return pd.DataFrame(test_transactions)


class TestDataReader:
    """Тесты для модуля чтения данных."""

    def test_get_file_path(self) -> None:
        """Тест формирования пути к файлу."""
        project_root: str = get_file_path("").replace("data", "")
        path: str = get_file_path("test.csv")
        expected_path: str = project_root + "data/test.csv"

        assert path == expected_path
        assert path.endswith("data/test.csv")

    @patch("src.data_reader.pd.read_csv")
    @patch("src.data_reader.get_file_path")
    def test_read_csv_file_success(
        self, mock_get_path: MagicMock, mock_read_csv: MagicMock, test_dataframe: pd.DataFrame
    ) -> None:
        """Тест успешного чтения CSV файла."""
        mock_get_path.return_value = "/fake/path/data/transactions.csv"
        mock_read_csv.return_value = test_dataframe

        result: List[Dict[str, Any]] = read_csv_file("transactions.csv")

        mock_get_path.assert_called_once_with("transactions.csv")
        mock_read_csv.assert_called_once_with("/fake/path/data/transactions.csv", header=0)

        assert len(result) == 3
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

        # Проверяем, что все ключи - строки
        for transaction in result:
            for key in transaction.keys():
                assert isinstance(key, str)

    @patch("src.data_reader.pd.read_excel")
    @patch("src.data_reader.get_file_path")
    def test_read_excel_file_success(
        self, mock_get_path: MagicMock, mock_read_excel: MagicMock, test_dataframe: pd.DataFrame
    ) -> None:
        """Тест успешного чтения Excel файла."""
        mock_get_path.return_value = "/fake/path/data/transactions.xlsx"
        mock_read_excel.return_value = test_dataframe

        result: List[Dict[str, Any]] = read_excel_file("transactions.xlsx")

        mock_get_path.assert_called_once_with("transactions.xlsx")
        mock_read_excel.assert_called_once_with("/fake/path/data/transactions.xlsx", engine="openpyxl", header=0)

        assert len(result) == 3
        assert result[0]["currency"] == "USD"
        assert result[1]["currency"] == "RUB"

    @patch("src.data_reader.pd.read_csv")
    @patch("src.data_reader.get_file_path")
    def test_read_csv_file_not_found(self, mock_get_path: MagicMock, mock_read_csv: MagicMock) -> None:
        """Тест обработки отсутствующего файла."""
        mock_get_path.return_value = "/fake/path/data/nonexistent.csv"
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        with pytest.raises(FileNotFoundError):
            read_csv_file("nonexistent.csv")

    @patch("src.data_reader.pd.read_csv")
    @patch("src.data_reader.get_file_path")
    def test_read_empty_csv_file(self, mock_get_path: MagicMock, mock_read_csv: MagicMock) -> None:
        """Тест чтения пустого CSV файла."""
        empty_df: pd.DataFrame = pd.DataFrame()
        mock_get_path.return_value = "/fake/path/data/empty.csv"
        mock_read_csv.return_value = empty_df

        result: List[Dict[str, Any]] = read_csv_file("empty.csv")

        assert len(result) == 0
        assert result == []

    @patch("src.data_reader.pd.read_csv")
    @patch("src.data_reader.get_file_path")
    def test_read_csv_with_pandas_error(self, mock_get_path: MagicMock, mock_read_csv: MagicMock) -> None:
        """Тест обработки ошибок pandas."""
        mock_get_path.return_value = "/fake/path/data/corrupted.csv"
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing CSV")

        with pytest.raises(pd.errors.ParserError):
            read_csv_file("corrupted.csv")
