from src.masks import get_mask_card_number, get_mask_account

from src.generators import card_number_generator


def main():
    """Простая демонстрация функций"""
    # Примеры использования
    card = "7000792289606361"
    account = "73654108430135874305"

    print("Примеры маскирования:")
    print(f"Карта: {card} -> {get_mask_card_number(card)}")
    print(f"Счет: {account} -> {get_mask_account(account)}")


    list(card_number_generator(-1, 5))
main()