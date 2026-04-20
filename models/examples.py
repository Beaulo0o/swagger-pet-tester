"""
Примеры использования моделей данных
Можно запустить для проверки: python -m models.examples
"""
from models import Pet, Category, Tag, PetStatus, Order, OrderStatus, User
from datetime import datetime, timedelta


def example_pet():
    """Пример работы с моделью Pet"""
    print("=" * 50)
    print("Пример: Pet")
    print("=" * 50)

    # Создание через конструктор
    pet = Pet(
        id=123,
        name="Rex",
        category=Category(id=1, name="Dogs"),
        photoUrls=["https://example.com/rex.jpg"],
        tags=[Tag(id=1, name="friendly")],
        status=PetStatus.AVAILABLE
    )

    print(f"Создан: {pet}")
    print(f"В словарь: {pet.to_dict()}")

    # Создание из словаря
    pet_dict = {
        "id": 456,
        "name": "Whiskers",
        "photoUrls": ["https://example.com/whiskers.jpg"],
        "status": "pending"
    }
    pet2 = Pet.from_dict(pet_dict)
    print(f"Из словаря: {pet2}")

    return pet


def example_order():
    """Пример работы с моделью Order"""
    print("\n" + "=" * 50)
    print("Пример: Order")
    print("=" * 50)

    order = Order(
        petId=123,
        quantity=2,
        shipDate=datetime.now() + timedelta(days=3),
        status=OrderStatus.PLACED,
        complete=False
    )

    print(f"Создан: {order}")
    print(f"В словарь: {order.to_dict()}")

    # Создание из словаря
    order_dict = {
        "id": 1001,
        "petId": 123,
        "quantity": 1,
        "status": "approved"
    }
    order2 = Order.from_dict(order_dict)
    print(f"Из словаря: {order2}")

    return order


def example_user():
    """Пример работы с моделью User"""
    print("\n" + "=" * 50)
    print("Пример: User")
    print("=" * 50)

    user = User(
        username="john_doe",
        firstName="John",
        lastName="Doe",
        email="john@example.com",
        password="Secret123",
        phone="+1234567890",
        userStatus=1
    )

    print(f"Создан: {user}")
    print(f"В словарь: {user.to_dict()}")

    # Создание из словаря
    user_dict = {
        "username": "jane_smith",
        "email": "jane@example.com",
        "password": "Pass456"
    }
    user2 = User.from_dict(user_dict)
    print(f"Из словаря: {user2}")

    return user


def test_validation():
    """Демонстрация валидации"""
    print("\n" + "=" * 50)
    print("Пример валидации")
    print("=" * 50)

    # Некорректное имя питомца
    try:
        pet = Pet(name="")  # Пустое имя
        print(f"Ошибка не возникла: {pet}")
    except ValueError as e:
        print(f"✅ Валидация сработала: {e}")

    # Некорректный статус
    try:
        pet = Pet(name="Test", status="invalid_status")  # Нет такого статуса
        print(f"Ошибка не возникла: {pet}")
    except ValueError as e:
        print(f"✅ Валидация сработала: {e}")

    # Некорректный username
    try:
        user = User(username="123invalid")  # Начинается с цифры
        print(f"Ошибка не возникла: {user}")
    except ValueError as e:
        print(f"✅ Валидация сработала: {e}")


if __name__ == "__main__":
    # Запуск примеров
    example_pet()
    example_order()
    example_user()
    test_validation()

    print("\n" + "=" * 50)
    print("Все примеры выполнены успешно!")
    print("=" * 50)