"""
API методы для работы с магазином (Store) - заказы
"""
from typing import Dict, Any
from api.client import APIClient


class StoreAPI:
    """Класс с методами для эндпоинтов /store"""

    def __init__(self, client: APIClient):
        self.client = client

    def place_order(self, order_data: Dict[str, Any]):
        """
        Разместить заказ на питомца
        POST /store/order

        Args:
            order_data: словарь с данными заказа

        Returns:
            Response объект
        """
        return self.client.post("/store/order", json=order_data)

    def get_order(self, order_id: int):
        """
        Получить заказ по ID
        GET /store/order/{orderId}

        Args:
            order_id: ID заказа

        Returns:
            Response объект
        """
        return self.client.get(f"/store/order/{order_id}")

    def delete_order(self, order_id: int):
        """
        Удалить заказ
        DELETE /store/order/{orderId}

        Args:
            order_id: ID заказа

        Returns:
            Response объект
        """
        return self.client.delete(f"/store/order/{order_id}")

    def get_inventory(self):
        """
        Получить инвентаризацию магазина по статусам
        GET /store/inventory

        Returns:
            Response объект (словарь: {"available": 10, "pending": 5, "sold": 3})
        """
        return self.client.get("/store/inventory")