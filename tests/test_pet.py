import pytest
import allure
from models import Pet, PetStatus, ApiResponse


@allure.feature("Pet API")
class TestCreatePet:
    
    @allure.title("Создание питомца с валидными данными")
    def test_create_pet_valid(self, pet_api, random_pet_data):
        response = pet_api.create_pet(random_pet_data)
        assert response.status_code == 200
        
        pet = Pet.from_dict(response.json())
        assert pet.name == random_pet_data["name"]
        assert pet.photoUrls == random_pet_data["photoUrls"]
        
        pet_api.delete_pet(pet.id)
    
    @allure.title("Создание питомца без обязательных полей")
    @pytest.mark.parametrize("missing_field,base_data", [
        ("name", {"photoUrls": ["url1"]}),
    ])
    def test_create_pet_missing_required_fields(self, pet_api, missing_field, base_data):
        response = pet_api.create_pet(base_data)
        # API возвращает 500 при отсутствии обязательных полей
        assert response.status_code == 500
    
    @allure.title("Создание питомца с любым статусом")
    def test_create_pet_any_status(self, pet_api, random_pet_data):
        random_pet_data["status"] = "invalid_status_123"
        response = pet_api.create_pet(random_pet_data)
        # API принимает любой статус
        assert response.status_code == 200
        pet = Pet.from_dict(response.json())
        assert pet.status == "invalid_status_123"


@allure.feature("Pet API")
class TestGetPet:
    
    @allure.title("Получение существующего питомца")
    def test_get_pet_by_id_success(self, pet_api, created_pet):
        response = pet_api.get_pet(created_pet.id)
        assert response.status_code == 200
        pet = Pet.from_dict(response.json())
        assert pet.id == created_pet.id
        assert pet.name == created_pet.name
    
    @allure.title("Получение несуществующего питомца")
    def test_get_pet_not_found(self, pet_api):
        response = pet_api.get_pet(999999999)
        assert response.status_code == 404
    
    @allure.title("Получение питомца с невалидным ID")
    @pytest.mark.parametrize("invalid_id", [-1, 0, "abc", None])
    def test_get_pet_invalid_id(self, pet_api, invalid_id):
        response = pet_api.get_pet(invalid_id)
        # Для строк и None возвращает 400
        if isinstance(invalid_id, str) or invalid_id is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 404


@allure.feature("Pet API")
class TestUpdatePet:
    
    @allure.title("Полное обновление питомца")
    def test_update_pet_full(self, pet_api, created_pet, random_pet_data):
        random_pet_data["id"] = created_pet.id
        response = pet_api.update_pet(random_pet_data)
        assert response.status_code == 200
        updated_pet = Pet.from_dict(response.json())
        assert updated_pet.name == random_pet_data["name"]


@allure.feature("Pet API")
class TestDeletePet:
    
    @allure.title("Удаление существующего питомца")
    def test_delete_pet_success(self, pet_api, existing_pet_id):
        response = pet_api.delete_pet(existing_pet_id)
        assert response.status_code == 200
        
        get_response = pet_api.get_pet(existing_pet_id)
        assert get_response.status_code == 404
    
    @allure.title("Удаление несуществующего питомца")
    def test_delete_pet_not_found(self, pet_api):
        response = pet_api.delete_pet(999999999)
        assert response.status_code == 200


@allure.feature("Pet API")
class TestFindByStatus:
    
    @allure.title("Поиск питомцев по статусу")
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_by_status_success(self, pet_api, status):
        response = pet_api.find_by_status(status)
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
    
    @allure.title("Поиск с невалидным статусом")
    def test_find_by_invalid_status(self, pet_api):
        response = pet_api.find_by_status("invalid")
        assert response.status_code == 400
