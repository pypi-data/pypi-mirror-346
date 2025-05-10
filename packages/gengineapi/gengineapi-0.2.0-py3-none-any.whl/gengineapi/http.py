"""
Модуль, содержащий асинхронный HTTP-клиент для взаимодействия с API G-Engine.

Поддерживает JWT аутентификацию, обработку различных HTTP-методов,
автоматическое форматирование URL, механизм повторных попыток и подробное логирование.
Также поддерживает работу через прокси, включая SOCKS5.
"""
import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp
from aiohttp import ClientResponse, ClientSession, ClientTimeout, TCPConnector

from .exceptions import (
    ApiConnectionError,
    ApiError,
    ApiParsingError,
    ApiTimeoutError,
    create_api_error,
)


class AsyncHttpClient:
    """
    Асинхронный HTTP-клиент для выполнения запросов к API.
    
    Attributes:
        base_url: Базовый URL для API
        jwt_token: JWT токен для аутентификации
        timeout: Таймаут для запросов в секундах
        max_retries: Максимальное количество повторных попыток при ошибках
        retry_statuses: Список кодов статуса для повторных попыток
        retry_exceptions: Список исключений для повторных попыток
        logger: Логгер для записи информации о запросах и ответах
        proxy: Прокси для запросов (например, 'socks5://user:pass@host:port')
    """

    def __init__(
        self,
        base_url: str,
        jwt_token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_statuses: List[int] = None,
        logger: Optional[logging.Logger] = None,
        proxy: Optional[str] = None,
    ) -> None:
        """
        Инициализация HTTP-клиента.
        
        Args:
            base_url: Базовый URL для API
            jwt_token: JWT токен для аутентификации (опционально)
            timeout: Таймаут для запросов в секундах (по умолчанию 30)
            max_retries: Максимальное количество повторных попыток (по умолчанию 3)
            retry_statuses: Список кодов статуса для повторных попыток 
                            (по умолчанию [429, 500, 502, 503, 504])
            logger: Логгер для записи информации о запросах и ответах (опционально)
            proxy: Прокси для запросов в формате 'socks5://user:pass@host:port' (опционально)
        """
        self.base_url = base_url.rstrip("/")
        self.jwt_token = jwt_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_statuses = retry_statuses or [429, 500, 502, 503, 504]
        self.retry_exceptions = (
            aiohttp.ClientError,
            asyncio.TimeoutError,
        )
        self.logger = logger or logging.getLogger(__name__)
        self.proxy = proxy
        self._session: Optional[ClientSession] = None
        self._session_lock = asyncio.Lock()
        
        # Проверяем, является ли прокси SOCKS5
        if self.proxy and self.proxy.startswith('socks5://'):
            try:
                # Попытка импортировать aiohttp_socks
                import aiohttp_socks
                self.logger.info(f"Используется SOCKS5 прокси: {self.proxy}")
            except ImportError:
                self.logger.error("Для использования SOCKS5 прокси необходимо установить пакет 'aiohttp-socks'")
                self.logger.error("Установите его с помощью: pip install aiohttp-socks")
                self.proxy = None

    async def _ensure_session(self) -> ClientSession:
        """
        Убеждается, что сессия aiohttp существует и валидна.
        
        Returns:
            ClientSession: Активная aiohttp сессия
        """
        if self._session is None or self._session.closed:
            async with self._session_lock:
                if self._session is None or self._session.closed:
                    timeout = ClientTimeout(total=self.timeout)
                    
                    # Создаем соответствующий коннектор в зависимости от настроек прокси
                    if self.proxy:
                        if self.proxy.startswith('socks5://'):
                            try:
                                # Импортируем aiohttp_socks для поддержки SOCKS5 прокси
                                from aiohttp_socks import ProxyConnector
                                connector = ProxyConnector.from_url(self.proxy, ssl=False)
                                self.logger.debug(f"Создан SOCKS5 коннектор для прокси: {self.proxy}")
                            except ImportError:
                                self.logger.error("Не удалось импортировать aiohttp_socks")
                                connector = TCPConnector(ssl=False)
                        else:
                            # Для HTTP/HTTPS прокси используем встроенные возможности aiohttp
                            connector = TCPConnector(ssl=False)
                            self.logger.debug(f"Будет использован HTTP прокси: {self.proxy}")
                    else:
                        connector = TCPConnector(ssl=False)
                    
                    # Создаем сессию
                    session_kwargs = {
                        'timeout': timeout,
                        'connector': connector,
                        'raise_for_status': False,
                    }
                    
                    # Добавляем прокси для HTTP/HTTPS прокси
                    if self.proxy and not self.proxy.startswith('socks5://'):
                        session_kwargs['proxy'] = self.proxy
                    
                    self._session = ClientSession(**session_kwargs)
        
        return self._session

    def _build_url(self, endpoint: str) -> str:
        """
        Формирует полный URL для запроса.
        
        Args:
            endpoint: Конечная точка API
            
        Returns:
            str: Полный URL для запроса
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Формирует заголовки для запроса, включая авторизацию.
        
        Args:
            additional_headers: Дополнительные заголовки для запроса
            
        Returns:
            Dict[str, str]: Заголовки для запроса
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
            
        if additional_headers:
            headers.update(additional_headers)
            
        return headers

    async def _parse_response(self, response: ClientResponse) -> Dict[str, Any]:
        """
        Парсит ответ от API.
        
        Args:
            response: Ответ от API
            
        Returns:
            Dict[str, Any]: Данные из ответа API
            
        Raises:
            ApiParsingError: Если не удалось распарсить ответ
        """
        try:
            if response.content_type.startswith("application/json"):
                return await response.json()
            else:
                text = await response.text()
                return {"text": text}
        except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
            status_text = await response.text()
            self.logger.error(f"Ошибка парсинга ответа: {str(e)}, Содержимое: {status_text[:100]}...")
            raise ApiParsingError(f"Не удалось распарсить ответ: {str(e)}")

    async def _handle_error_response(self, response: ClientResponse) -> None:
        """
        Обрабатывает ответы с ошибками от API.
        
        Args:
            response: Ответ от API с ошибкой
            
        Raises:
            ApiError: Соответствующее исключение в зависимости от кода ответа
        """
        try:
            response_data = await self._parse_response(response)
        except ApiParsingError:
            response_data = {}
        
        # Получаем сообщение об ошибке из ответа, если оно есть
        message = None
        if isinstance(response_data, dict):
            message = response_data.get("message")
            if not message and "detail" in response_data:
                # Обработка ошибок валидации FastAPI
                detail = response_data["detail"]
                if isinstance(detail, list) and detail:
                    errors = [f"{e.get('loc', [''])[0]}: {e.get('msg', '')}" for e in detail if isinstance(e, dict)]
                    message = ", ".join(errors)
                else:
                    message = str(detail)
        
        # Создаем соответствующее исключение
        raise create_api_error(
            status_code=response.status,
            message=message,
            response_data=response_data,
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP-запрос с повторными попытками.
        
        Args:
            method: HTTP-метод (GET, POST, PUT, DELETE, etc.)
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            json_data: Данные для отправки в формате JSON (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
            
        Raises:
            ApiConnectionError: При ошибке соединения
            ApiTimeoutError: При превышении времени ожидания
            ApiError: При других ошибках API
        """
        url = self._build_url(endpoint)
        request_headers = self._get_headers(headers)
        request_timeout = ClientTimeout(total=timeout or self.timeout)
        
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                attempt += 1
                session = await self._ensure_session()
                
                # Логирование запроса на уровне DEBUG
                self.logger.debug(
                    f"Запрос {method} {url} (попытка {attempt}/{self.max_retries + 1}). "
                    f"Параметры: {params}, Данные: {json_data}, Заголовки: {request_headers}"
                )
                if self.proxy:
                    self.logger.debug(f"Запрос выполняется через прокси: {self.proxy}")
                
                start_time = time.time()
                async with session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=request_headers,
                    timeout=request_timeout,
                ) as response:
                    elapsed_time = time.time() - start_time
                    
                    # Логирование ответа на уровне DEBUG
                    self.logger.debug(
                        f"Ответ на {method} {url}: статус {response.status}, "
                        f"заголовки {dict(response.headers)}, время {elapsed_time:.2f}с"
                    )
                    
                    # Если успешный ответ
                    if 200 <= response.status < 300:
                        return await self._parse_response(response)
                    
                    # Если ошибка, но нужно повторить
                    if response.status in self.retry_statuses and attempt <= self.max_retries:
                        delay = self._calculate_retry_delay(attempt)
                        self.logger.warning(
                            f"Получен статус {response.status} при запросе {method} {url}. "
                            f"Повторная попытка через {delay:.2f}с (попытка {attempt})"
                        )
                        await asyncio.sleep(delay)
                        continue
                    
                    # Если ошибка и больше не повторяем
                    await self._handle_error_response(response)
                
            except self.retry_exceptions as e:
                last_error = e
                if attempt <= self.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    error_type = type(e).__name__
                    self.logger.warning(
                        f"Ошибка {error_type} при запросе {method} {url}: {str(e)}. "
                        f"Повторная попытка через {delay:.2f}с (попытка {attempt})"
                    )
                    await asyncio.sleep(delay)
                else:
                    break
        
        # Если все попытки неудачные
        if isinstance(last_error, asyncio.TimeoutError):
            raise ApiTimeoutError(f"Превышено время ожидания при запросе {method} {url} после {attempt} попыток")
        else:
            raise ApiConnectionError(f"Ошибка соединения при запросе {method} {url} после {attempt} попыток: {last_error}")

    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Вычисляет задержку перед повторной попыткой с экспоненциальным ростом.
        
        Args:
            attempt: Номер попытки (начиная с 1)
            
        Returns:
            float: Задержка в секундах
        """
        # Экспоненциальная задержка с небольшим случайным разбросом
        import random
        base_delay = min(2 ** (attempt - 1), 30)  # Ограничиваем до 30 секунд
        jitter = random.uniform(0, 0.5 * base_delay)  # Добавляем до 50% случайности
        return base_delay + jitter

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет GET-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("GET", endpoint, params=params, headers=headers, timeout=timeout)

    async def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет POST-запрос.
        
        Args:
            endpoint: Конечная точка API
            json_data: Данные для отправки в формате JSON (опционально)
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("POST", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)

    async def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет PUT-запрос.
        
        Args:
            endpoint: Конечная точка API
            json_data: Данные для отправки в формате JSON (опционально)
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("PUT", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет DELETE-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            json_data: Данные для отправки в формате JSON (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("DELETE", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)

    async def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет PATCH-запрос.
        
        Args:
            endpoint: Конечная точка API
            json_data: Данные для отправки в формате JSON (опционально)
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("PATCH", endpoint, params=params, json_data=json_data, headers=headers, timeout=timeout)

    async def head(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет HEAD-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("HEAD", endpoint, params=params, headers=headers, timeout=timeout)

    async def options(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет OPTIONS-запрос.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса (опционально)
            headers: Дополнительные заголовки для запроса (опционально)
            timeout: Таймаут для запроса в секундах (опционально)
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        return await self._request("OPTIONS", endpoint, params=params, headers=headers, timeout=timeout)

    async def close(self) -> None:
        """Закрывает сессию aiohttp."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    def update_token(self, jwt_token: str) -> None:
        """
        Обновляет JWT токен для аутентификации.
        
        Args:
            jwt_token: Новый JWT токен
        """
        self.jwt_token = jwt_token
        
    def update_proxy(self, proxy: Optional[str] = None) -> None:
        """
        Обновляет настройки прокси.
        
        Args:
            proxy: Новый прокси в формате 'socks5://user:pass@host:port' или None для отключения прокси
        """
        # Если прокси изменился, нужно закрыть существующую сессию
        if self.proxy != proxy:
            self.proxy = proxy
            
            # Закрываем сессию, чтобы при следующем запросе она была пересоздана с новыми настройками
            if self._session and not self._session.closed:
                asyncio.create_task(self._session.close())
                self._session = None
            
            # Проверяем, если указан SOCKS5 прокси, нужен ли aiohttp_socks
            if self.proxy and self.proxy.startswith('socks5://'):
                try:
                    import aiohttp_socks
                    self.logger.info(f"Используется SOCKS5 прокси: {self.proxy}")
                except ImportError:
                    self.logger.error("Для использования SOCKS5 прокси необходимо установить пакет 'aiohttp-socks'")
                    self.logger.error("Установите его с помощью: pip install aiohttp-socks")
                    self.proxy = None