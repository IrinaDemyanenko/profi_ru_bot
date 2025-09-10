"""Парсер DOM страницы с заказами, чтобы бот находил новые заявки."""
from PySide6.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup


class Parser():
    """Парсер вэб-страницы с двумя режимами работы 'html' или 'js'."""
    def __init__(self, browser: QWebEngineView, mode: str = 'js'):
        """
        browser - встроенный браузер (QWebEngineView)
        mode - режим работы
            'html' - получение всей страницы и парсинг через BeautifulSoup,
            'js' - выполнение JavaScript и извлечение ID заказов напрямую.
        """
        self.browser = browser
        self.mode = mode

    def get_orders(self, callback):
        """Запускает поиск заказов и передаёт результат в callback.

        callback - callback - функция, которая примет результат:
        0 - нет новых заказов,
        1 - есть новые заказы,
        -1 - другой результат / ошибка
        """
        if self.mode == 'html':
            self.browser.page().toHtml(
                lambda html: callback(self._parse_html(html))
                )
        else:
            js_code = self._get_js_code()
            self.browser.page().runJavaScript(
                js_code,
                lambda result: callback(self._parse_js(result))
                )

    def _parse_html(self, html: str):
        """Парсинг HTML страницы с помощью BeautifulSoup.
        Из полученного файла HTML создаёт DOM дерево, ищет
        непросмотренные заказы по тегу или разделитель.
        """
        tree = BeautifulSoup(html, 'html.parser')
        container = tree.select_one('#content-content')
        if not container:
            return -1

        for item in container.find_all('div', recursive=False):
            if item.get('id') == 'DIVIDER':
                return 0
            if item.select_one('a[data-testid]'):
                return 1
        return -1

    def _get_js_code(self):
        """Возвращает JavaScript-код, который смотрит id первого
        элемента и оценивает его:

        - если это непросмотренный заказ - вернёт 1;
        - если разделитель, который ставится
        между просмотренными заказами и новыми - то вернёт 0;
        - если ничего из этого - то -1.
        """
        return """
        (function() {
            var items = document.querySelectorAll('#content-content > div');
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                if (item.id === 'DIVIDER') return 0;
                if (item.querySelector('a[data-testid]')) return 1;
            }
            return -1;
        })();
        """


    def _parse_js(self, result):
        """Обрабатывает результат выполнения JS и возвращает

        0 - нет новых заказов;
        1 - есть новые заказы;
        -1 - другой результат.
        """
        print("DEBUG js ->", result)  # добавили отладочный вывод
        try:
            return int(result)
        except (ValueError, TypeError):
            return -1


    # для отладки
    def dump_html(self, filename="debug_page.html"):
        """Сохраняет текущий HTML страницы в файл для отладки."""
        def _save(html):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[DEBUG] HTML страницы сохранён в {filename}")

        self.browser.page().toHtml(_save)
