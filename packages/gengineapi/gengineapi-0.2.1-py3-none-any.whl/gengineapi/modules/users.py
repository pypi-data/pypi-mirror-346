"""
Модуль для работы с пользователями в API G-Engine.

Предоставляет методы для получения информации о пользователях, их балансах и текущем пользователе.
"""
from datetime import date
from typing import Any, Dict, List, Optional, Union

from .base import BaseApiModule


class UsersModule(BaseApiModule):
    """
    Модуль для работы с пользователями.
    
    Предоставляет методы для получения информации о пользователях,
    их балансах и текущем пользователе.
    """
    
    async def get_users(
        self,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        search_field: Optional[str] = None,
        search_value: Optional[str] = None,
        role_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Получает список пользователей (только для Observer).
        
        Args:
            limit: Ограничение на количество результатов (макс. 500)
            offset: Смещение для пагинации
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки ("asc" или "desc")
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            search_field: Поле для поиска
            search_value: Значение для поиска
            role_name: Название роли для фильтрации
            
        Returns:
            List[Dict[str, Any]]: Список пользователей
            
        Examples:
            >>> async with Client(...) as client:
            >>>     users = await client.users.get_users(
            >>>         limit=50,
            >>>         role_name="User"
            >>>     )
            >>>     print(f"Получено {len(users)} пользователей")
        """
        params = self.remove_none_values({
            "limit": limit,
            "offset": offset,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "start_date": self.format_date_param(start_date),
            "end_date": self.format_date_param(end_date),
            "search_field": search_field,
            "search_value": search_value,
            "role_name": role_name,
        })
        
        self.logger.info(f"Получение списка пользователей с параметрами: {params}")
        return await self._get("user", params=params)
    
    async def get_balance(self) -> Dict[str, Any]:
        """
        Получает баланс текущего пользователя.
        
        Returns:
            Dict[str, Any]: Информация о балансе пользователя
            
        Examples:
            >>> async with Client(...) as client:
            >>>     balance = await client.users.get_balance()
            >>>     print(f"Баланс: {balance['balance']} {balance['currency']}")
        """
        self.logger.info("Получение баланса текущего пользователя")
        return await self._get("user/balance")
    
    async def get_me(self) -> Dict[str, Any]:
        """
        Получает данные текущего пользователя.
        
        Returns:
            Dict[str, Any]: Информация о текущем пользователе
            
        Examples:
            >>> async with Client(...) as client:
            >>>     user = await client.users.get_me()
            >>>     print(f"Текущий пользователь: {user['login']}")
        """
        self.logger.info("Получение данных текущего пользователя")
        return await self._get("user/me")