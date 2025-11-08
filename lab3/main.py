import sys
from PyQt6.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Приложение заметок")
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
