"""Здесь всё, что будет в главном окне программы: браузер, кнопки старт и стоп."""
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from gui.browser import Browser
from gui.control_buttons import Control_buttons
from core.refresher import Refresher
from core.watcher import Watcher
from core.notifier import Notifier
from utils.storage import Storage



class MainWindow(QMainWindow):
    """Собирает элементы для главного окна приложения."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profi Helper")

        # основной пустой контейнер, в котором всё разместим
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # расположим в окне все эл-ты вертикально
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # добавим встроенный браузер в виджет
        self.browser = Browser(self)  # здесь self это parent, те родителем браузера будет главное окно
        self.browser.load_url('https://profi.ru/')

        # добавим виджет с кнопками старт и стоп
        self.control_panel = Control_buttons(self)  # self это parent, делаем панель с кнопками дочерним виджетом по отношению к главному окну

        # добавим хранилище
        self.storage = Storage()

        # отслеживание новых заявок и уведомление
        self.notifier = Notifier()
        self.watcher = Watcher(self.browser, self.storage, self.notifier)

        # собираем всё в окне
        layout.addWidget(self.browser, stretch=1)
        layout.addWidget(self.control_panel, stretch=0)

        # добавим обновление страницы
        self.refresher = Refresher(
            browser=self.browser,
            watcher=self.watcher,
            interval=5000
        )

        # соединяем кнопки с сигналами
        self.control_panel.start_button.clicked.connect(self.on_start)
        self.control_panel.stop_button.clicked.connect(self.on_stop)


    def on_start(self):
        """Запускает обновление страницы, делает кнопку старт неактивной."""
        self.control_panel.start_button.setEnabled(False)
        self.control_panel.stop_button.setEnabled(True)
        self.refresher.start()
        print('Бот Профи.ру запущен')

    def on_stop(self):
        """Останавливает обновление страницы, кнопка старт снова активна, стоп - неаутивна."""
        self.control_panel.start_button.setEnabled(True)
        self.control_panel.stop_button.setEnabled(False)
        self.refresher.stop()
        print('Бот Профи.ру остановлен')
