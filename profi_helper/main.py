"""Точка входа."""
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow



def start_profi_helper():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # делаем окно видимым
    sys.exit(app.exec())  # главный цикл событий Qt, а потом выход


if __name__ == '__main__':
    start_profi_helper()
