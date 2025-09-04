"""Логика автообновления страницы"""
from PySide6.QtCore import QTimer



class Refresher():
    """Отвечает за логику обновления вэб-страницы в переданном браузере
    с заданной частотой обновления.

    browser - это объект QWebEngineView;
    interval - интервал обновления в миллисекундах (по умолчанию 5 секунд).
    """
    def __init__(self, browser, watcher, interval=5000):
        self.browser = browser
        self.interval = interval
        self.timer = QTimer()
        self.watcher = watcher
        self.timer.timeout.connect(self.refresh)

    def start(self):
        """Запускает таймер."""
        self.timer.start(self.interval)

    def stop(self):
        """Оставнавливает таймер."""
        self.timer.stop()

    def refresh(self):
        """Перезагружает страницу."""
        self.browser.reload()
        self.watcher.check_new_orders()  # проверяет наличие новых заявок
        print('Обновляется страница')
