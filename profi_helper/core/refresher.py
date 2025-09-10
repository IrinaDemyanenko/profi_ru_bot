"""Логика автообновления страницы"""
from PySide6.QtCore import QTimer
from utils.random_interval import get_random_interval


class Refresher():
    """Отвечает за логику обновления вэб-страницы в переданном браузере
    с заданной частотой обновления.

    Ждёт сигнала loadFinished о полной загрузки страницы и,
    только получив ok == True включает анализ содержимого страницы
    self.watcher.check_new_orders().

    browser - это объект QWebEngineView;
    interval - интервал обновления в миллисекундах (случайный от 7-15 сек.).
    """
    def __init__(self, browser, watcher, min_interval=7000, max_interval=15000):
        self.browser = browser
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.timer = QTimer()
        self.watcher = watcher
        self.timer.timeout.connect(self.refresh)

    def start(self):
        """Запускает таймер."""
        self._set_next_rand_interval()

    def stop(self):
        """Оставнавливает таймер."""
        self.timer.stop()

    def refresh(self):
        """Перезагружает страницу."""
        # подключаем одноразовый слот на сигнал loadFinished
        self.browser.page().loadFinished.connect(self._on_load_finished)
        self.browser.reload()
        print('Обновляется страница')

    def _on_load_finished(self, ok):
        """Вызывается после полной загрузки страницы."""
        # после получения loadFinished отключаем слот,
        # чтобы для этой перезагрузки о сработал только один раз
        self.browser.page().loadFinished.disconnect(self._on_load_finished)
        if ok:  # если Qt вернёт true
            self.watcher.check_new_orders()  # проверяет наличие новых заявок
        else:
            print('Ошибка загрузки страницы!')

        self._set_next_rand_interval()  # назначаем новый случайный интервал только после полной загрузки

    def _set_next_rand_interval(self):
        """Устанавливает случайный интервал перед следующим обновлением."""
        interval = get_random_interval(self.min_interval, self.max_interval)
        print(f'Следующее обновление через {interval} мс.')
        self.timer.start(interval)
