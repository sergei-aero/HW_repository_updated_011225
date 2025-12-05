import pytest
from datetime import datetime
from src.proccesing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями"""
        return [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00.000000"},
            {"id": 2, "state": "PENDING", "date": "2024-01-16T11:00:00.000000"},
            {"id": 3, "state": "EXECUTED", "date": "2024-01-17T12:00:00.000000"},
            {"id": 4, "state": "CANCELED", "date": "2024-01-18T13:00:00.000000"},
            {"id": 5, "state": "EXECUTED", "date": "2024-01-19T14:00:00.000000"},
        ]

    @pytest.fixture
    def transactions_with_missing_state(self):
        """Фикстура с транзакциями без ключа state"""
        return [
            {"id": 1, "date": "2024-01-15T10:30:00.000000"},
            {"id": 2, "state": "EXECUTED", "date": "2024-01-16T11:00:00.000000"},
            {"id": 3, "date": "2024-01-17T12:00:00.000000"},
            {"id": 4, "state": "PENDING", "date": "2024-01-18T13:00:00.000000"},
        ]

    @pytest.fixture
    def empty_transactions(self):
        """Фикстура с пустым списком транзакций"""
        return []

    @pytest.mark.parametrize(
        "state,expected_ids",
        [
            ("EXECUTED", [1, 3, 5]),
            ("PENDING", [2]),
            ("CANCELED", [4]),
            ("COMPLETED", []),  # Несуществующий статус
        ],
    )
    def test_filter_by_different_states(self, sample_transactions, state, expected_ids):
        """Параметризация тестов для различных значений статуса state"""
        result = filter_by_state(sample_transactions, state)

        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

        # Проверяем, что все элементы имеют правильный state
        for item in result:
            assert item["state"] == state

    def test_default_state_parameter(self, sample_transactions):
        """Тестирование фильтрации со значением state по умолчанию"""
        result = filter_by_state(sample_transactions)  # state="EXECUTED" по умолчанию

        result_ids = [item["id"] for item in result]
        assert result_ids == [1, 3, 5]

    def test_missing_state_key(self, transactions_with_missing_state):
        """Проверка работы при отсутствии ключа state у некоторых элементов"""
        result = filter_by_state(transactions_with_missing_state, "EXECUTED")

        result_ids = [item["id"] for item in result]
        assert result_ids == [2]  # Только один элемент с state="EXECUTED"

    def test_empty_input_list(self, empty_transactions):
        """Проверка работы функции при пустом списке"""
        result = filter_by_state(empty_transactions, "EXECUTED")
        assert result == []

    def test_no_matching_state(self, sample_transactions):
        """Проверка работы при отсутствии словарей с указанным статусом"""
        result = filter_by_state(sample_transactions, "NON_EXISTENT")
        assert result == []

    def test_original_list_unmodified(self, sample_transactions):
        """Проверка, что исходный список не изменяется"""
        original_data = sample_transactions.copy()
        result = filter_by_state(sample_transactions, "EXECUTED")

        assert sample_transactions == original_data
        assert result is not sample_transactions  # Должен возвращаться новый список


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями для сортировки"""
        return [
            {"id": 1, "date": "2024-01-15T10:30:00.000000", "amount": 100},
            {"id": 2, "date": "2024-01-10T14:45:00.000000", "amount": 200},
            {"id": 3, "date": "2024-01-20T09:15:00.000000", "amount": 300},
            {"id": 4, "date": "2024-01-05T16:20:00.000000", "amount": 400},
        ]

    @pytest.fixture
    def transactions_with_same_dates(self):
        """Фикстура с транзакциями с одинаковыми датами"""
        return [
            {"id": 1, "date": "2024-01-15T10:30:00.000000", "amount": 100},
            {"id": 2, "date": "2024-01-15T10:30:00.000000", "amount": 200},
            {"id": 3, "date": "2024-01-15T10:30:00.000000", "amount": 300},
            {"id": 4, "date": "2024-01-10T14:45:00.000000", "amount": 400},
        ]

    @pytest.fixture
    def transactions_with_invalid_dates(self):
        """Фикстура с транзакциями с некорректными датами"""
        return [
            {"id": 1, "date": "2024-01-15T10:30:00.000000", "amount": 100},
            {"id": 2, "date": "invalid_date_format", "amount": 200},
            {"id": 3, "date": "2024-01-20T09:15:00.000000", "amount": 300},
        ]

    @pytest.fixture
    def empty_transactions(self):
        """Фикстура с пустым списком транзакций"""
        return []

    def test_sort_descending_default(self, sample_transactions):
        """Тестирование сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_transactions)

        result_ids = [item["id"] for item in result]
        assert result_ids == [3, 1, 2, 4]  # От новых к старым

    def test_sort_descending_explicit(self, sample_transactions):
        """Тестирование сортировки по убыванию (явно)"""
        result = sort_by_date(sample_transactions, descending=True)

        result_ids = [item["id"] for item in result]
        assert result_ids == [3, 1, 2, 4]  # От новых к старым

    def test_sort_ascending(self, sample_transactions):
        """Тестирование сортировки по возрастанию"""
        result = sort_by_date(sample_transactions, descending=False)

        result_ids = [item["id"] for item in result]
        assert result_ids == [4, 2, 1, 3]  # От старых к новым

    def test_sort_with_same_dates(self, transactions_with_same_dates):
        """Проверка корректности сортировки при одинаковых датах"""
        result = sort_by_date(transactions_with_same_dates)

        # При одинаковых датах порядок должен сохраняться (стабильная сортировка)
        result_ids = [item["id"] for item in result]

        # Проверяем, что даты действительно отсортированы правильно
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, key=lambda x: datetime.fromisoformat(x), reverse=True)

    def test_empty_input_list(self, empty_transactions):
        """Тестирование сортировки пустого списка"""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_original_list_unmodified(self, sample_transactions):
        """Проверка, что исходный список не изменяется"""
        original_data = sample_transactions.copy()
        result = sort_by_date(sample_transactions)

        assert sample_transactions == original_data
        assert result is not sample_transactions  # Должен возвращаться новый список

    def test_invalid_date_format(self, transactions_with_invalid_dates):
        """Тесты на работу функции с некорректными форматами дат"""
        with pytest.raises(ValueError):
            sort_by_date(transactions_with_invalid_dates)

    #    @pytest.mark.parametrize(
    #        "date_format",
    #        [
    #           "2024-01-15",  # Без времени
    #           "2024-01-15T10:30:00",  # Без микросекунд
    #           "15-01-2024 10:30:00",  # Неправильный формат
    #           "2024/01/15T10:30:00.000000",  # Неправильный разделитель
    #       ],
    #   )
    # def test_various_date_formats(self, date_format):
    #   """Тестирование различных форматов дат"""
    #    transactions = [{"id": 1, "date": date_format}]
    #
    #   with pytest.raises(ValueError):
    #        sort_by_date(transactions)

    def test_missing_date_key(self):
        """Тестирование при отсутствии ключа date"""
        transactions = [
            {"id": 1, "amount": 100},
            {"id": 2, "date": "2024-01-15T10:30:00.000000", "amount": 200},
        ]

        with pytest.raises(KeyError):
            sort_by_date(transactions)


# Интеграционные тесты для обеих функций
class TestIntegration:
    """Интеграционные тесты для совместной работы функций"""

    @pytest.fixture
    def complex_transactions(self):
        """Фикстура со сложными данными для интеграционного тестирования"""
        return [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00.000000"},
            {"id": 2, "state": "PENDING", "date": "2024-01-10T14:45:00.000000"},
            {"id": 3, "state": "EXECUTED", "date": "2024-01-20T09:15:00.000000"},
            {"id": 4, "state": "EXECUTED", "date": "2024-01-05T16:20:00.000000"},
            {"id": 5, "state": "CANCELED", "date": "2024-01-25T11:00:00.000000"},
        ]

    def test_filter_and_sort_combination(self, complex_transactions):
        """Тестирование комбинации фильтрации и сортировки"""
        # Сначала фильтруем по EXECUTED
        filtered = filter_by_state(complex_transactions, "EXECUTED")

        # Затем сортируем по убыванию даты
        sorted_result = sort_by_date(filtered, descending=True)

        result_ids = [item["id"] for item in sorted_result]
        assert result_ids == [3, 1, 4]  # EXECUTED транзакции от новых к старым

    def test_filter_and_sort_ascending(self, complex_transactions):
        """Тестирование комбинации фильтрации и сортировки по возрастанию"""
        filtered = filter_by_state(complex_transactions, "EXECUTED")
        sorted_result = sort_by_date(filtered, descending=False)

        result_ids = [item["id"] for item in sorted_result]
        assert result_ids == [4, 1, 3]  # EXECUTED транзакции от старых к новым
