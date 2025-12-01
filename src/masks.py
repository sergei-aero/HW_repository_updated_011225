from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX

    """
    card_str = str(card_number).replace(" ", "")

    if len(card_str) != 16 or not card_str.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    return masked_card


def get_mask_account(account_number: Union[int, str]) -> str:
    """
    Маскирует номер счета в формате **XXXX

    """
    account_str = "".join(filter(str.isdigit, str(account_number)))

    if len(account_str) < 6:
        raise ValueError("Номер счета должен содержать минимум 6 цифр")

    return f"**{account_str[-4:]}"
