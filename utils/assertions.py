"""
Кастомные ассерты для тестов
"""
from typing import Dict, Any, List, Optional
from requests import Response

from models import Pet, Order, User


def assert_status_code(response: Response, expected_status: int, message: Optional[str] = None):
    """
    Проверка статус кода с понятным сообщением

    Args:
        response: Response объект
        expected_status: ожидаемый статус код
        message: дополнительное сообщение
    """
    error_msg = message or f"Expected status {expected_status}, got {response.status_code}"
    if response.status_code != expected_status:
        # Добавляем тело ответа для диагностики
        try:
            error_msg += f"\nResponse body: {response.text[:500]}"
        except:
            pass
        raise AssertionError(error_msg)


def assert_pet_equal(pet1: Pet, pet2: Pet, check_id: bool = True):
    """
    Проверка равенства двух питомцев

    Args:
        pet1: первый питомец
        pet2: второй питомец
        check_id: проверять ли ID
    """
    if check_id:
        assert pet1.id == pet2.id, f"Pet IDs don't match: {pet1.id} vs {pet2.id}"

    assert pet1.name == pet2.name, f"Pet names don't match: {pet1.name} vs {pet2.name}"

    if pet1.status and pet2.status:
        assert pet1.status == pet2.status, f"Pet statuses don't match: {pet1.status} vs {pet2.status}"

    if pet1.category and pet2.category:
        assert pet1.category.id == pet2.category.id, f"Category IDs don't match"
        assert pet1.category.name == pet2.category.name, f"Category names don't match"

    if pet1.tags and pet2.tags:
        assert len(pet1.tags) == len(pet2.tags), f"Tags count mismatch: {len(pet1.tags)} vs {len(pet2.tags)}"


def assert_order_equal(order1: Order, order2: Order, check_id: bool = True):
    """
    Проверка равенства двух заказов

    Args:
        order1: первый заказ
        order2: второй заказ
        check_id: проверять ли ID
    """
    if check_id:
        assert order1.id == order2.id, f"Order IDs don't match: {order1.id} vs {order2.id}"

    assert order1.petId == order2.petId, f"Pet IDs don't match: {order1.petId} vs {order2.petId}"
    assert order1.quantity == order2.quantity, f"Quantities don't match: {order1.quantity} vs {order2.quantity}"

    if order1.status and order2.status:
        assert order1.status == order2.status, f"Order statuses don't match: {order1.status} vs {order2.status}"

    assert order1.complete == order2.complete, f"Complete flags don't match: {order1.complete} vs {order2.complete}"


def assert_user_equal(user1: User, user2: User, check_id: bool = True, check_password: bool = False):
    """
    Проверка равенства двух пользователей

    Args:
        user1: первый пользователь
        user2: второй пользователь
        check_id: проверять ли ID
        check_password: проверять ли пароль (обычно не возвращается в ответе)
    """
    if check_id and user1.id and user2.id:
        assert user1.id == user2.id, f"User IDs don't match: {user1.id} vs {user2.id}"

    assert user1.username == user2.username, f"Usernames don't match: {user1.username} vs {user2.username}"

    if user1.firstName and user2.firstName:
        assert user1.firstName == user2.firstName, f"First names don't match"

    if user1.lastName and user2.lastName:
        assert user1.lastName == user2.lastName, f"Last names don't match"

    if user1.email and user2.email:
        assert user1.email == user2.email, f"Emails don't match: {user1.email} vs {user2.email}"

    if check_password and user1.password and user2.password:
        assert user1.password == user2.password, f"Passwords don't match"


def assert_pet_in_list(pet: Pet, pet_list: List[Dict[str, Any]]):
    """
    Проверяет, что питомец присутствует в списке

    Args:
        pet: питомец для поиска
        pet_list: список словарей с питомцами
    """
    found = False
    for item in pet_list:
        if item.get("id") == pet.id:
            found = True
            assert item.get("name") == pet.name, f"Name mismatch: {item.get('name')} vs {pet.name}"
            break

    assert found, f"Pet with ID {pet.id} not found in list"


def assert_response_has_fields(response: Response, required_fields: List[str]):
    """
    Проверяет, что ответ содержит все обязательные поля

    Args:
        response: Response объект
        required_fields: список обязательных полей
    """
    try:
        data = response.json()
    except:
        raise AssertionError(f"Response is not JSON: {response.text[:200]}")

    missing_fields = [field for field in required_fields if field not in data]
    assert not missing_fields, f"Missing fields in response: {missing_fields}"


def assert_response_has_headers(response: Response, required_headers: List[str]):
    """
    Проверяет, что ответ содержит все обязательные заголовки

    Args:
        response: Response объект
        required_headers: список обязательных заголовков
    """
    missing_headers = [header for header in required_headers if header not in response.headers]
    assert not missing_headers, f"Missing headers in response: {missing_headers}"


def assert_error_message(response: Response, expected_message: str):
    """
    Проверяет сообщение об ошибке в ответе

    Args:
        response: Response объект
        expected_message: ожидаемое сообщение
    """
    try:
        data = response.json()
        actual_message = data.get("message", str(data))
    except:
        actual_message = response.text

    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in '{actual_message}'"


def assert_not_empty(data: Any, field_name: str = "data"):
    """
    Проверяет, что данные не пустые

    Args:
        data: проверяемые данные
        field_name: имя поля для сообщения об ошибке
    """
    if isinstance(data, (dict, list)):
        assert len(data) > 0, f"{field_name} is empty"
    else:
        assert data is not None, f"{field_name} is None"
        if isinstance(data, str):
            assert data.strip(), f"{field_name} is empty string"


def assert_valid_uuid(uuid_string: str, field_name: str = "uuid"):
    """
    Проверяет, что строка является валидным UUID

    Args:
        uuid_string: проверяемая строка
        field_name: имя поля для сообщения об ошибке
    """
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    assert re.match(uuid_pattern, uuid_string, re.IGNORECASE), f"{field_name} is not a valid UUID: {uuid_string}"