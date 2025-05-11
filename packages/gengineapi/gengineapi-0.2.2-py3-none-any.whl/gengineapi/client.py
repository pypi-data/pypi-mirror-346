"""
Основной класс клиента API G-Engine.

Предоставляет интерфейс для взаимодействия со всеми модулями API
и управления соединением.
"""
import logging
from typing import Optional

from .http import AsyncHttpClient
from .modules import (
    AuthModule,
    CurrenciesModule,
    FinancesModule,
    PaymentsModule,
    TransactionsModule,
    UsersModule,
)


class GEngineClient:
    """
    Клиент для API G-Engine.
    
    Предоставляет доступ ко всем модулям API через единый интерфейс
    и управляет жизненным циклом HTTP-соединения.
    """
    
    def __init__(
        self,
        base_url: str,
        jwt_token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        logger: Optional[logging.Logger] = None,
        proxy: Optional[str] = None,
    ) -> None:
        """
        Инициализирует клиент API G-Engine.
        
        Args:
            base_url: Базовый URL для API
            jwt_token: JWT токен для аутентификации (если уже есть)
            timeout: Таймаут для запросов в секундах (по умолчанию 30)
            max_retries: Максимальное количество повторных попыток (по умолчанию 3)
            logger: Логгер для записи информации (опционально)
            proxy: Прокси для запросов в формате 'socks5://user:pass@host:port' (опционально)
        """
        self.logger = logger or logging.getLogger(__name__)
        
        if jwt_token:
            self.logger.info("Клиент инициализирован с существующим JWT токеном")
        
        if proxy:
            self.logger.info(f"Клиент будет использовать прокси: {proxy}")
        
        # Инициализация HTTP-клиента
        self.http_client = AsyncHttpClient(
            base_url=base_url,
            jwt_token=jwt_token,
            timeout=timeout,
            max_retries=max_retries,
            logger=self.logger,
            proxy=proxy,
        )
        
        # Инициализация модулей API
        self.auth = AuthModule(http_client=self.http_client, logger=self.logger)
        self.payments = PaymentsModule(http_client=self.http_client, logger=self.logger)
        self.finances = FinancesModule(http_client=self.http_client, logger=self.logger)
        self.users = UsersModule(http_client=self.http_client, logger=self.logger)
        self.transactions = TransactionsModule(http_client=self.http_client, logger=self.logger)
        self.currencies = CurrenciesModule(http_client=self.http_client, logger=self.logger)
    
    async def close(self) -> None:
        """
        Закрывает соединение с API.
        
        Должен быть вызван при завершении работы с клиентом.
        """
        await self.http_client.close()
        self.logger.info("Соединение с API закрыто")
    
    async def __aenter__(self) -> "GEngineClient":
        """
        Поддержка контекстного менеджера (async with).
        
        Returns:
            GEngineClient: Экземпляр клиента API
        """
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Закрывает соединение при выходе из контекстного менеджера.
        """
        await self.close()
    
    def update_token(self, jwt_token: str) -> None:
        """
        Обновляет JWT токен для аутентификации.
        
        Args:
            jwt_token: Новый JWT токен
        """
        self.http_client.update_token(jwt_token)
        self.logger.info("JWT токен обновлен")
        
    def update_proxy(self, proxy: Optional[str] = None) -> None:
        """
        Обновляет настройки прокси.
        
        Args:
            proxy: Новый прокси в формате 'socks5://user:pass@host:port' или None для отключения прокси
        """
        if hasattr(self.http_client, 'update_proxy'):
            self.http_client.update_proxy(proxy)
            if proxy:
                self.logger.info(f"Прокси обновлен: {proxy}")
            else:
                self.logger.info("Прокси отключен")
