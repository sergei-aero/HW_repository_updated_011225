import unittest
from unittest.mock import Mock, patch

from src.external_api import convert_to_rubles


class TestCurrencyConverter(unittest.TestCase):
    """Тесты для функции конвертации валют."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        # Транзакция в рублях
        self.rub_transaction = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}

        # Транзакция в долларах
        self.usd_transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

        # Транзакция в евро
        self.eur_transaction = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}

    def test_rub_transaction(self) -> None:
        """
        Тест: транзакция в рублях (без вызова API).
        """
        with patch("currency_converter.requests.get") as mock_get:
            result = convert_to_rubles(self.rub_transaction)

            # API не должно вызываться для рублевых транзакций
            mock_get.assert_not_called()

            # Сумма должна остаться без изменений
            self.assertEqual(result, 1000.50)
            self.assertIsInstance(result, float)

    @patch.dict("os.environ", {"FOREX_API_KEY": "test-key"})
    @patch("currency_converter.requests.get")
    def test_usd_transaction(self, mock_get: Mock) -> None:
        """
        Тест: транзакция в долларах (с вызовом API).
        """
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.50}}
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = convert_to_rubles(self.usd_transaction)

        # Проверяем вызов API
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            headers={"apikey": "test-key"},
            params={"base": "USD", "symbols": "RUB"},
        )

        # Проверяем результат конвертации (100 * 75.50 = 7550.00)
        self.assertEqual(result, 7550.00)

    @patch.dict("os.environ", {"FOREX_API_KEY": "test-key"})
    @patch("currency_converter.requests.get")
    def test_eur_transaction(self, mock_get: Mock) -> None:
        """
        Тест: транзакция в евро (с вызовом API).
        """
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 89.25}}
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = convert_to_rubles(self.eur_transaction)

        # Проверяем вызов API
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            headers={"apikey": "test-key"},
            params={"base": "EUR", "symbols": "RUB"},
        )

        # Проверяем результат конвертации (50 * 89.25 = 4462.50)
        self.assertEqual(result, 4462.50)

    @patch.dict("os.environ", {"FOREX_API_KEY": "test-key"})
    @patch("currency_converter.requests.get")
    def test_api_timeout(self, mock_get: Mock) -> None:
        """
        Тест: таймаут при вызове API.
        """
        # Мокируем исключение таймаута
        mock_get.side_effect = requests.exceptions.Timeout

        # Проверяем, что исключение пробрасывается дальше
        with self.assertRaises(requests.exceptions.Timeout):
            convert_to_rubles(self.usd_transaction)
