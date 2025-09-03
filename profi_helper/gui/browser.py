"""Встроенный браузер, в котором будет работать пользователь."""
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl



class Browser(QWebEngineView):
    """Встроенный браузер.

    Нужен, чтобы пользователь мог не переключаться из окна бота,
    а сразу отвечать на заявки в этом же окне.

    load_url: Браузер сразу же будет переходит на заданную страницу.
    """
    def __init_(self, parent=None):  # parent=None чтобы браузер мог быть и самостоят. и эл-том внутри окна
        super().__init__(parent)

    def load_url(self, url:str):
        """Загружает страницу по переданному адресу."""
        self.setUrl(QUrl(url))
