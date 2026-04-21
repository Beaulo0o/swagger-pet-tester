# Swagger Pet Tester

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.0-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Requests](https://img.shields.io/badge/Requests-2.31-20232A?style=for-the-badge&logo=python&logoColor=white)](https://requests.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

[ О проекте](#-о-проекте) •
[ Цели](#-цели-проекта) •
[ Быстрый старт](#-быстрый-старт) •
[ Тесты](#-тестовые-сценарии) •
[ Стек](#-стек-технологий) •
[ Структура](#-структура-проекта) •
[ CI/CD](#-cicd) •
[ Проблемы](#-известные-проблемы)

---

##  О проекте

Проект представляет собой набор автотестов для API Petstore, написанных на Python с использованием современных инструментов тестирования.  
Тесты запускаются на локальном Docker-контейнере с Petstore API (v3).

---

##  Цели проекта

- Отработка подходов к автоматизации API-тестирования
- Практика работы с REST API (Petstore Swagger)
- Построение поддерживаемой структуры автотестов
- Настройка CI/CD с GitHub Actions

---

##  Стек технологий

| Компонент           | Технология                          |
|---------------------|-------------------------------------|
| Язык                | Python 3.12                        |
| Тестовый фреймворк  | Pytest 8.0                          |
| HTTP-клиент         | Requests 2.31                       |
| Генерация данных    | Faker 22.0                          |
| Валидация данных    | Pydantic 2.5                        |
| Отчёты              | Allure Pytest + Pytest HTML         |
| CI/CD               | GitHub Actions                      |
| Линтер              | Flake8, Black                       |
| API                 | Petstore Swagger (Docker)           |

---

## Структура проекта

 ```text
swagger-pet-tester/
├── .github/workflows/   # CI/CD конфигурация
├── api/                 # API слой (клиенты)
│   ├── client.py        # Базовый HTTP-клиент
│   ├── pet_api.py       # Методы для Pet
│   ├── store_api.py     # Методы для Store
│   └── user_api.py      # Методы для User
├── config/              # Конфигурация
│   └── settings.py      # URL, таймауты, настройки
├── models/              # Pydantic модели данных
│   ├── pet.py           # Pet, Category, Tag
│   ├── order.py         # Order
│   ├── user.py          # User
│   └── api_response.py  # ApiResponse
├── tests/               # Тесты
│   ├── conftest.py      # Фикстуры
│   ├── test_pet.py      # Тесты Pet API
│   ├── test_store.py    # Тесты Store API
│   └── test_user.py     # Тесты User API (пропущены)
├── utils/               # Утилиты
│   ├── generators.py    # Генерация тестовых данных
│   ├── assertions.py    # Кастомные ассерты
│   ├── logger.py        # Настройка логирования
│   └── constants.py     # Константы
├── data/                # Тестовые данные (JSON)
├── reports/             # Отчёты (создаются при запуске)
├── .env.example         # Пример переменных окружения
├── .gitignore
├── Makefile
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── README.md
 ```

---

##  Быстрый старт

 1. Клонирование репозитория

 ```bash
git clone https://github.com/your-username/swagger-pet-tester.git
cd swagger-pet-tester
 ```

 2. Установка зависимостей

 ```bash
# Через Makefile
make install

# Или вручную
pip install -r requirements.txt
 ```

 3. Запуск Petstore API через Docker

 ```bash
docker run -d -p 8080:8080 swaggerapi/petstore3:latest
 ```

Проверь, что API работает:
- Открой браузер: `http://localhost:8080/api/v3/pet/1`
- Должен прийти JSON с питомцем

 4. Настройка окружения

Скопируй пример конфига:

 ```bash
cp .env.example .env
 ```

Отредактируй `.env` при необходимости (по умолчанию всё уже настроено).

 5. Запуск тестов

 ```bash
# Все тесты (User пропущены)
make test

# Только Pet API
make test-pet

# Только Store API
make test-store

# Smoke тесты
make test-smoke
 ```

---

## Тестовые сценарии

 Pet API

- Создание питомца (позитивные и негативные сценарии)
- Получение питомца по ID
- Обновление питомца
- Удаление питомца
- Поиск по статусу

 Store API

- Размещение заказа
- Получение заказа по ID
- Удаление заказа
- Получение инвентаризации

 User API

- Пропущены из-за неработоспособности в Docker-образе (500 ошибка)

---

##  Команды Makefile

| Команда               | Описание                          |
|-----------------------|-----------------------------------|
| `make install`        | Установка зависимостей            |
| `make test`           | Запуск всех тестов                |
| `make test-smoke`     | Запуск smoke тестов               |
| `make test-pet`       | Тесты Pet API                     |
| `make test-store`     | Тесты Store API                   |
| `make lint`           | Проверка стиля кода               |
| `make format`         | Автоформатирование кода           |
| `make clean`          | Очистка временных файлов          |
| `make report`         | Allure отчёт                      |
| `make ci`             | Запуск как в CI (линтер + тесты)  |

---

##  CI/CD

Проект настроен на автоматический запуск тестов через GitHub Actions:

- **Push** в `main`/`master`/`develop`
- **Pull Request** в `main`/`master`
- **Ручной запуск** через `workflow_dispatch`

Что происходит в CI:

1. Установка Python (3.12)
2. Установка зависимостей
3. Линтинг (flake8)
4. Проверка форматирования (black)
5. Запуск всех тестов
6. Загрузка артефактов (результаты тестов, Allure отчёты)

---

##  Известные проблемы

- **User API** в Docker-образе `swaggerapi/petstore3:latest` возвращает 500 ошибку. Тесты для User эндпоинтов временно пропущены.
- **Store API** создаёт заказы даже с несуществующим `petId` (особенность API, не ошибка тестов).
- **Pet API** принимает любые значения `status` (нет валидации).

---

##  Пример использования

 ```python
from api import APIClient, PetAPI
from models import Pet
from utils import generate_pet_data

client = APIClient()
pet_api = PetAPI(client)

pet_data = generate_pet_data()
response = pet_api.create_pet(pet_data)
pet = Pet.from_dict(response.json())

print(f"Создан питомец: {pet.name} (ID: {pet.id})")

pet_api.delete_pet(pet.id)
client.close()
 ```
