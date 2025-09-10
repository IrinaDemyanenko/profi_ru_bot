"""Наблюдатель, который отслеживает новые заявки и включает уведомление."""
from core.parser import Parser
from utils.storage import Storage


class Watcher():
    """Класс связывает парсер, браузер, хранилище заявок и уведомления."""
    def __init__(self, browser, storage: Storage, notifier, mode='js'):
        """
        browser - встроенный браузер (QWebEngineView),
        storage - хранилище заказов (сейчас множество, можно заменить на SQLite),
        notifier - объект для уведомлений (звук, popup и т.д.),
        mode - режим парсинга: "html" или "js".
        """
        self.browser = browser
        self.storage = storage
        self.notifier = notifier
        self.parser = Parser(self.browser, mode)

    def check_new_orders(self):
        """Запрашивает через парсер наличие новых заказов (0\1\-1)
        и обрабатывает результат.
        """
        try:
            self.parser.get_orders(self._process_orders)
        except Exception as e:
            print(f'Ошибка при проверке заказов: {e}')

    def _process_orders(self, result: int):
        """Получает от парсера:
            1 - есть новая заявка
            0 - нет новых заявок
           -1 - ошибка или неожиданный результат
        Если есть -  включает звуковое/текстовое уведомление.
        """
        print("DEBUG: парсер вернул ->", result)

        if result == 0:
            print('Новых заявок нет!')
            # Сохраняем HTML для анализа
            # self.parser.dump_html("debug_no_orders.html")
            # self.storage.debug_print()
            return

        elif result == 1:
            self.notifier.sound_notify()
            # self.notifier.popup_notify(message='Найдена новая заявка') пока выключим

        else:
            print('Непредвиденный результат от парсера, смотри HTML для анализа.')
            self.parser.dump_html('debug_parser.html')
