"""Система уведомления о новых заявках: звуковой сигнал и сообщение (если нужно)."""
import os
from PySide6.QtWidgets import QMessageBox
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl


class Notifier():
    """Оповещает о новой заявке звуковым сигналом и сообщением."""
    def __init__(self, parent=None):
        self.parent = parent
        # файл со звуком должен быть расположен в той же папке, что и этот файл
        # mp3 (или wav)
        sound_file = os.path.join(os.path.dirname(__file__), '2alert.wav')

        # создаём звуковой эффект
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(sound_file))
        self.sound.setVolume(0.8)  # громкость в диапазоне 0.0–1.0

    def sound_notify(self):
        """Включает звуковое уведомление о событии."""
        # if self.sound.isLoaded():
        #     self.sound.play()
        # else:
        #     print('Проблема со звуковым файлом - файл не загружен.')
        self.sound.play()

    def popup_notify(self, message: str):
        """Включает неблокирующее основную программу popup-окно с уведомлением."""
        self.msg = QMessageBox(self.parent)  # self.parent внутри главного окна
        self.msg.setWindowTitle('Новая заявка!')
        self.msg.setText(message)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()  # msg.exec() будет блокировать, пока не нажмут Ok
