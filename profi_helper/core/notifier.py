"""Система уведомления о новых заявках: звуковой сигнал и сообщение (если нужно)."""
import sys
import os
from PySide6.QtWidgets import QMessageBox
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl, QTimer


class Notifier():
    """Оповещает о новой заявке звуковым сигналом и сообщением."""
    def __init__(self, parent=None):
        self.parent = parent
        # файл со звуком должен быть расположен в той же папке, что и этот файл
        # mp3 (или wav)
        sound_file = self._resourсe_path('2alert.wav')

        # создаём звуковой эффект
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(sound_file))
        self.sound.setVolume(0.8)  # громкость в диапазоне 0.0–1.0

        # таймер для повторного воспроизведения звука
        self.timer = QTimer()
        self.timer.timeout.connect(self._play_sound)

    @staticmethod
    def _resourсe_path(filename: str):
        """Возвращает путь к ресурсу, работает и для .py, и для .exe."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        return os.path.join(os.path.dirname(__file__), filename)

    def _play_sound(self):
        """Звуковое уведомление о событии."""
        if self.sound.isLoaded():
            self.sound.play()
        else:
            print('Проблема со звуковым файлом - файл не загружен.')

    def sound_notify(self):
        """Включает звуковое уведомление о событии и повторяет его каждую
        1 секунду.
        """
        self._play_sound()
        self.timer.start(1000)  # повтор каждые 1000 мс (1 секундe)

    def stop_sound(self):
        """Останавливает повторение звука."""
        self.timer.stop()

    def popup_notify(self, message: str):
        """Включает неблокирующее основную программу popup-окно с уведомлением."""
        self.msg = QMessageBox(self.parent)  # self.parent внутри главного окна
        self.msg.setWindowTitle('Новая заявка!')
        self.msg.setText(message)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()  # msg.exec() будет блокировать, пока не нажмут Ok
