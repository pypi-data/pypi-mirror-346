"""
Модуль для работы с аутентификацией в API G-Engine.

Предоставляет методы для получения токенов доступа.
"""
from typing import Any, Dict

from .base import BaseApiModule


class AuthModule(BaseApiModule):
    """
    Модуль для работы с аутентификацией.
    
    Предоставляет методы для аутентификации пользователя и получения JWT-токена.
    """
    
    async def login(self, login: str, password: str) -> Dict[str, Any]:
        """
        Получает токен доступа на основе логина и пароля.
        
        Args:
            login: Логин пользователя
            password: Пароль пользователя
            
        Returns:
            Dict[str, Any]: Информация о токене доступа
            
        Examples:
            >>> async with Client(base_url="https://api.example.com") as client:
            >>>     token_info = await client.auth.login(
            >>>         login="user@example.com",
            >>>         password="password123"
            >>>     )
            >>>     print(f"Получен токен: {token_info['access_token']}")
            >>>     
            >>>     # Обновляем токен в клиенте
            >>>     client.update_token(token_info['access_token'])
        """
        data = {
            "login": login,
            "password": password,
        }
        
        self.logger.info(f"Аутентификация пользователя: {login}")
        return await self._post("auth/token", data=data)