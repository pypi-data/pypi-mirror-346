"""
Базовый класс для всех модулей API G-Engine.

Содержит общие методы и функциональность, используемые всеми модулями.
"""
import logging
from abc import ABC
from typing import Any, Dict, List, Optional, Union

from ..http import AsyncHttpClient


class BaseApiModule(ABC):
    """
    Базовый класс для всех модулей API.
    
    Attributes:
        http_client: HTTP-клиент для выполнения запросов
        logger: Логгер для записи информации
    """
    
    def __init__(
        self,
        http_client: AsyncHttpClient,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Инициализация базового класса модуля API.
        
        Args:
            http_client: HTTP-клиент для выполнения запросов
            logger: Логгер для записи информации (опционально)
        """
        self.http_client = http_client
        self.logger = logger or logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Выполняет GET-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            **kwargs: Дополнительные параметры для HTTP-клиента
            
        Returns:
            Any: Данные из ответа API
        """
        return await self.http_client.get(endpoint, params=params, **kwargs)
    
    async def _post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Выполняет POST-запрос.
        
        Args:
            endpoint: Конечная точка API
            data: Данные для отправки (опционально)
            params: Параметры запроса (опционально)
            **kwargs: Дополнительные параметры для HTTP-клиента
            
        Returns:
            Any: Данные из ответа API
        """
        return await self.http_client.post(endpoint, json_data=data, params=params, **kwargs)
    
    async def _put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Выполняет PUT-запрос.
        
        Args:
            endpoint: Конечная точка API
            data: Данные для отправки (опционально)
            params: Параметры запроса (опционально)
            **kwargs: Дополнительные параметры для HTTP-клиента
            
        Returns:
            Any: Данные из ответа API
        """
        return await self.http_client.put(endpoint, json_data=data, params=params, **kwargs)
    
    async def _delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Выполняет DELETE-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            data: Данные для отправки (опционально)
            **kwargs: Дополнительные параметры для HTTP-клиента
            
        Returns:
            Any: Данные из ответа API
        """
        return await self.http_client.delete(endpoint, params=params, json_data=data, **kwargs)

    async def _patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Выполняет PATCH-запрос.
        
        Args:
            endpoint: Конечная точка API
            data: Данные для отправки (опционально)
            params: Параметры запроса (опционально)
            **kwargs: Дополнительные параметры для HTTP-клиента
            
        Returns:
            Any: Данные из ответа API
        """
        return await self.http_client.patch(endpoint, json_data=data, params=params, **kwargs)
    
    @staticmethod
    def extract_data(response: Dict[str, Any]) -> Any:
        """
        Извлекает данные из стандартного формата ответа API.
        
        Обрабатывает общую структуру ответа G-Engine API:
        {
            "success": true,
            "message": "...",
            "data": { ... }
        }
        
        Args:
            response: Ответ от API
            
        Returns:
            Any: Извлеченные данные или исходный ответ, если не удалось извлечь
        """
        if isinstance(response, dict):
            # Для стандартного формата ответа G-Engine API
            if "success" in response and "data" in response:
                return response["data"]
        return response
    
    @staticmethod
    def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Удаляет значения None из словаря.
        
        Args:
            data: Исходный словарь
            
        Returns:
            Dict[str, Any]: Словарь без значений None
        """
        return {k: v for k, v in data.items() if v is not None}
    
    @staticmethod
    def format_date_param(date_value: Any) -> Optional[str]:
        """
        Форматирует параметр даты для API.
        
        Args:
            date_value: Значение даты (может быть строкой, объектом datetime или date)
            
        Returns:
            Optional[str]: Форматированная дата или None, если значение не было предоставлено
        """
        if date_value is None:
            return None
            
        if hasattr(date_value, "strftime"):
            # Если это datetime или date объект
            return date_value.strftime("%Y-%m-%d")
            
        # Предполагаем, что это уже строка
        return str(date_value)