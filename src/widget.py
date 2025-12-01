from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(account_card_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке
    """
    parts = account_card_info.split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер карты/счета")

    card_type = " ".join(parts[:-1])
    number = parts[-1]

    if card_type.lower().startswith("счет") or len(number) > 16:
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ
    """
    # Разделяем дату и время по символу 'T'
    date_part = date_string.split("T")[0]

    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
