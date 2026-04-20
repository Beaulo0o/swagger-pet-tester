"""
API методы для работы с питомцами (Pet)
"""
from typing import Dict, Any, List, Optional
from api.client import APIClient


class PetAPI:
    """Класс с методами для эндпоинтов /pet"""

    def __init__(self, client: APIClient):
        self.client = client

    def create_pet(self, pet_data: Dict[str, Any]):
        """
        Создать нового питомца
        POST /pet

        Args:
            pet_data: словарь с данными питомца

        Returns:
            Response объект
        """
        return self.client.post("/pet", json=pet_data)

    def get_pet(self, pet_id: int):
        """
        Получить питомца по ID
        GET /pet/{petId}

        Args:
            pet_id: ID питомца

        Returns:
            Response объект
        """
        return self.client.get(f"/pet/{pet_id}")

    def update_pet(self, pet_data: Dict[str, Any]):
        """
        Обновить существующего питомца (полное обновление)
        PUT /pet

        Args:
            pet_data: словарь с обновлёнными данными питомца

        Returns:
            Response объект
        """
        return self.client.put("/pet", json=pet_data)

    def delete_pet(self, pet_id: int, api_key: Optional[str] = None):
        """
        Удалить питомца
        DELETE /pet/{petId}

        Args:
            pet_id: ID питомца
            api_key: опциональный API ключ (для авторизации)

        Returns:
            Response объект
        """
        headers = {}
        if api_key:
            headers["api_key"] = api_key
        return self.client.delete(f"/pet/{pet_id}", headers=headers)

    def find_by_status(self, status: str):
        """
        Найти питомцев по статусу
        GET /pet/findByStatus

        Args:
            status: статус (available, pending, sold)

        Returns:
            Response объект
        """
        return self.client.get("/pet/findByStatus", params={"status": status})

    def find_by_statuses(self, statuses: List[str]):
        """
        Найти питомцев по нескольким статусам
        GET /pet/findByStatus?status=available&status=pending

        Args:
            statuses: список статусов

        Returns:
            Response объект
        """
        params = [("status", status) for status in statuses]
        return self.client.get("/pet/findByStatus", params=params)

    def upload_image(self, pet_id: int, file_path: str, additional_metadata: Optional[str] = None):
        """
        Загрузить изображение для питомца
        POST /pet/{petId}/uploadImage

        Args:
            pet_id: ID питомца
            file_path: путь к файлу изображения
            additional_metadata: дополнительная метаинформация

        Returns:
            Response объект
        """
        files = {"file": open(file_path, "rb")}
        data = {}
        if additional_metadata:
            data["additionalMetadata"] = additional_metadata

        try:
            response = self.client.post(f"/pet/{pet_id}/uploadImage", files=files, data=data)
            return response
        finally:
            files["file"].close()