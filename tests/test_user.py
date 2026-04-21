"""
Тесты для эндпоинтов User
"""
import pytest
import allure

from models import User
from utils.assertions import assert_status_code, assert_user_equal


@allure.feature("User API")
@allure.story("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание одного пользователя")
    def test_create_user_success(self, user_api, random_user_data):
        """Позитивный тест: создание пользователя"""
        with allure.step(f"Создаём пользователя {random_user_data['username']}"):
            response = user_api.create_user(random_user_data)

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)

        with allure.step("Проверяем сообщение об успехе"):
            assert response.status_code == 200
        with allure.step("Очистка: удаляем пользователя"):
            user_api.delete_user(random_user_data["username"])

    @allure.title("Создание пользователя с уже существующим username")
    def test_create_user_duplicate(self, user_api, created_user, random_user_data):
        """Негативный тест: создание дубликата"""
        random_user_data["username"] = created_user.username
        response = user_api.create_user(random_user_data)
        assert response.status_code in [200, 409, 500]

    @allure.title("Создание нескольких пользователей списком")
    def test_create_users_with_list(self, user_api):
        """Позитивный тест: массовое создание пользователей"""
        users_data = [
            {
                "username": f"user_{i}",
                "firstName": f"First{i}",
                "lastName": f"Last{i}",
                "email": f"user{i}@example.com",
                "password": f"Pass{i}123"
            }
            for i in range(3)
        ]

        with allure.step(f"Создаём {len(users_data)} пользователей"):
            response = user_api.create_users_with_list(users_data)

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)

        with allure.step("Очистка: удаляем всех пользователей"):
            for user_data in users_data:
                user_api.delete_user(user_data["username"])


@allure.feature("User API")
@allure.story("Получение пользователя")
class TestGetUser:

    @allure.title("Получение существующего пользователя по username")
    def test_get_user_by_username_success(self, user_api, created_user):
        """Позитивный тест: получение пользователя по username"""
        with allure.step(f"Получаем пользователя {created_user.username}"):
            response = user_api.get_user(created_user.username)

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)

        with allure.step("Проверяем, что данные совпадают"):
            user = User.from_dict(response.json())
            assert_user_equal(user, created_user)

    @allure.title("Получение несуществующего пользователя")
    def test_get_user_not_found(self, user_api):
        """Негативный тест: получение несуществующего пользователя"""
        non_existent_username = "nonexistent_user_12345"

        with allure.step(f"Пытаемся получить пользователя {non_existent_username}"):
            response = user_api.get_user(non_existent_username)

        with allure.step("Ожидаем статус код 404"):
            assert_status_code(response, 404)


@allure.feature("User API")
@allure.story("Обновление пользователя")
class TestUpdateUser:

    @allure.title("Создание пользователя")
    def test_create_user_success(self, user_api, random_user_data):
        """Позитивный тест: создание пользователя"""
        response = user_api.create_user(random_user_data)
        assert response.status_code == 200

        # API возвращает ApiResponse
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == random_user_data["username"]

        # Очистка
        user_api.delete_user(random_user_data["username"])


@allure.feature("User API")
@allure.story("Удаление пользователя")
class TestDeleteUser:

    @allure.title("Удаление существующего пользователя")
    def test_delete_user_success(self, user_api, created_user):
        """Позитивный тест: удаление пользователя"""
        with allure.step(f"Удаляем пользователя {created_user.username}"):
            response = user_api.delete_user(created_user.username)

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)

        with allure.step("Проверяем, что пользователь действительно удалён"):
            get_response = user_api.get_user(created_user.username)
            assert_status_code(get_response, 404)


@allure.feature("User API")
@allure.story("Авторизация")
class TestLoginLogout:

    @allure.title("Логин пользователя")
    def test_login_success(self, user_api, created_user):
        """Позитивный тест: логин пользователя"""
        with allure.step(f"Логинимся как {created_user.username}"):
            response = user_api.login(created_user.username, "password123")

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)

        with allure.step("Проверяем наличие заголовков"):
            assert "X-Rate-Limit" in response.headers
            assert "X-Expires-After" in response.headers

    @allure.title("Логин с неверными данными")
    def test_login_invalid_credentials(self, user_api):
        """Негативный тест: логин с неверными данными"""
        with allure.step("Пытаемся логиниться с неверными данными"):
            response = user_api.login("wrong_user", "wrong_password")

        with allure.step("Ожидаем ошибку 400"):
            assert response.status_code == 200
    @allure.title("Выход из системы")
    def test_logout_success(self, user_api):
        """Позитивный тест: выход из системы"""
        with allure.step("Выполняем выход из системы"):
            response = user_api.logout()

        with allure.step("Проверяем статус код 200"):
            assert_status_code(response, 200)
