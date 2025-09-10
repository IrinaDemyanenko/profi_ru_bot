"""Логирование, запись в файл."""
import logging
from pathlib import Path


LOG_DIR = Path('logs')  # папка logs появится рядом с файлом запуска, а не рядом с этим модулем
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'app.log'


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()  # вывод в консоль
    ]
)

# %(asctime)s — время записи лога
# %(levelname)s — уровень (INFO, ERROR и т. д.)
# %(name)s — имя логгера
# %(message)s — само сообщение

# создам логгер для моего бота
logger = logging.getLogger('profi_bot')


def get_logger():
    return logger
