import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
from PyQt6.QtGui import QFontDatabase, QFont, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt


# Загружаем шрифты из assets/fonts/ и возвращаем словарь с категориями
def load_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "assets", "fonts")

    print(f"Ищем шрифты в: {base_path}")
    print(f"Путь существует: {os.path.exists(base_path)}")

    font_categories = {"main_fonts": [], "decorative_fonts": []}

    # Загружаем все шрифты из папок
    for category in ["main_fonts", "decorative_fonts"]:
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            print(f"Папка не найдена: {category_path}")
            continue

        print(f"Загружаем из: {category_path}")

        for font_folder_name in sorted(os.listdir(category_path)):
            font_folder_path = os.path.join(category_path, font_folder_name)
            if not os.path.isdir(font_folder_path):
                continue

            font_files = [
                f for f in os.listdir(font_folder_path) if f.endswith((".ttf", ".otf"))
            ]

            if not font_files:
                continue

            # Загружаем все файлы шрифтов из папки
            loaded_font_ids = []
            for file_name in font_files:
                font_file_path = os.path.join(font_folder_path, file_name)
                font_id = QFontDatabase.addApplicationFont(font_file_path)
                if font_id != -1:
                    loaded_font_ids.append(font_id)

            loaded = len(loaded_font_ids) > 0

            # Если загрузили шрифты, определяем название семейства
            if loaded:
                family_name = None

                # Получаем название семейства из загруженных шрифтов
                for font_id in loaded_font_ids:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    if families:
                        family_name = families[0]
                        break

                # Если не получили через applicationFontFamilies, ищем в базе данных
                if not family_name:
                    all_families = QFontDatabase.families()

                    # Точное совпадение названия папки
                    if font_folder_name in all_families:
                        family_name = font_folder_name
                    else:
                        # Учитываем регистр
                        font_folder_lower = font_folder_name.lower().replace(" ", "")
                        for family in all_families:
                            family_lower = family.lower().replace(" ", "")
                            if font_folder_lower == family_lower:
                                family_name = family
                                break
                            # Название папки содержится в названии семейства
                            if (
                                font_folder_lower in family_lower
                                and len(font_folder_lower) >= 3
                            ):
                                family_name = family
                                break

                # Если всё ещё не нашли, используем название папки
                if not family_name:
                    family_name = font_folder_name

                # Добавляем в категорию
                if family_name and family_name not in font_categories[category]:
                    font_categories[category].append(family_name)
                    print(
                        f"  - Добавлен шрифт: {family_name} (из папки: {font_folder_name})"
                    )

    # Сортируем
    for category in font_categories:
        font_categories[category] = sorted(set(font_categories[category]))

    return font_categories


class NotesApp(QWidget):
    def __init__(self, font_categories):
        super().__init__()

        self.font_categories = font_categories

        self.setWindowTitle("Приложение заметок")
        self.resize(600, 500)

        layout = QVBoxLayout()

        self.title_label = QLabel("Моя заметка it's my text")
        self.title_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        layout.addWidget(self.title_label)

        # Текстовое поле
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Горизонтальный layout для выбора шрифта и жирности
        font_layout = QHBoxLayout()

        # Список выбора шрифта
        self.font_select = QComboBox()
        font_layout.addWidget(self.font_select)

        # Поле для ввода жирности
        weight_label = QLabel("Жирность:")
        font_layout.addWidget(weight_label)

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("100-900")
        self.weight_input.setMaximumWidth(100)
        font_layout.addWidget(self.weight_input)

        layout.addLayout(font_layout)

        self.load_font_list()
        self.font_select.currentTextChanged.connect(self.apply_font)
        self.weight_input.textChanged.connect(self.on_weight_changed)

        self.setLayout(layout)

    # Загружаем названия шрифтов с разделением по категориям
    def load_font_list(self):
        self.font_select.clear()

        # Используем модель для управления элементами
        model = QStandardItemModel()

        # Добавляем основные шрифты
        if self.font_categories["main_fonts"]:
            separator_item = QStandardItem("─── Основные шрифты ───")
            separator_item.setEnabled(False)
            model.appendRow(separator_item)

            for font in self.font_categories["main_fonts"]:
                font_item = QStandardItem(font)
                model.appendRow(font_item)

        # Добавляем декоративные шрифты
        if self.font_categories["decorative_fonts"]:
            separator_item = QStandardItem("─── Декоративные шрифты ───")
            separator_item.setEnabled(False)
            model.appendRow(separator_item)

            for font in self.font_categories["decorative_fonts"]:
                font_item = QStandardItem(font)
                model.appendRow(font_item)

        self.font_select.setModel(model)

        # Устанавливаем первый доступный шрифт по умолчанию
        for i in range(model.rowCount()):
            item = model.item(i)
            if item and item.isEnabled():
                self.font_select.setCurrentIndex(i)
                break

    # Обработчик изменения жирности
    def on_weight_changed(self, text):
        self.apply_font()

    # Меняем шрифт текста
    def apply_font(self, font_name=None):
        # Получаем текущий выбранный шрифт
        if font_name is None:
            current_index = self.font_select.currentIndex()
            model = self.font_select.model()
            if model:
                item = model.item(current_index)
                if not item or not item.isEnabled():
                    return
            font_name = self.font_select.currentText()

        # Пропускаем разделители
        if not font_name or font_name.startswith("───"):
            return

        # Получаем жирность из поля ввода
        weight_text = self.weight_input.text().strip()

        # Создаём шрифт
        font = QFont(font_name, 12)

        # Устанавливаем жирность, если она указана
        if weight_text:
            try:
                weight = int(weight_text)
                weight = max(100, min(900, weight))
                font.setWeight(weight)
            except ValueError:
                pass

        # Применяем шрифт
        self.text_edit.setFont(font)
        self.title_label.setFont(font)


def main():
    app = QApplication(sys.argv)

    # Загружаем шрифты
    font_categories = load_fonts()

    # Отладочный вывод
    print("=" * 50)
    print("Загруженные шрифты:")
    print(
        f"Основные ({len(font_categories['main_fonts'])}): {font_categories['main_fonts']}"
    )
    print(
        f"Декоративные ({len(font_categories['decorative_fonts'])}): {font_categories['decorative_fonts']}"
    )
    print("=" * 50)

    window = NotesApp(font_categories)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
