"""
Базовый HTTP-клиент для работы с API
"""
import requests
import logging
from typing import Optional, Dict, Any

from config.settings import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для выполнения HTTP-запросов"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(config.DEFAULT_HEADERS)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.timeout = (config.CONNECTION_TIMEOUT, config.READ_TIMEOUT)

    def _log_request(self, method: str, url: str, **kwargs):
        """Логирование запроса"""
        if config.LOG_REQUESTS:
            logger.info(f"➡️  {method.upper()} {url}")
            if "json" in kwargs and kwargs["json"]:
                logger.debug(f"   Body: {kwargs['json']}")
            if "params" in kwargs and kwargs["params"]:
                logger.debug(f"   Params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        if config.LOG_RESPONSES:
            logger.info(f"⬅️  {response.status_code} {response.reason}")
            try:
                # Если ответ в JSON, логируем его
                if response.headers.get("Content-Type", "").startswith("application/json"):
                    logger.debug(f"   Body: {response.json()}")
            except:
                pass

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Внутренний метод для выполнения запроса

        Args:
            method: HTTP метод (get, post, put, delete)
            endpoint: эндпоинт (например, /pet)

        Returns:
            Response объект
        """
        url = f"{self.base_url}{endpoint}"

        # Устанавливаем таймаут, если не передан
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        self._log_request(method, url, **kwargs)

        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {e}")
            raise

    # Публичные методы для HTTP-глаголов
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET запрос"""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST запрос"""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT запрос"""
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE запрос"""
        return self._request("DELETE", endpoint, **kwargs)

    def close(self):
        """Закрыть сессию"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()