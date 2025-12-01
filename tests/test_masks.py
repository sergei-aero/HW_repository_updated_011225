import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number"""

    @pytest.fixture
    def valid_card_numbers(self):
        """Фикстура с валидными номерами карт"""
        return ["7000792289606361", "1234567890123456", "1111222233334444"]

    @pytest.fixture
    def card_numbers_with_spaces(self):
        """Фикстура с номерами карт с пробелами"""
        return ["7000 7922 8960 6361", "1234 5678 9012 3456", "1111 2222 3333 4444"]

    @pytest.fixture
    def card_numbers_as_integers(self):
        """Фикстура с номерами карт как целые числа"""
        return [7000792289606361, 1234567890123456]

    @pytest.fixture
    def invalid_length_cards(self):
        """Фикстура с номерами карт нестандартной длины"""
        return [
            "1234",  # 4 цифры
            "123456789012345",  # 15 цифр
            "12345678901234567",  # 17 цифр
            "12345678901234567890",  # 20 цифр
        ]

    @pytest.fixture
    def invalid_format_cards(self):
        """Фикстура с номерами карт в неверном формате"""
        return [
            "1234abcd56789012",  # с буквами
            "1234-5678-9012-3456",  # с дефисами
            "1234 5678 9012 345",  # 15 цифр с пробелами
        ]

    @pytest.fixture
    def empty_card_inputs(self):
        """Фикстура с пустыми входными данными"""
        return ["", "   ", None]

    def test_correct_card_masking(self, valid_card_numbers):
        """Тестирование правильности маскирования номера карты"""
        expected_results = ["7000 79** **** 6361", "1234 56** **** 3456", "1111 22** **** 4444"]

        for card, expected in zip(valid_card_numbers, expected_results):
            result = get_mask_card_number(card)
            assert result == expected

    def test_card_numbers_with_spaces(self, card_numbers_with_spaces):
        """Проверка работы функции на номерах карт с пробелами"""
        expected_results = ["7000 79** **** 6361", "1234 56** **** 3456", "1111 22** **** 4444"]

        for card, expected in zip(card_numbers_with_spaces, expected_results):
            result = get_mask_card_number(card)
            assert result == expected

    def test_card_numbers_as_integers(self, card_numbers_as_integers):
        """Проверка работы функции с целыми числами"""
        expected_results = ["7000 79** **** 6361", "1234 56** **** 3456"]

        for card, expected in zip(card_numbers_as_integers, expected_results):
            result = get_mask_card_number(card)
            assert result == expected

    def test_invalid_length_cards(self, invalid_length_cards):
        """Проверка граничных случаев и нестандартных длин номеров"""
        for invalid_card in invalid_length_cards:
            with pytest.raises(ValueError):
                get_mask_card_number(invalid_card)

    def test_invalid_format_cards(self, invalid_format_cards):
        """Проверка неверных форматов номеров карт"""
        for invalid_card in invalid_format_cards:
            with pytest.raises(ValueError):
                get_mask_card_number(invalid_card)

    def test_empty_card_inputs(self, empty_card_inputs):
        """Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты"""
        for empty_input in empty_card_inputs:
            with pytest.raises(ValueError):
                get_mask_card_number(empty_input)


class TestGetMaskAccount:
    """Тесты для функции get_mask_account"""

    @pytest.fixture
    def valid_account_numbers(self):
        """Фикстура с валидными номерами счетов"""
        return ["73654108430135874305", "12345678901234567890", "98765432109876543210"]

    @pytest.fixture
    def account_numbers_with_spaces(self):
        """Фикстура с номерами счетов с пробелами"""
        return ["7365 4108 4301 3587 4305", "1234 5678 9012 3456 7890", "9876 5432 1098 7654 3210"]

    @pytest.fixture
    def account_numbers_as_integers(self):
        """Фикстура с номерами счетов как целые числа"""
        return [73654108430135874305, 12345678901234567890]

    @pytest.fixture
    def various_length_accounts(self):
        """Фикстура с номерами счетов различной длины"""
        return [
            "123456",  # 6 цифр (минимальная длина)
            "1234567",  # 7 цифр
            "12345678",  # 8 цифр
        ]

    @pytest.fixture
    def too_short_accounts(self):
        """Фикстура со слишком короткими номерами счетов"""
        return [
            "",  # пустая строка
            "1",  # 1 цифра
            "12",  # 2 цифры
            "123",  # 3 цифры
            "1234",  # 4 цифры
            "12345",  # 5 цифр
        ]

#    @pytest.fixture
#    def invalid_format_accounts(self):
#        """Фикстура с номерами счетов в неверном формате"""
#        return [
#            "1234abcd567890123456",  # с буквами
#            "1234-5678-9012-3456-7890",  # с дефисами
#            "account_number",  # только буквы
#        ]

    def test_correct_account_masking(self, valid_account_numbers):
        """Тестирование правильности маскирования номера счета"""
        expected_results = ["**4305", "**7890", "**3210"]

        for account, expected in zip(valid_account_numbers, expected_results):
            result = get_mask_account(account)
            assert result == expected

    def test_account_numbers_with_spaces(self, account_numbers_with_spaces):
        """Проверка работы функции с номерами счетов с пробелами"""
        expected_results = ["**4305", "**7890", "**3210"]

        for account, expected in zip(account_numbers_with_spaces, expected_results):
            result = get_mask_account(account)
            assert result == expected

    def test_account_numbers_as_integers(self, account_numbers_as_integers):
        """Проверка работы функции с целыми числами"""
        expected_results = ["**4305", "**7890"]

        for account, expected in zip(account_numbers_as_integers, expected_results):
            result = get_mask_account(account)
            assert result == expected

    def test_various_length_accounts(self, various_length_accounts):
        """Проверка работы функции с различными длинами номеров счетов"""
        expected_results = ["**3456", "**4567", "**5678"]

        for account, expected in zip(various_length_accounts, expected_results):
            result = get_mask_account(account)
            assert result == expected

    def test_too_short_accounts(self, too_short_accounts):
        """Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины"""
        for too_short_account in too_short_accounts:
            with pytest.raises(ValueError):
                get_mask_account(too_short_account)

#    def test_invalid_format_accounts(self, invalid_format_accounts):
#       """Проверка неверных форматов номеров счетов"""
#       for invalid_account in invalid_format_accounts:
#            with pytest.raises(ValueError):
#                get_mask_account(invalid_account)
