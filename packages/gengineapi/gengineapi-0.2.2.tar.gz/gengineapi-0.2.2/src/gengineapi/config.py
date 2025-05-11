"""
Модуль конфигурации для клиента G-Engine API.

Предоставляет класс для централизованной настройки параметров клиента
и возможность повторного использования клиента без необходимости
каждый раз указывать параметры.
"""
import os
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, ClassVar

from .client import GEngineClient


class GEngineConfig:
    """
    Класс-конфигурация для G-Engine клиента.
    
    Позволяет настроить параметры клиента один раз и затем использовать
    их для создания экземпляров клиента без повторного указания параметров.
    
    Attributes:
        base_url: Базовый URL для API
        jwt_token: JWT токен для аутентификации
        timeout: Таймаут для запросов в секундах
        max_retries: Максимальное количество повторных попыток
        logger: Логгер для записи информации
        proxy: Прокси для запросов (например, 'socks5://user:pass@host:port')
        
    Class Attributes:
        _instance: Глобальный экземпляр клиента (для повторного использования)
    """
    # Настройки по умолчанию
    base_url: ClassVar[str] = "https://api.example.com/api/v2"
    jwt_token: ClassVar[Optional[str]] = None
    timeout: ClassVar[int] = 30
    max_retries: ClassVar[int] = 3
    logger: ClassVar[Optional[logging.Logger]] = None
    proxy: ClassVar[Optional[str]] = None
    
    # Глобальный экземпляр клиента
    _instance: ClassVar[Optional[GEngineClient]] = None
    
    @classmethod
    def setup(cls, 
              base_url: Optional[str] = None, 
              jwt_token: Optional[str] = None, 
              timeout: Optional[int] = None, 
              max_retries: Optional[int] = None,
              logger: Optional[logging.Logger] = None,
              proxy: Optional[str] = None) -> None:
        """
        Настраивает параметры клиента по умолчанию.
        
        Args:
            base_url: Базовый URL для API (опционально)
            jwt_token: JWT токен для аутентификации (опционально)
            timeout: Таймаут для запросов в секундах (опционально)
            max_retries: Максимальное количество повторных попыток (опционально)
            logger: Логгер для записи информации (опционально)
            proxy: Прокси для запросов в формате 'socks5://user:pass@host:port' (опционально)
        """
        if base_url:
            cls.base_url = base_url
        if jwt_token:
            cls.jwt_token = jwt_token
        if timeout:
            cls.timeout = timeout
        if max_retries:
            cls.max_retries = max_retries
        if logger:
            cls.logger = logger
        if proxy is not None:  # Проверяем None, чтобы можно было передать пустую строку для отключения прокси
            cls.proxy = proxy
        
        # Если есть активный глобальный клиент, закрываем его
        if cls._instance:
            import asyncio
            try:
                # Пытаемся закрыть клиент синхронно, если мы в событийном цикле
                asyncio.get_event_loop().create_task(cls.reset())
            except RuntimeError:
                # Если мы не в событийном цикле, просто отмечаем инстанс как None
                # Реальное закрытие произойдет при следующем использовании
                cls._instance = None
    
    @classmethod
    def load_from_env(cls) -> None:
        """
        Загружает настройки из переменных окружения.
        
        Ищет следующие переменные:
            - GENGINE_BASE_URL: Базовый URL для API
            - GENGINE_TOKEN: JWT токен для аутентификации
            - GENGINE_TIMEOUT: Таймаут для запросов в секундах
            - GENGINE_MAX_RETRIES: Максимальное количество повторных попыток
            - GENGINE_PROXY: Прокси для запросов
        """
        base_url = os.environ.get("GENGINE_BASE_URL")
        jwt_token = os.environ.get("GENGINE_TOKEN")
        timeout_str = os.environ.get("GENGINE_TIMEOUT")
        max_retries_str = os.environ.get("GENGINE_MAX_RETRIES")
        proxy = os.environ.get("GENGINE_PROXY")
        
        # Преобразуем строковые значения в числа, если они есть
        timeout = int(timeout_str) if timeout_str and timeout_str.isdigit() else None
        max_retries = int(max_retries_str) if max_retries_str and max_retries_str.isdigit() else None
        
        cls.setup(
            base_url=base_url,
            jwt_token=jwt_token,
            timeout=timeout,
            max_retries=max_retries,
            proxy=proxy,
        )
    
    @classmethod
    def load_from_file(cls, file_path: str) -> None:
        """
        Загружает настройки из JSON-файла.
        
        Args:
            file_path: Путь к файлу настроек
            
        Raises:
            FileNotFoundError: Если файл не существует
            json.JSONDecodeError: Если файл содержит некорректный JSON
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл конфигурации не найден: {file_path}")
        
        with open(path, "r") as f:
            config = json.load(f)
        
        cls.setup(
            base_url=config.get("base_url"),
            jwt_token=config.get("jwt_token"),
            timeout=config.get("timeout"),
            max_retries=config.get("max_retries"),
            proxy=config.get("proxy"),
        )
    
    @classmethod
    def save_to_file(cls, file_path: str) -> None:
        """
        Сохраняет текущие настройки в JSON-файл.
        
        Args:
            file_path: Путь к файлу для сохранения настроек
        """
        config = {
            "base_url": cls.base_url,
            "jwt_token": cls.jwt_token,
            "timeout": cls.timeout,
            "max_retries": cls.max_retries,
            "proxy": cls.proxy,
        }
        
        with open(file_path, "w") as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def get_client_kwargs(cls) -> Dict[str, Any]:
        """
        Возвращает словарь с параметрами для создания клиента.
        
        Returns:
            Dict[str, Any]: Словарь с параметрами клиента
        """
        return {
            "base_url": cls.base_url,
            "jwt_token": cls.jwt_token,
            "timeout": cls.timeout,
            "max_retries": cls.max_retries,
            "logger": cls.logger,
            "proxy": cls.proxy,
        }
    
    @classmethod
    def create_client(cls) -> GEngineClient:
        """
        Создает новый экземпляр клиента с текущими настройками.
        
        Returns:
            GEngineClient: Новый экземпляр клиента
        """
        return GEngineClient(**cls.get_client_kwargs())
    
    @classmethod
    async def get_client(cls) -> GEngineClient:
        """
        Возвращает глобальный экземпляр клиента или создает новый,
        если глобальный экземпляр не существует.
        
        Returns:
            GEngineClient: Экземпляр клиента
        """
        if cls._instance is None:
            cls._instance = cls.create_client()
        return cls._instance
    
    @classmethod
    async def reset(cls) -> None:
        """
        Закрывает глобальный экземпляр клиента, если он существует.
        """
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
    
    @classmethod
    async def update_token(cls, jwt_token: str) -> None:
        """
        Обновляет JWT токен в настройках и в глобальном экземпляре клиента.
        
        Args:
            jwt_token: Новый JWT токен
        """
        cls.jwt_token = jwt_token
        if cls._instance:
            cls._instance.update_token(jwt_token)
            
    @classmethod
    async def update_proxy(cls, proxy: Optional[str] = None) -> None:
        """
        Обновляет настройки прокси в конфигурации и в глобальном экземпляре клиента.
        
        Args:
            proxy: Новый прокси в формате 'socks5://user:pass@host:port' или None для отключения прокси
        """
        cls.proxy = proxy
        if cls._instance:
            # Если клиент поддерживает обновление прокси
            if hasattr(cls._instance.http_client, 'update_proxy'):
                cls._instance.http_client.update_proxy(proxy)
            else:
                # Иначе пересоздаем клиент
                await cls.reset()
                cls._instance = cls.create_client()