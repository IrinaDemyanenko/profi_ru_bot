"""Встроенный браузер, в котором будет работать пользователь."""
import os
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QStandardPaths
from PySide6.QtWebEngineCore import (
    QWebEngineProfile, QWebEnginePage)


class Browser(QWebEngineView):
    """Встроенный браузер.

    Нужен, чтобы пользователь мог не переключаться из окна бота,
    а сразу отвечать на заявки в этом же окне.

    Чтобы не логиниться на сайте всякий раз заново, создаёт профиль и пути
    хранения данных профиля (куки, кэш, сессия).

    load_url: Браузер сразу же будет переходит на заданную страницу.
    """
    def __init__(self, parent=None, proxy_url: str | None = None):  # parent=None чтобы браузер мог быть и самостоят. и эл-том внутри окна
        # если передан proxy_url — указываем его через Chromium-флаг
        if proxy_url:
            # пример: "http://123.45.67.89:8080" или "socks5://127.0.0.1:9050"
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--proxy-server={proxy_url}"
            print(f"[DEBUG] Прокси установлен: {proxy_url}")

        #глобальные флаги Chromium (для SameSite и кук)
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
            "--enable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure "
            "--disable-features=AutoupgradeMixedContent "
            "--disable-web-security "
            "--allow-running-insecure-content"
        )

        super().__init__(parent)

        # папка для хранения данных профиля на компьютере
        base_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        profile_folder = os.path.join(base_path, 'profi_profile')
        os.makedirs(profile_folder, exist_ok=True)

        print(base_path)

        # создаём именованный профиль во встроенном браузере
        profile = QWebEngineProfile('ProfiProfile', self)  # self это браузер
        # пути хранения временных файлов и кэша
        profile.setPersistentStoragePath(os.path.join(profile_folder, 'storage'))
        profile.setCachePath(os.path.join(profile_folder, 'cache'))

        # хранить все куки, не только разрешённые, а все!
        try:
            profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        except AttributeError:
            profile.PersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        # добавляем User-Agent, чтобы сайт думал, что это
        profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36")

        #язык и кэш, чтобы сайт видел русского пользователя с локальным кэшем
        profile.setHttpAcceptLanguage("ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)

        # !!!ключевой момент - привязываем профиль к браузеру Chrome на Windows
        page = QWebEnginePage(profile, self)
        self.setPage(page)

    def load_url(self, url:str):
        """Загружает страницу по переданному адресу."""
        self.setUrl(QUrl(url))

    def open_devtools(self):
        """Открывает встроенные DevTools в отдельном окне.

        При нажатии кнопки DevTools откроется отдельное окно-инспектор.
        Можно будет смотреть консоль, сетевые запросы, html-структуру
        и тестировать, как в обычном Chrome.
        """
        dev_tools = QWebEngineView()
        dev_tools_page = QWebEnginePage(self.page().profile(), dev_tools)
        dev_tools.setPage(dev_tools_page)
        self.page().setDevToolsPage(dev_tools_page)
        dev_tools.setWindowTitle("DevTools")
        dev_tools.resize(900, 700)
        dev_tools.show()
