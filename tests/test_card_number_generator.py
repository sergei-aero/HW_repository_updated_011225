"""
Тесты для генератора card_number_generator.
"""

import pytest
import re
from typing import Iterator
from collections.abc import Generator

from src.generators import card_number_generator


# ==================== ФИКСТУРЫ ====================


@pytest.fixture
def card_format_pattern() -> re.Pattern:
    """Фикстура с регулярным выражением для проверки формата номера карты."""
    return re.compile(r"^\d{4} \d{4} \d{4} \d{4}$")


@pytest.fixture(
    params=[
        (1, 5),  # Базовый случай из примера
        (1, 1),  # Один номер
        (9996, 9999),  # Близко к границе 4-значного числа
        (100, 105),  # Трехзначные числа
        (9990, 9995),  # Верхняя граница диапазона
    ]
)
def number_ranges(request: pytest.FixtureRequest) -> tuple[int, int]:
    """Параметризованная фикстура для разных диапазонов генерации."""
    return request.param


# ==================== ТЕСТЫ ====================


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    def test_returns_iterator(self) -> None:
        """Проверяем, что функция возвращает итератор."""
        result = card_number_generator(1, 5)
        assert isinstance(result, Iterator)
        assert isinstance(result, Generator)

    def test_correct_range_length(self, number_ranges: tuple[int, int]) -> None:
        """Проверяем, что генератор выдает правильное количество номеров."""
        start, end = number_ranges
        expected_count = end - start + 1

        numbers = list(card_number_generator(start, end))

        assert len(numbers) == expected_count

    def test_card_format_matches_pattern(
        self, number_ranges: tuple[int, int], card_format_pattern: re.Pattern
    ) -> None:
        """Проверяем корректность форматирования номеров карт."""
        start, end = number_ranges

        for card_number in card_number_generator(start, end):
            assert card_format_pattern.match(card_number)

    def test_numbers_in_correct_order(self, number_ranges: tuple[int, int]) -> None:
        """Проверяем, что номера идут в правильном порядке."""
        start, end = number_ranges

        numbers = list(card_number_generator(start, end))

        # Проверяем порядок номеров
        for i, card_number in enumerate(numbers):
            expected_last_four = f"{start + i:04d}"
            assert card_number.endswith(expected_last_four)

    def test_generator_exhaustion(self) -> None:
        """Проверяем, что генератор корректно завершает генерацию."""
        generator = card_number_generator(1, 3)

        # Извлекаем все элементы
        for _ in range(3):
            next(generator)

        # Проверяем, что генератор исчерпан
        with pytest.raises(StopIteration):
            next(generator)

    @pytest.mark.parametrize(
        "start, end, expected_first, expected_last",
        [
            (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
            (9996, 9999, "0000 0000 0000 9996", "0000 0000 0000 9999"),
            (100, 102, "0000 0000 0000 0100", "0000 0000 0000 0102"),
        ],
    )
    def test_boundary_values(self, start: int, end: int, expected_first: str, expected_last: str) -> None:
        """Параметризованный тест для проверки крайних значений диапазона."""
        numbers = list(card_number_generator(start, end))

        assert numbers[0] == expected_first
        assert numbers[-1] == expected_last

    def test_example_from_assignment(self) -> None:
        """Проверяем пример использования из задания."""
        result = list(card_number_generator(1, 5))

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]

        assert result == expected

    @pytest.mark.parametrize(
        "start, end",
        [
            (0, 5),  # Начинается с 0
            (9995, 10000),  # Включает 5-значное число (должно работать)
            (-1, "3"),  # Отрицательное начало (ожидаем ошибку при форматировании)
        ],
    )
    def test_various_ranges(self, start: int, end: int) -> None:
        """Проверяем генератор с различными диапазонами."""
        if start < 0:
            # Отрицательные числа не могут быть отформатированы как 04d
            with pytest.raises(TypeError):
                list(card_number_generator(start, end))
        else:
            numbers = list(card_number_generator(start, end))
            assert len(numbers) == end - start + 1

    def test_large_range_performance(self) -> None:
        """Проверяем, что генератор может обрабатывать большие диапазоны лениво."""
        generator = card_number_generator(1, 1000)

        # Берем только первые 5 элементов
        first_five = [next(generator) for _ in range(5)]

        # Генератор должен продолжать работать
        sixth = next(generator)

        assert len(first_five) == 5
        assert sixth == "0000 0000 0000 0006"
