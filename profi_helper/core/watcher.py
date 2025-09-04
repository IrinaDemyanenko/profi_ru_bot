"""Наблюдатель, который отслеживает новые заявки и включает уведомление."""
from PySide6.QtWebEngineWidgets import QWebEngineView
from utils.storage import Storage
from bs4 import BeautifulSoup


class Watcher():
    """Класс связывает встроенный браузер, хранилище заявок и уведомления."""
    def __init__(self, browser: QWebEngineView, storage: Storage, notifier):
        self.browser = browser
        self.storage = storage
        self.notifier = notifier

    def check_new_orders(self):
        """Связывает две функции: асинхронно запрашивает HTML
        и применяет к нему поиск новых заказов."""
        try:
            self.browser.page().toHtml(self.process_html)
        except Exception as e:
            print(f'Ошибка при получении файла HTML: {e}')

    def process_html(self, html: str):
        """Из полученного файла HTML создаёт DOM дерево.
        Ищет новые заказы по тегу и сравнивает с хранилищем.
        Если находит, включает звуковое/текстовое уведомление.
        """
        tree = BeautifulSoup(html, 'html.parser')  # 'html.parser' встроенный парсер, медленный, есть быстрее

        orders = tree.find_all('div', class_='order-card')
        if not orders:
            print('Заказы не найдены!')
            return
        # если заказов нет, вернётся, если есть, будем искать "новые"
        for order in orders:
            order_id = order.get('data-id') or order.text.strip()[:30]
            if self.storage.is_new(order_id):
                self.notifier.sound_notify()
                # self.notifier.popup_notify(message='Найдена новая заявка') пока выключим
