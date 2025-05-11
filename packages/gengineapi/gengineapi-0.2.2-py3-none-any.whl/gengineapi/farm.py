"""
Модуль, предоставляющий функциональность для управления фермой клиентов G-Engine API.

Позволяет создавать и управлять несколькими независимыми клиентами
с различными конфигурациями, прокси и токенами аутентификации.
"""
import asyncio
import logging
import uuid
from typing import Dict, Optional, List, Any

from .client import GEngineClient


class ClientConfig:
    """
    Класс конфигурации для отдельного клиента.
    
    Позволяет хранить и управлять параметрами для создания клиента.
    
    Attributes:
        name: Уникальное имя конфигурации
        base_url: Базовый URL для API
        jwt_token: JWT токен для аутентификации
        timeout: Таймаут для запросов в секундах
        max_retries: Максимальное количество повторных попыток
        logger: Логгер для записи информации
        proxy: Прокси для запросов
        client: Экземпляр клиента, если он был создан
    """
    
    def __init__(
        self,
        base_url: str,
        jwt_token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        logger: Optional[logging.Logger] = None,
        proxy: Optional[str] = None,
        name: Optional[str] = None,  # Уникальное имя конфига
        tags: Optional[List[str]] = None,  # Теги для группировки и фильтрации
    ) -> None:
        """
        Инициализация конфигурации клиента.
        
        Args:
            base_url: Базовый URL для API
            jwt_token: JWT токен для аутентификации (опционально)
            timeout: Таймаут для запросов в секундах (по умолчанию 30)
            max_retries: Максимальное количество повторных попыток (по умолчанию 3)
            logger: Логгер для записи информации (опционально)
            proxy: Прокси для запросов в формате 'socks5://user:pass@host:port' (опционально)
            name: Уникальное имя конфигурации (опционально, генерируется автоматически)
            tags: Список тегов для группировки и фильтрации (опционально)
        """
        self.base_url = base_url
        self.jwt_token = jwt_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger
        self.proxy = proxy
        self.name = name or str(uuid.uuid4())
        self.tags = tags or []
        self.client: Optional[GEngineClient] = None
        self.last_used: float = 0  # Время последнего использования (для ротации)
        self.error_count: int = 0  # Счетчик ошибок
        self.success_count: int = 0  # Счетчик успешных запросов
        self.is_active: bool = True  # Флаг активности конфигурации

    async def get_client(self) -> GEngineClient:
        """
        Возвращает клиент или создает новый, если он не существует.
        
        Returns:
            GEngineClient: Экземпляр клиента API
        """
        if self.client is None:
            self.client = GEngineClient(
                base_url=self.base_url,
                jwt_token=self.jwt_token,
                timeout=self.timeout,
                max_retries=self.max_retries,
                logger=self.logger,
                proxy=self.proxy
            )
        
        # Обновляем время последнего использования
        import time
        self.last_used = time.time()
        
        return self.client
    
    async def close(self) -> None:
        """Закрывает клиент."""
        if self.client:
            await self.client.close()
            self.client = None
    
    def update_token(self, jwt_token: str) -> None:
        """
        Обновляет JWT токен в конфигурации и в клиенте, если он существует.
        
        Args:
            jwt_token: Новый JWT токен
        """
        self.jwt_token = jwt_token
        if self.client:
            self.client.update_token(jwt_token)
    
    def update_proxy(self, proxy: Optional[str] = None) -> None:
        """
        Обновляет настройки прокси в конфигурации и в клиенте, если он существует.
        
        Args:
            proxy: Новый прокси или None для отключения прокси
        """
        self.proxy = proxy
        if self.client:
            if hasattr(self.client, 'update_proxy'):
                self.client.update_proxy(proxy)
            else:
                # Если клиент не поддерживает динамическое обновление прокси,
                # закрываем его и создадим новый при следующем запросе
                asyncio.create_task(self.close())
    
    def deactivate(self) -> None:
        """Деактивирует конфигурацию."""
        self.is_active = False
    
    def activate(self) -> None:
        """Активирует конфигурацию."""
        self.is_active = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует конфигурацию в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с параметрами конфигурации
        """
        return {
            "name": self.name,
            "base_url": self.base_url,
            "jwt_token": self.jwt_token,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "proxy": self.proxy,
            "tags": self.tags,
            "is_active": self.is_active,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "last_used": self.last_used,
        }


class ClientFarm:
    """
    Управляет фермой клиентов с разными конфигурациями.
    
    Позволяет создавать, хранить и использовать множество клиентов
    с разными настройками, токенами и прокси.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Инициализация фермы клиентов.
        
        Args:
            logger: Логгер для записи информации (опционально)
        """
        self.configs: Dict[str, ClientConfig] = {}
        self.logger = logger or logging.getLogger(__name__)
        self._selection_strategy: str = "round_robin"  # Стратегия выбора клиента
        self._last_used_index: int = -1  # Индекс последнего использованного клиента
    
    def add_config(self, config: ClientConfig) -> None:
        """
        Добавляет конфигурацию в ферму.
        
        Args:
            config: Конфигурация клиента
        """
        self.configs[config.name] = config
        self.logger.info(f"Добавлена конфигурация: {config.name}")
    
    def create_config(self, **kwargs) -> ClientConfig:
        """
        Создает и добавляет новую конфигурацию.
        
        Args:
            **kwargs: Параметры для создания конфигурации
            
        Returns:
            ClientConfig: Созданная конфигурация
        """
        config = ClientConfig(**kwargs)
        self.add_config(config)
        return config
    
    async def get_client(self, name: str) -> Optional[GEngineClient]:
        """
        Возвращает клиент по имени конфигурации.
        
        Args:
            name: Имя конфигурации
            
        Returns:
            Optional[GEngineClient]: Экземпляр клиента или None, если конфигурация не найдена
        """
        config = self.configs.get(name)
        if config and config.is_active:
            return await config.get_client()
        return None
    
    async def get_next_client(self, tag: Optional[str] = None) -> Optional[GEngineClient]:
        """
        Возвращает следующий клиент согласно выбранной стратегии.
        
        Args:
            tag: Тег для фильтрации клиентов (опционально)
            
        Returns:
            Optional[GEngineClient]: Экземпляр клиента или None, если нет доступных клиентов
        """
        active_configs = [
            config for config in self.configs.values()
            if config.is_active and (tag is None or tag in config.tags)
        ]
        
        if not active_configs:
            self.logger.warning("Нет доступных конфигураций клиентов")
            return None
        
        if self._selection_strategy == "round_robin":
            # Стратегия Round Robin
            self._last_used_index = (self._last_used_index + 1) % len(active_configs)
            config = active_configs[self._last_used_index]
            return await config.get_client()
        
        elif self._selection_strategy == "random":
            # Случайный выбор
            import random
            config = random.choice(active_configs)
            return await config.get_client()
        
        elif self._selection_strategy == "least_errors":
            # Выбираем клиент с наименьшим количеством ошибок
            config = min(active_configs, key=lambda c: c.error_count)
            return await config.get_client()
        
        elif self._selection_strategy == "least_recently_used":
            # Выбираем наименее недавно использованный клиент
            config = min(active_configs, key=lambda c: c.last_used)
            return await config.get_client()
        
        else:
            # По умолчанию используем Round Robin
            self._last_used_index = (self._last_used_index + 1) % len(active_configs)
            config = active_configs[self._last_used_index]
            return await config.get_client()
    
    def set_selection_strategy(self, strategy: str) -> None:
        """
        Устанавливает стратегию выбора клиента.
        
        Args:
            strategy: Стратегия выбора ('round_robin', 'random', 'least_errors', 'least_recently_used')
        """
        valid_strategies = ["round_robin", "random", "least_errors", "least_recently_used"]
        if strategy not in valid_strategies:
            raise ValueError(f"Недопустимая стратегия выбора: {strategy}. "
                            f"Должна быть одна из: {', '.join(valid_strategies)}")
        
        self._selection_strategy = strategy
        self.logger.info(f"Установлена стратегия выбора клиента: {strategy}")
    
    async def close_client(self, name: str) -> None:
        """
        Закрывает клиент по имени конфигурации.
        
        Args:
            name: Имя конфигурации
        """
        config = self.configs.get(name)
        if config:
            await config.close()
            self.logger.info(f"Клиент закрыт: {name}")
    
    async def close_all(self) -> None:
        """Закрывает все клиенты в ферме."""
        for name, config in self.configs.items():
            await config.close()
            self.logger.info(f"Клиент закрыт: {name}")
    
    def remove_config(self, name: str) -> None:
        """
        Удаляет конфигурацию из фермы.
        
        Args:
            name: Имя конфигурации
        """
        if name in self.configs:
            config = self.configs[name]
            # Запустим задачу на закрытие клиента, если он существует
            if config.client:
                asyncio.create_task(config.close())
            del self.configs[name]
            self.logger.info(f"Конфигурация удалена: {name}")
    
    def get_configs_by_tag(self, tag: str) -> List[ClientConfig]:
        """
        Возвращает список конфигураций с указанным тегом.
        
        Args:
            tag: Тег для фильтрации
            
        Returns:
            List[ClientConfig]: Список конфигураций с указанным тегом
        """
        return [config for config in self.configs.values() if tag in config.tags]
    
    def get_active_configs(self) -> List[ClientConfig]:
        """
        Возвращает список активных конфигураций.
        
        Returns:
            List[ClientConfig]: Список активных конфигураций
        """
        return [config for config in self.configs.values() if config.is_active]
    
    def deactivate_config(self, name: str) -> None:
        """
        Деактивирует конфигурацию.
        
        Args:
            name: Имя конфигурации
        """
        if name in self.configs:
            self.configs[name].deactivate()
            self.logger.info(f"Конфигурация деактивирована: {name}")
    
    def activate_config(self, name: str) -> None:
        """
        Активирует конфигурацию.
        
        Args:
            name: Имя конфигурации
        """
        if name in self.configs:
            self.configs[name].activate()
            self.logger.info(f"Конфигурация активирована: {name}")
    
    def register_error(self, name: str) -> None:
        """
        Регистрирует ошибку для указанной конфигурации.
        
        Args:
            name: Имя конфигурации
        """
        if name in self.configs:
            self.configs[name].error_count += 1
            
            # Если превышен порог ошибок, деактивируем конфигурацию
            if self.configs[name].error_count >= 10:  # Пример порога
                self.configs[name].deactivate()
                self.logger.warning(f"Конфигурация деактивирована из-за ошибок: {name}")
    
    def register_success(self, name: str) -> None:
        """
        Регистрирует успешное использование указанной конфигурации.
        
        Args:
            name: Имя конфигурации
        """
        if name in self.configs:
            self.configs[name].success_count += 1
            
            # Если клиент был деактивирован из-за ошибок, но успешно выполнил запрос,
            # сбрасываем счетчик ошибок и активируем его снова
            if not self.configs[name].is_active and self.configs[name].error_count > 0:
                self.configs[name].error_count = 0
                self.configs[name].activate()
                self.logger.info(f"Конфигурация активирована после успешного запроса: {name}")
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Возвращает статистику по всем конфигурациям.
        
        Returns:
            Dict[str, Dict[str, Any]]: Словарь со статистикой
        """
        return {name: config.to_dict() for name, config in self.configs.items()}
    
    async def export_configs(self, file_path: str) -> None:
        """
        Экспортирует конфигурации в JSON-файл.
        
        Args:
            file_path: Путь к файлу для экспорта
        """
        import json
        
        # Закрываем все клиенты перед экспортом
        await self.close_all()
        
        # Получаем данные конфигураций
        configs_data = {name: config.to_dict() for name, config in self.configs.items()}
        
        # Сохраняем в файл
        with open(file_path, "w") as f:
            json.dump(configs_data, f, indent=2)
        
        self.logger.info(f"Конфигурации экспортированы в файл: {file_path}")
    
    @classmethod
    async def import_configs(cls, file_path: str, logger: Optional[logging.Logger] = None) -> "ClientFarm":
        """
        Импортирует конфигурации из JSON-файла.
        
        Args:
            file_path: Путь к файлу с конфигурациями
            logger: Логгер для записи информации (опционально)
            
        Returns:
            ClientFarm: Новый экземпляр фермы клиентов с импортированными конфигурациями
        """
        import json
        
        farm = cls(logger=logger)
        
        try:
            # Загружаем данные из файла
            with open(file_path, "r") as f:
                configs_data = json.load(f)
            
            # Создаем конфигурации на основе данных
            for name, data in configs_data.items():
                # Извлекаем только параметры, необходимые для создания конфигурации
                config_params = {
                    "name": data.get("name"),
                    "base_url": data.get("base_url"),
                    "jwt_token": data.get("jwt_token"),
                    "timeout": data.get("timeout"),
                    "max_retries": data.get("max_retries"),
                    "proxy": data.get("proxy"),
                    "tags": data.get("tags", []),
                }
                
                # Создаем конфигурацию
                config = ClientConfig(**config_params)
                
                # Устанавливаем дополнительные параметры
                config.is_active = data.get("is_active", True)
                config.error_count = data.get("error_count", 0)
                config.success_count = data.get("success_count", 0)
                
                # Добавляем конфигурацию в ферму
                farm.add_config(config)
        except Exception as e:
            if logger:
                logger.error(f"Ошибка при импорте конфигураций: {e}")
            raise
        
        return farm
