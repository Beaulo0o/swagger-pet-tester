"""
Константы для тестов
"""

# API Endpoints
class Endpoints:
    PET = "/pet"
    PET_BY_ID = "/pet/{pet_id}"
    PET_FIND_BY_STATUS = "/pet/findByStatus"
    PET_UPLOAD_IMAGE = "/pet/{pet_id}/uploadImage"

    STORE_ORDER = "/store/order"
    STORE_ORDER_BY_ID = "/store/order/{order_id}"
    STORE_INVENTORY = "/store/inventory"

    USER = "/user"
    USER_BY_USERNAME = "/user/{username}"
    USER_LOGIN = "/user/login"
    USER_LOGOUT = "/user/logout"
    USER_CREATE_WITH_LIST = "/user/createWithList"


# HTTP Status Codes
class HttpStatus:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


# Test Data Constants
class TestData:
    # Предопределённые питомцы
    PET_1 = {
        "id": 1001,
        "name": "Buddy",
        "status": "available"
    }

    PET_2 = {
        "id": 1002,
        "name": "Max",
        "status": "pending"
    }

    # Предопределённые пользователи
    USER_1 = {
        "username": "testuser1",
        "password": "TestPass123",
        "email": "test1@example.com"
    }

    USER_2 = {
        "username": "testuser2",
        "password": "TestPass456",
        "email": "test2@example.com"
    }


# Заголовки по умолчанию
class Headers:
    CONTENT_TYPE_JSON = {"Content-Type": "application/json"}
    CONTENT_TYPE_FORM = {"Content-Type": "application/x-www-form-urlencoded"}
    ACCEPT_JSON = {"Accept": "application/json"}

    # API ключ для Petstore
    API_KEY = {"api_key": "special-key"}