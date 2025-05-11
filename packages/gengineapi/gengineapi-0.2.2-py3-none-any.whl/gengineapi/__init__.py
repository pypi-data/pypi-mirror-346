"""
G-Engine API Client - Асинхронный модульный клиент для взаимодействия с API G-Engine.

Предоставляет удобный интерфейс для работы с платежами, финансами, 
пользователями и другими ресурсами API G-Engine.
"""

from .client import GEngineClient
from .config import GEngineConfig
from .exceptions import (
    ApiAuthError,
    ApiConnectionError,
    ApiError,
    ApiForbiddenError,
    ApiParsingError,
    ApiResourceNotFoundError,
    ApiServerError,
    ApiServiceUnavailableError,
    ApiTimeoutError,
    ApiValidationError,
)
from .farm import ClientFarm, ClientConfig
from .http import AsyncHttpClient

__version__ = "1.0.0"
__all__ = [
    # Основной клиент
    'GEngineClient',
    # Конфигурация
    'GEngineConfig',
    # HTTP клиент
    'AsyncHttpClient',
    # Ферма клиентов
    'ClientFarm',
    'ClientConfig',
    # Исключения
    'ApiError',
    'ApiConnectionError',
    'ApiTimeoutError',
    'ApiAuthError',
    'ApiForbiddenError',
    'ApiValidationError',
    'ApiResourceNotFoundError',
    'ApiServerError',
    'ApiServiceUnavailableError',
    'ApiParsingError',
]