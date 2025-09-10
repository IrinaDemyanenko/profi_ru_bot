"""Точка входа."""
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.logger import get_logger



def start_profi_helper():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # делаем окно видимым
    sys.exit(app.exec())  # главный цикл событий Qt, а потом выход


if __name__ == '__main__':
    get_logger().info('Запуск бота Профи.ру')
    try:
        start_profi_helper()
    except Exception as e:
        get_logger().exception(f'Ошибка при запуске бота Профи.ру: {e}')
