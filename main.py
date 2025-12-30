import sys
import os
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


from src.utils import load_json_operations
from src.data_reader_operating import read_csv_file, read_excel_file, process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency


def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Получение выбора пользователя
    choice = input("\nВаш выбор: ").strip()

    # Определение пути к файлу данных
    data_folder = os.path.join(os.path.dirname(__file__), "data")

    # Загрузка данных в зависимости от выбора
    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        file_path = os.path.join(data_folder, "operations.json")
        transactions: List[Dict[str, Any]] = load_json_operations(file_path)

    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        file_path = os.path.join(data_folder, "transactions.csv")
        transactions = read_csv_file(file_path)

    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        file_path = os.path.join(data_folder, "transactions_excel.xlsx")
        transactions = read_excel_file(file_path)

    else:
        print("\nНекорректный выбор. Программа завершена.")
        return

    print(f"Загружено {len(transactions)} транзакций.")

    # Фильтрация по статусу
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("Статус: ").strip().upper()

        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            transactions = filter_by_state(transactions, status)
            print(f'\nОперации отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'\nСтатус операции "{status}" недоступен.')
            print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    # Сортировка по дате
    while True:
        sort_answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()

        if sort_answer in ["да", "нет"]:
            if sort_answer == "да":
                while True:
                    order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

                    if order in ["по возрастанию", "по убыванию"]:
                        reverse = order == "по убыванию"
                        transactions = sort_by_date(transactions, reverse)
                        break
                    else:
                        print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")
            break
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'")

        # Фильтрация по валюте
        print("\nТранзакции в какой валюте выводить?")
        print("Примеры валют: RUB, USD, EUR")
        currency = input("Введите код валюты: ").strip().upper()

        # Фильтрация по выбранной валюте
        transactions = list(filter_by_currency(transactions, currency))
        print(f"Отфильтрованы транзакции в валюте: {currency}")

    # Фильтрация по описанию
    while True:
        desc_answer = (
            input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        )

        if desc_answer in ["да", "нет"]:
            if desc_answer == "да":
                keyword = input("Введите слово для поиска в описании: ").strip()
                if keyword:
                    transactions = process_bank_search(transactions, keyword)
            break
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")


if __name__ == "__main__":
    main()
