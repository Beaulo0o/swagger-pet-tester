"""
Фикстуры для pytest
"""
import pytest
from faker import Faker
from typing import Dict, Any, Generator

from api.client import APIClient
from api.pet_api import PetAPI
from api.store_api import StoreAPI
from api.user_api import UserAPI
from models import Pet, Category, Tag, PetStatus, Order, OrderStatus, User
from utils.generators import generate_pet_data, generate_order_data, generate_user_data

# Инициализация Faker для русских/английских данных
fake = Faker()
Faker.seed(42)  # Для воспроизводимости


# ========== Клиенты ==========

@pytest.fixture(scope="session")
def api_client() -> Generator[APIClient, None, None]:
    """
    Базовый API клиент (один на всю сессию)
    """
    client = APIClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def pet_api(api_client: APIClient) -> PetAPI:
    """API для работы с питомцами"""
    return PetAPI(api_client)


@pytest.fixture(scope="session")
def store_api(api_client: APIClient) -> StoreAPI:
    """API для работы с магазином"""
    return StoreAPI(api_client)


@pytest.fixture(scope="session")
def user_api(api_client: APIClient) -> UserAPI:
    """API для работы с пользователями"""
    return UserAPI(api_client)


# ========== Генераторы данных ==========

@pytest.fixture
def random_pet_data() -> Dict[str, Any]:
    """Генерирует случайные данные для питомца"""
    return generate_pet_data()


@pytest.fixture
def random_order_data() -> Dict[str, Any]:
    """Генерирует случайные данные для заказа"""
    return generate_order_data()


@pytest.fixture
def random_user_data() -> Dict[str, Any]:
    """Генерирует случайные данные для пользователя"""
    return generate_user_data()


# ========== Созданные объекты с автоочисткой ==========

@pytest.fixture
def created_pet(pet_api: PetAPI, random_pet_data: Dict[str, Any]) -> Generator[Pet, None, None]:
    """
    Создаёт питомца перед тестом и удаляет после теста
    """
    # Создаём питомца
    response = pet_api.create_pet(random_pet_data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"

    pet = Pet.from_dict(response.json())
    yield pet

    # Удаляем после теста
    delete_response = pet_api.delete_pet(pet.id)
    # 200 - успешно, 404 - уже удалён (тоже норм)
    assert delete_response.status_code in [200, 404], f"Failed to delete pet {pet.id}"


@pytest.fixture
def created_order(store_api: StoreAPI, random_order_data: Dict[str, Any]) -> Generator[Order, None, None]:
    """
    Создаёт заказ перед тестом и удаляет после теста
    """
    # Создаём заказ
    response = store_api.place_order(random_order_data)
    assert response.status_code == 200, f"Failed to create order: {response.text}"

    order = Order.from_dict(response.json())
    yield order

    # Удаляем после теста (если есть id)
    if order.id:
        delete_response = store_api.delete_order(order.id)
        assert delete_response.status_code in [200, 404], f"Failed to delete order {order.id}"


@pytest.fixture
def created_user(user_api: UserAPI, random_user_data: Dict[str, Any]) -> Generator[User, None, None]:
    """
    Создаёт пользователя перед тестом и удаляет после теста
    """
    response = user_api.create_user(random_user_data)
    assert response.status_code == 200, f"Failed to create user: {response.text}"

    user = User.from_dict(random_user_data)
    yield user

    delete_response = user_api.delete_user(user.username)
    assert delete_response.status_code in [200, 404]

# ========== Вспомогательные фикстуры ==========

@pytest.fixture
def existing_pet_id(pet_api: PetAPI) -> Generator[int, None, None]:
    """
    Создаёт питомца и возвращает его ID (без модели)
    """
    pet_data = generate_pet_data()
    response = pet_api.create_pet(pet_data)
    assert response.status_code == 200

    pet_id = response.json()["id"]
    yield pet_id

    pet_api.delete_pet(pet_id)


@pytest.fixture
def auth_headers() -> Dict[str, str]:
    """
    Заголовки для авторизации (если понадобится API ключ)
    """
    # В Petstore API ключ не обязателен, но можно добавить
    return {
        "api_key": "special-key"  # Тестовый ключ из документации
    }


# ========== Параметризация статусов ==========

def pytest_generate_tests(metafunc):
    """
    Динамическая параметризация для тестов
    """
    if "pet_status" in metafunc.fixturenames:
        metafunc.parametrize(
            "pet_status",
            ["available", "pending", "sold"],
            ids=["available", "pending", "sold"]
        )