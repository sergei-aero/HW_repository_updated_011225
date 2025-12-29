import logging
from typing import Union
from pathlib import Path

# Получаем путь к текущему файлу (masks.py)
current_file = Path(__file__).resolve()

project_root = current_file.parent.parent

log_dir = project_root / "logs"
log_file = log_dir / "masks.log"

log_dir.mkdir(exist_ok=True)


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file)
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX

    """
    card_str = str(card_number).replace(" ", "")

    if len(card_str) != 16 or not card_str.isdigit():
        logger.error("Произошла ошибка! Номер карты должен состоять из 16 цифр")
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    return masked_card


def get_mask_account(account_number: Union[int, str]) -> str:
    """
    Маскирует номер счета в формате **XXXX

    """
    account_str = "".join(filter(str.isdigit, str(account_number)))

    if len(account_str) < 6:
        logger.error("Произошла ошибка! Номер счета должен содержать минимум 6 цифр")
        raise ValueError("Номер счета должен содержать минимум 6 цифр")

    return f"**{account_str[-4:]}"
