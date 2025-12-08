import pytest
import os
import tempfile
from typing import Callable

from src.decorators import log


# ==================== ФИКСТУРЫ ====================


@pytest.fixture
def temp_log_file() -> str:
    """Создает временный файл для тестирования записи логов."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
        temp_file = f.name

    yield temp_file

    # Удаляем временный файл после теста
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def sample_function() -> Callable:
    """Тестовая функция для декорирования."""

    def func(x: int, y: int) -> int:
        return x + y

    return func


@pytest.fixture
def error_function() -> Callable:
    """Тестовая функция, которая вызывает исключение."""

    def func(x: int, y: int) -> int:
        raise ValueError("Test error")

    return func


@pytest.fixture
def slow_function() -> Callable:
    """Тестовая функция для тестирования производительности."""
    import time

    def func() -> str:
        time.sleep(0.01)  # Небольшая задержка
        return "Done"

    return func


# ==================== ТЕСТЫ ДЛЯ ДЕКОРАТОРА log ====================


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_decorator_returns_decorator(self) -> None:
        """Проверяем, что log возвращает декоратор."""
        decorator = log()
        assert callable(decorator)

        decorator_with_file = log(filename="test.txt")
        assert callable(decorator_with_file)

    def test_log_success_to_console(self, sample_function: Callable, capsys: pytest.CaptureFixture) -> None:
        """Проверяем логирование успешного выполнения в консоль."""
        decorated_func = log()(sample_function)

        result = decorated_func(1, 2)

        # Проверяем результат функции
        assert result == 3

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "ok" in captured.out
        assert sample_function.__name__ in captured.out

    def test_log_success_to_file(self, temp_log_file: str, sample_function: Callable) -> None:
        """Проверяем логирование успешного выполнения в файл."""
        decorated_func = log(filename=temp_log_file)(sample_function)

        result = decorated_func(3, 4)

        # Проверяем результат функции
        assert result == 7

        # Проверяем запись в файл
        with open(temp_log_file, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "ok" in log_content
        assert sample_function.__name__ in log_content

    def test_log_error_to_console(self, error_function: Callable, capsys: pytest.CaptureFixture) -> None:
        """Проверяем логирование ошибки в консоль."""
        decorated_func = log()(error_function)

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError, match="Test error"):
            decorated_func(1, 2)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "error" in captured.out
        assert "ValueError" in captured.out
        assert error_function.__name__ in captured.out
        assert "Inputs:" in captured.out
        assert "(1, 2)" in captured.out

    def test_log_error_to_file(self, temp_log_file: str, error_function: Callable) -> None:
        """Проверяем логирование ошибки в файл."""
        decorated_func = log(filename=temp_log_file)(error_function)

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError, match="Test error"):
            decorated_func(5, 6)

        # Проверяем запись в файл
        with open(temp_log_file, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "error" in log_content
        assert "ValueError" in log_content
        assert error_function.__name__ in log_content
        assert "Inputs:" in log_content
        assert "(5, 6)" in log_content
