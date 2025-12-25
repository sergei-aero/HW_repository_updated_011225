"""
Объединенные тесты для функций filter_by_currency и transaction_descriptions.
"""
import pytest
from typing import List, Dict, Any, Iterator
from collections.abc import Generator

# Импортируем тестируемые функции
from src.generators import filter_by_currency, transaction_descriptions


# ==================== ФИКСТУРЫ ====================

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Основные тестовые данные из задания (5 транзакций)."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Пустой список транзакций для тестирования граничных случаев."""
    return []


@pytest.fixture
def single_transaction() -> List[Dict[str, Any]]:
    """Список с одной транзакцией для тестирования минимального случая."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            },
            "description": "Тестовая транзакция"
        }
    ]


@pytest.fixture
def two_transactions() -> List[Dict[str, Any]]:
    """Список с двумя транзакциями для тестирования небольшого набора."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Первая транзакция",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Вторая транзакция",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "EUR"}
            }
        }
    ]


@pytest.fixture
def mixed_currency_transactions() -> List[Dict[str, Any]]:
    """Транзакции с разными валютами для тестирования фильтрации."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            },
            "description": "USD транзакция"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "EUR"}
            },
            "description": "EUR транзакция"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"code": "USD"}
            },
            "description": "Еще USD транзакция"
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "400.00",
                "currency": {"code": "GBP"}
            },
            "description": "GBP транзакция"
        }
    ]


# ==================== ТЕСТЫ ДЛЯ filter_by_currency ====================

class TestFilterByCurrency:
    """Тесты для функции filter_by_currency"""

    def test_returns_iterator(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем, что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions, "USD")
        assert isinstance(result, Iterator)
        assert isinstance(result, Generator)

    def test_correctly_filters_usd_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем корректную фильтрацию USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 3
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)

    def test_correctly_filters_rub_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем корректную фильтрацию RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in rub_transactions)

    def test_case_insensitive_filtering(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем регистронезависимую фильтрацию."""
        usd_lower = list(filter_by_currency(sample_transactions, "usd"))
        usd_upper = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_lower) == 3 and len(usd_upper) == 3
        assert {t["id"] for t in usd_lower} == {t["id"] for t in usd_upper}

    def test_no_transactions_in_target_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем случай, когда транзакций в заданной валюте нет."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

        eur_iterator = filter_by_currency(sample_transactions, "EUR")
        with pytest.raises(StopIteration):
            next(eur_iterator)

    def test_empty_transactions_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем обработку пустого списка транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert len(result) == 0

        empty_iterator = filter_by_currency(empty_transactions, "USD")
        with pytest.raises(StopIteration):
            next(empty_iterator)

    def test_single_transaction_filtering(self, single_transaction: List[Dict[str, Any]]) -> None:
        """Проверяем фильтрацию с одной транзакцией."""
        usd_transactions = list(filter_by_currency(single_transaction, "USD"))
        assert len(usd_transactions) == 1
        assert usd_transactions[0]["description"] == "Тестовая транзакция"

        eur_transactions = list(filter_by_currency(single_transaction, "EUR"))
        assert len(eur_transactions) == 0

    def test_two_transactions_filtering(self, two_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем фильтрацию с двумя транзакциями."""
        usd_transactions = list(filter_by_currency(two_transactions, "USD"))
        assert len(usd_transactions) == 1
        assert usd_transactions[0]["description"] == "Первая транзакция"

        eur_transactions = list(filter_by_currency(two_transactions, "EUR"))
        assert len(eur_transactions) == 1
        assert eur_transactions[0]["description"] == "Вторая транзакция"

    def test_mixed_currency_filtering(self, mixed_currency_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем фильтрацию с разными валютами."""
        usd_transactions = list(filter_by_currency(mixed_currency_transactions, "USD"))
        assert len(usd_transactions) == 2
        assert {t["id"] for t in usd_transactions} == {1, 3}

        eur_transactions = list(filter_by_currency(mixed_currency_transactions, "EUR"))
        assert len(eur_transactions) == 1
        assert eur_transactions[0]["id"] == 2

        gbp_transactions = list(filter_by_currency(mixed_currency_transactions, "GBP"))
        assert len(gbp_transactions) == 1
        assert gbp_transactions[0]["id"] == 4

        jpy_transactions = list(filter_by_currency(mixed_currency_transactions, "JPY"))
        assert len(jpy_transactions) == 0

    def test_sequential_iteration(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем последовательную итерацию (как в примере задания)."""
        usd_transactions = filter_by_currency(sample_transactions, "USD")
        iterator = iter(usd_transactions)

        first = next(iterator)
        assert first["id"] == 939719570

        second = next(iterator)
        assert second["id"] == 142264268

        third = next(iterator)
        assert third["id"] == 895315941

        with pytest.raises(StopIteration):
            next(iterator)

    def test_preserves_order(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем, что порядок транзакций сохраняется."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        expected_order = [939719570, 142264268, 895315941]
        actual_order = [t["id"] for t in usd_transactions]
        assert actual_order == expected_order

    @pytest.mark.parametrize("currency, expected_count, expected_ids", [
        ("USD", 3, {939719570, 142264268, 895315941}),
        ("RUB", 2, {873106923, 594226727}),
        ("EUR", 0, set()),
        ("GBP", 0, set()),
    ])
    def test_parametrized_currency_filtering(
            self,
            sample_transactions: List[Dict[str, Any]],
            currency: str,
            expected_count: int,
            expected_ids: set[int]
    ) -> None:
        """Параметризованный тест для разных валют."""
        filtered = list(filter_by_currency(sample_transactions, currency))
        assert len(filtered) == expected_count
        assert {t["id"] for t in filtered} == expected_ids


# ==================== ТЕСТЫ ДЛЯ transaction_descriptions ====================

class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions"""

    def test_returns_iterator(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем, что функция возвращает итератор."""
        result = transaction_descriptions(sample_transactions)
        assert isinstance(result, Iterator)
        assert isinstance(result, Generator)

    def test_returns_correct_descriptions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем, что функция возвращает корректные описания для каждой транзакции."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]
        assert descriptions == expected

    def test_preserves_order_of_descriptions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем, что порядок описаний соответствует порядку транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert descriptions[0] == "Перевод организации"
        assert descriptions[1] == "Перевод со счета на счет"
        assert descriptions[2] == "Перевод со счета на счет"
        assert descriptions[3] == "Перевод с карты на карту"
        assert descriptions[4] == "Перевод организации"

    def test_empty_transactions_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем работу функции с пустым списком транзакций."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert len(descriptions) == 0

        empty_iterator = transaction_descriptions(empty_transactions)
        with pytest.raises(StopIteration):
            next(empty_iterator)

    def test_single_transaction(self, single_transaction: List[Dict[str, Any]]) -> None:
        """Проверяем работу функции с одной транзакцией."""
        descriptions = list(transaction_descriptions(single_transaction))
        assert len(descriptions) == 1
        assert descriptions[0] == "Тестовая транзакция"

    def test_two_transactions(self, two_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем работу функции с двумя транзакциями."""
        descriptions = list(transaction_descriptions(two_transactions))
        assert len(descriptions) == 2
        assert descriptions == ["Первая транзакция", "Вторая транзакция"]

    def test_mixed_currency_transactions_descriptions(
            self,
            mixed_currency_transactions: List[Dict[str, Any]]
    ) -> None:
        """Проверяем описания транзакций с разными валютами."""
        descriptions = list(transaction_descriptions(mixed_currency_transactions))
        expected = [
            "USD транзакция",
            "EUR транзакция",
            "Еще USD транзакция",
            "GBP транзакция"
        ]
        assert descriptions == expected

    def test_sequential_iteration_example(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Пример использования из задания."""
        descriptions = transaction_descriptions(sample_transactions)
        result = []
        for _ in range(5):
            result.append(next(descriptions))

        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]
        assert result == expected

    def test_generator_exhaustion(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем исчерпание генератора."""
        descriptions_gen = transaction_descriptions(sample_transactions)

        # Извлекаем все 5 описаний
        for _ in range(5):
            next(descriptions_gen)

        # Генератор должен быть исчерпан
        with pytest.raises(StopIteration):
            next(descriptions_gen)

    @pytest.mark.parametrize("fixture_name, expected_count", [
        ("empty_transactions", 0),
        ("single_transaction", 1),
        ("two_transactions", 2),
        ("sample_transactions", 5),
        ("mixed_currency_transactions", 4),
    ])
    def test_parametrized_with_different_counts(
            self,
            fixture_name: str,
            expected_count: int,
            request: pytest.FixtureRequest
    ) -> None:
        """Параметризованный тест для разного количества транзакций."""
        transactions = request.getfixturevalue(fixture_name)
        descriptions = list(transaction_descriptions(transactions))
        assert len(descriptions) == expected_count


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

class TestIntegratedFunctions:
    """Интеграционные тесты, проверяющие совместную работу функций."""

    def test_chain_functions_together(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем цепочку вызовов функций."""
        # Сначала фильтруем по USD, затем получаем описания
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        usd_descriptions = list(transaction_descriptions(usd_transactions))

        assert len(usd_descriptions) == 3
        expected_usd_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод с карты на карту"
        ]

        # Проверяем, что все описания присутствуют (порядок сохраняется)
        assert usd_descriptions == expected_usd_descriptions

    def test_chain_with_empty_results(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем цепочку вызовов с пустыми результатами."""
        # Фильтруем по несуществующей валюте
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        eur_descriptions = list(transaction_descriptions(eur_transactions))

        assert len(eur_descriptions) == 0

    def test_exact_examples_from_assignment(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Проверяем точные примеры из задания для обеих функций."""
        # Пример для filter_by_currency
        usd_transactions = filter_by_currency(sample_transactions, "USD")
        iterator = iter(usd_transactions)

        first_transaction = next(iterator)
        assert first_transaction["id"] == 939719570
        assert first_transaction["operationAmount"]["currency"]["code"] == "USD"

        second_transaction = next(iterator)
        assert second_transaction["id"] == 142264268
        assert second_transaction["operationAmount"]["currency"]["code"] == "USD"

        # Пример для transaction_descriptions
        descriptions = transaction_descriptions(sample_transactions)
        result = []
        for _ in range(5):
            result.append(next(descriptions))

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]
        assert result == expected_descriptions

