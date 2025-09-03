"""Виджиты кнопок и старт и стоп и самой панели управления."""
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout



class Control_buttons(QWidget):
    """Виджет-контейнер с двумя кнопками старт и стоп.

    Только создаёт кнопки, располагает их горизонтально и показывает,
    без логики дальнейшей работы (только отрисовка кнопок).
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.start_button = QPushButton('Старт')  # создадим кнопки старт и стоп
        self.stop_button = QPushButton('Стоп')

        self.stop_button.setEnabled(False)  # при запуске стоп не активна

        layout = QHBoxLayout()  # две кнопки рядом в горизонтальной раскладке
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)
