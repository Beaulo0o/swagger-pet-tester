"""
API методы для работы с пользователями (User)
"""
from typing import Dict, Any, List
from api.client import APIClient


class UserAPI:
    """Класс с методами для эндпоинтов /user"""

    def __init__(self, client: APIClient):
        self.client = client

    def create_user(self, user_data: Dict[str, Any]):
        """
        Создать одного пользователя
        POST /user

        Args:
            user_data: словарь с данными пользователя

        Returns:
            Response объект
        """
        return self.client.post("/user", json=user_data)

    def create_users_with_list(self, users_list: List[Dict[str, Any]]):
        """
        Создать нескольких пользователей (списком)
        POST /user/createWithList

        Args:
            users_list: список словарей с данными пользователей

        Returns:
            Response объект
        """
        return self.client.post("/user/createWithList", json=users_list)

    def get_user(self, username: str):
        """
        Получить пользователя по имени
        GET /user/{username}

        Args:
            username: имя пользователя

        Returns:
            Response объект
        """
        return self.client.get(f"/user/{username}")

    def update_user(self, username: str, user_data: Dict[str, Any]):
        """
        Обновить пользователя
        PUT /user/{username}

        Args:
            username: текущее имя пользователя
            user_data: обновлённые данные

        Returns:
            Response объект
        """
        return self.client.put(f"/user/{username}", json=user_data)

    def delete_user(self, username: str):
        """
        Удалить пользователя
        DELETE /user/{username}

        Args:
            username: имя пользователя

        Returns:
            Response объект
        """
        return self.client.delete(f"/user/{username}")

    def login(self, username: str, password: str):
        """
        Логин пользователя
        GET /user/login

        Args:
            username: имя пользователя
            password: пароль

        Returns:
            Response объект (с заголовком X-Rate-Limit, X-Expires-After)
        """
        return self.client.get("/user/login", params={"username": username, "password": password})

    def logout(self):
        """
        Выйти из системы
        GET /user/logout

        Returns:
            Response объект
        """
        return self.client.get("/user/logout")