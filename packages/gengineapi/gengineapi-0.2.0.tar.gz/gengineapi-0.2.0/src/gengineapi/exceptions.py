"""
Модуль для обработки исключений API клиента G-Engine.

Содержит иерархию исключений для различных типов ошибок,
которые могут возникнуть при взаимодействии с API.
"""
from typing import Any, Dict, Optional, Union


class ApiError(Exception):
    """Базовое исключение для всех ошибок API."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Инициализация базового исключения API.
        
        Args:
            message: Сообщение об ошибке
            status_code: HTTP-код ответа
            response_data: Данные из ответа API
        """
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Строковое представление исключения."""
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status code: {self.status_code}")
        if self.response_data:
            parts.append(f"Response data: {self.response_data}")
        return " | ".join(parts)


# Ошибки соединения
class ApiConnectionError(ApiError):
    """Исключение при ошибках соединения с API."""
    pass


class ApiTimeoutError(ApiConnectionError):
    """Исключение при превышении времени ожидания ответа от API."""
    pass


# Ошибки авторизации
class ApiAuthError(ApiError):
    """Исключение при ошибках авторизации."""
    pass


class ApiForbiddenError(ApiAuthError):
    """Исключение при отсутствии доступа к ресурсу."""
    pass


# Ошибки валидации
class ApiValidationError(ApiError):
    """Исключение при ошибках валидации запроса."""
    pass


# Ошибки ресурсов
class ApiResourceNotFoundError(ApiError):
    """Исключение при запросе несуществующего ресурса."""
    pass


# Серверные ошибки
class ApiServerError(ApiError):
    """Исключение при ошибках на стороне сервера."""
    pass


class ApiServiceUnavailableError(ApiServerError):
    """Исключение при недоступности сервиса."""
    pass


# Ошибки парсинга
class ApiParsingError(ApiError):
    """Исключение при ошибках парсинга ответа API."""
    pass


def create_api_error(
    status_code: int, 
    message: str = None, 
    response_data: Optional[Dict[str, Any]] = None
) -> ApiError:
    """
    Фабрика для создания соответствующего исключения по коду статуса HTTP.
    
    Args:
        status_code: HTTP-код ответа
        message: Сообщение об ошибке (опционально)
        response_data: Данные из ответа API (опционально)
    
    Returns:
        ApiError: Соответствующее исключение
    """
    default_message = f"API вернул ошибку со статусом {status_code}"
    message = message or default_message
    
    error_classes = {
        400: ApiValidationError,
        401: ApiAuthError,
        403: ApiForbiddenError,
        404: ApiResourceNotFoundError,
        408: ApiTimeoutError,
        500: ApiServerError,
        502: ApiServerError,
        503: ApiServiceUnavailableError,
        504: ApiTimeoutError,
    }
    
    error_class = error_classes.get(status_code, ApiError)
    return error_class(message=message, status_code=status_code, response_data=response_data)