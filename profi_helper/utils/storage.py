"""Хранилище заявок."""


class Storage():
    """Создаёт множество для хранения элементов.

    is_new - метод для проверки есть ли элемент во множестве.
    """
    def __init__(self):
        self.seen_orders = set()

    def is_new(self, order_id: str):
        """Проверяет, есть ли переданный элемент в хранилище."""
        if order_id not in self.seen_orders:
            self.seen_orders.add(order_id)
            return True
        return False

    def debug_print(self):
        print('Текущее хранилище:', self.seen_orders)
