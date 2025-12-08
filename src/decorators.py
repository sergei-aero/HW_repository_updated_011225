import functools
from typing import Callable, Any, Optional
from datetime import datetime


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для автоматического логирования начала и конца выполнения функции.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декоратор, который логирует вызов функции.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем сообщение для логирования
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{timestamp} - {func_name} ok"

                # Логируем результат
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                log_message = f"{timestamp} - {func_name} error: {error_type}. Inputs: {args}, {kwargs}"

                # Логируем ошибку
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                else:
                    print(log_message)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
