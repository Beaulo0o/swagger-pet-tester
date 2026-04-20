"""
Генераторы тестовых данных с использованием Faker
"""
import random
from typing import Dict, Any, List, Optional
from faker import Faker
from datetime import datetime, timedelta

# Инициализация Faker
fake = Faker()
Faker.seed(42)

# Константы
PET_STATUSES = ["available", "pending", "sold"]
ORDER_STATUSES = ["placed", "approved", "delivered"]
PET_CATEGORIES = [
    {"id": 1, "name": "Dogs"},
    {"id": 2, "name": "Cats"},
    {"id": 3, "name": "Birds"},
    {"id": 4, "name": "Fish"},
    {"id": 5, "name": "Reptiles"},
    {"id": 6, "name": "Hamsters"},
]
PET_TAGS = [
    {"id": 1, "name": "friendly"},
    {"id": 2, "name": "vaccinated"},
    {"id": 3, "name": "purebred"},
    {"id": 4, "name": "exotic"},
    {"id": 5, "name": "senior"},
    {"id": 6, "name": "puppy"},
    {"id": 7, "name": "kitten"},
]


def generate_unique_id() -> int:
    """Генерирует уникальный ID на основе timestamp и случайного числа"""
    import time
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1, 9999)
    return timestamp + random_suffix


def generate_category(category_id: Optional[int] = None) -> Dict[str, Any]:
    """Генерирует случайную категорию для питомца"""
    if category_id is None:
        category = random.choice(PET_CATEGORIES)
    else:
        category = next((c for c in PET_CATEGORIES if c["id"] == category_id), PET_CATEGORIES[0])

    return {
        "id": category["id"],
        "name": category["name"]
    }


def generate_tags(num_tags: int = 2) -> List[Dict[str, Any]]:
    """Генерирует список случайных тегов для питомца"""
    selected_tags = random.sample(PET_TAGS, min(num_tags, len(PET_TAGS)))
    return [{"id": tag["id"], "name": tag["name"]} for tag in selected_tags]


def generate_pet_data(
        pet_id: Optional[int] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        with_category: bool = True,
        with_tags: bool = True
) -> Dict[str, Any]:
    """Генерирует случайные данные для питомца"""
    pet_data = {
        "id": pet_id if pet_id is not None else generate_unique_id(),
        "name": name if name is not None else fake.first_name() + " " + random.choice(
            ["Max", "Bella", "Charlie", "Lucy", "Cooper"]),
        "photoUrls": [fake.image_url() for _ in range(random.randint(1, 3))],
        "status": status if status is not None else random.choice(PET_STATUSES),
    }

    if with_category:
        pet_data["category"] = generate_category()

    if with_tags:
        pet_data["tags"] = generate_tags(num_tags=random.randint(1, 3))

    return pet_data


def generate_order_data(
        order_id: Optional[int] = None,
        pet_id: Optional[int] = None,
        quantity: Optional[int] = None,
        status: Optional[str] = None,
        complete: Optional[bool] = None
) -> Dict[str, Any]:
    """Генерирует случайные данные для заказа"""
    order_data = {
        "id": order_id if order_id is not None else generate_unique_id(),
        "petId": pet_id if pet_id is not None else generate_unique_id(),
        "quantity": quantity if quantity is not None else random.randint(1, 10),
        "shipDate": (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat(),
        "status": status if status is not None else random.choice(ORDER_STATUSES),
        "complete": complete if complete is not None else random.choice([True, False]),
    }

    return order_data


def generate_user_data(
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        user_status: int = 1
) -> Dict[str, Any]:
    """
    Генерирует полные данные для пользователя (все поля обязательны)
    """
    user_data = {
        "id": generate_unique_id(),
        "username": username if username is not None else fake.user_name(),
        "firstName": first_name if first_name is not None else fake.first_name(),
        "lastName": last_name if last_name is not None else fake.last_name(),
        "email": email if email is not None else fake.email(),
        "password": password if password is not None else fake.password(length=8, special_chars=False, digits=True),
        "phone": phone if phone is not None else fake.phone_number()[:15],
        "userStatus": user_status,
    }

    return user_data


def generate_multiple_pets(count: int = 5) -> List[Dict[str, Any]]:
    """Генерирует список из нескольких питомцев"""
    return [generate_pet_data() for _ in range(count)]


def generate_multiple_users(count: int = 3) -> List[Dict[str, Any]]:
    """Генерирует список из нескольких пользователей"""
    return [generate_user_data() for _ in range(count)]


if __name__ == "__main__":
    print("=" * 50)
    print("Пример генерации данных:")
    print("=" * 50)

    print("\n1. Питомец:")
    pet = generate_pet_data()
    print(f"   {pet}")

    print("\n2. Заказ:")
    order = generate_order_data(pet_id=pet["id"])
    print(f"   {order}")

    print("\n3. Пользователь:")
    user = generate_user_data()
    print(f"   {user}")