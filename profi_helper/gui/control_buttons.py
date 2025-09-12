"""Виджиты кнопок и старт и стоп и самой панели управления."""
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt



class Control_buttons(QWidget):
    """Виджет-контейнер с двумя кнопками старт и стоп.

    Только создаёт кнопки, располагает их горизонтально и показывает,
    без логики дальнейшей работы (только отрисовка кнопок).
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.start_button = QPushButton('Старт')  # создадим кнопки старт и стоп
        self.stop_button = QPushButton('Стоп')

        self.start_button.setMinimumHeight(60)  # чтобы кнопки не расползались по экрану
        self.start_button.setMaximumHeight(100)
        self.start_button.setMinimumWidth(100)
        self.start_button.setMaximumWidth(150)

        self.stop_button.setMinimumHeight(60)  # чтобы кнопки не расползались по экрану
        self.stop_button.setMaximumHeight(100)
        self.stop_button.setMinimumWidth(100)
        self.stop_button.setMaximumWidth(150)

        self.stop_button.setEnabled(False)  # при запуске стоп не активна

        layout = QHBoxLayout()  # две кнопки рядом в горизонтальной раскладке
        layout.addStretch()  # прижать всё к правому краю
        layout.addWidget(self.start_button, alignment=Qt.AlignRight)
        layout.addWidget(self.stop_button, alignment=Qt.AlignRight)
        # layout.addStretch()  # прижать всё к левому краю
        self.setLayout(layout)
