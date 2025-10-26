import re
import urllib.request
import urllib.error
from binary_divisible_by_three import is_divisible_by_three


def load_and_check_from_file(filename: str):

    # Загружает двоичные числа из файла и проверяет их на кратность 3.

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        results = []
        for i, line in enumerate(lines, 1):
            binary = line.strip()
            if binary:
                try:
                    result = is_divisible_by_three(binary)
                    decimal = int(binary, 2)
                    results.append(
                        {
                            "line": i,
                            "binary": binary,
                            "decimal": decimal,
                            "divisible": result,
                        }
                    )
                except ValueError as e:
                    print(f"Строка {i}: {binary} - Ошибка: {e}")

        return results
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []


def user_input_check():

    # Позволяет пользователю вводить одно двоичное число для проверки.

    binary = input("\nВведите двоичное число: ").strip()

    if not binary:
        print("Пустая строка.")
        return

    try:
        result = is_divisible_by_three(binary)
        decimal = int(binary, 2)
        print(
            f"  {binary} (десятичное: {decimal}) {'делится на 3' if result else 'не делится на 3'}"
        )
    except ValueError as e:
        print(f"  Ошибка: {e}")


def print_results(results):

    # Выводит результаты проверки бинарных чисел.

    if not results:
        print("Нет результатов для вывода.")
        return

    print("\nРезультаты проверки:")
    print("-" * 60)
    for r in results:
        status = "да" if r["divisible"] else "нет"
        print(
            f"Строка {r['line']}: {r['binary']} = {r['decimal']} - делится на 3: {status}"
        )
    print()


def find_binary_numbers(text: str):

    # Извлекает двоичные числа из текста.

    # Ищем числа длиной от 3 символов, где начинается с 1
    pattern = r"\b1[01]{2,}\b"
    return re.findall(pattern, text)


def analyze_url_content(url: str = "https://www.convertbinary.com/numbers/"):

    # Открывает URL, находит все двоичные числа и проверяет их на кратность 3.

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            html = response.read().decode(encoding)

            binary_numbers = find_binary_numbers(html)

            results = []
            for binary in binary_numbers:
                try:
                    result = is_divisible_by_three(binary)
                    decimal = int(binary, 2)
                    results.append(
                        {"binary": binary, "decimal": decimal, "divisible": result}
                    )
                except ValueError:
                    # Пропускаем некорректные числа
                    continue

            return results
    except urllib.error.URLError as e:
        print(f"Проблема открытия {url}: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def main():
    # Главное меню программы.
    while True:
        print("\nМеню:")
        print("1 - Проверка из файла data.txt")
        print("2 - Пользовательский ввод")
        print("3 - Поиск двоичных чисел на веб-странице")
        print("0 - Выход")

        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            results = load_and_check_from_file("data.txt")
            print_results(results)

        elif choice == "2":
            user_input_check()

        elif choice == "3":
            url = input("Введите URL: ").strip()
            if url:
                print("\nОбработка...")

                results = analyze_url_content(url)
                countLimit = 50
                if results:
                    divisible_count = sum(
                        1 for r in results if r["divisible"]
                    )  # if r["divisible"]
                    print(f"\nНайдено двоичных чисел: {len(results)}")
                    print(f"Кратных 3: {divisible_count}")

                    print("\nПримеры чисел, кратных 3:")
                    examples = [r for r in results if r["divisible"]][
                        :countLimit
                    ]  # if r["divisible"]

                    for r in examples:
                        print(f"  {r['binary']} = {r['decimal']} {r['divisible']}")

                    if divisible_count > countLimit:
                        print(f"  ... и еще {divisible_count - countLimit} чисел")
                else:
                    print("\nДвоичные числа не найдены.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
