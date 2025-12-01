import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции маскировки карт и счетов"""

    # Параметризованные тесты для карт
    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
            ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
            ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
            ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
            ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ],
    )
    def test_mask_card_number(self, input_data: str, expected: str) -> None:
        assert mask_account_card(input_data) == expected

    # Параметризованные тесты для счетов
    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ("Счет 12345678901234567890", "Счет **7890"),
            ("Счет 12345678901234567891", "Счет **7891"),
            ("Счет 12345678901234567892", "Счет **7892"),
        ],
    )
    def test_mask_account_number(self, input_data: str, expected: str) -> None:
        assert mask_account_card(input_data) == expected

    # Тесты для некорректных данных
    #    @pytest.mark.parametrize(
    #        "invalid_input",
    #        [
    #            "",
    #            "InvalidStringWithoutNumber",
    #            "Счет",
    #            "Card",
    #            "Счет 123",
    #            "Card 123",
    #            "Счет 123456789012345678901234567890",  # Слишком длинный номер
    #        ],
    #    )
    #    def test_invalid_input(self, invalid_input):
    #        with pytest.raises(ValueError):
    #            mask_account_card(invalid_input)

    # Тест на обработку разных регистров
    def test_case_insensitive(self) -> None:
        assert mask_account_card("сЧет 12345678901234567890") == "сЧет **7890"


class TestGetDate:
    """Тесты для функции преобразования даты"""

    # Основные тесты преобразования дат
    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-03-25T10:30:00", "25.03.2024"),
            ("2023-12-01T00:00:00", "01.12.2023"),
            ("2020-02-29T23:59:59", "29.02.2020"),  # Високосный год
            ("1999-01-01T12:00:00", "01.01.1999"),
        ],
    )
    def test_date_conversion(self, input_date: str, expected: str) -> None:
        assert get_date(input_date) == expected

        # Тесты граничных случаев

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-01-01T00:00:00", "01.01.2024"),  # Начало года
            ("2024-12-31T23:59:59", "31.12.2024"),  # Конец года
            ("2024-02-28T12:00:00", "28.02.2024"),  # Конец февраля
        ],
    )
    def test_boundary_dates(self, input_date: str, expected: str) -> None:
        assert get_date(input_date) == expected

    # Тест на корректность обработки без времени
    def test_date_without_time(self) -> None:
        assert get_date("2024-03-25") == "25.03.2024"

    # Тест на обработку минимально допустимой даты
    def test_minimum_date(self) -> None:
        assert get_date("0001-01-01T00:00:00") == "01.01.0001"
