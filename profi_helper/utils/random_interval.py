"""Случайное значение интервала автообновления страницы."""
import random


def get_random_interval(min_ms=5000, max_ms=10000) -> int:
    """Возвращает случайный интервал в миллисекундах
    между min_ms и max_ms (включительно).
    """
    return random.randint(min_ms, max_ms)
