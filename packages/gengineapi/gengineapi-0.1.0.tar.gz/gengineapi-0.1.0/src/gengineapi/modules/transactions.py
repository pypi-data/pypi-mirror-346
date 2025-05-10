"""
Модуль для работы с транзакциями в API G-Engine.

Предоставляет методы для получения списка транзакций с различными фильтрами.
"""
from datetime import date
from typing import Any, Dict, List, Optional, Union

from .base import BaseApiModule


class TransactionsModule(BaseApiModule):
    """
    Модуль для работы с транзакциями.
    
    Предоставляет методы для получения списка транзакций с различными фильтрами.
    """
    
    async def get_transactions(
        self,
        user_cache: bool = True,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "date",
        sort_order: str = "desc",
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        search_field: Optional[str] = None,
        search_value: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Получает список транзакций.
        
        Args:
            user_cache: Использовать кэш пользователя
            limit: Ограничение на количество результатов (макс. 500)
            offset: Смещение для пагинации
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки ("asc" или "desc")
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            search_field: Поле для поиска
            search_value: Значение для поиска
            
        Returns:
            List[Dict[str, Any]]: Список транзакций
            
        Examples:
            >>> async with Client(...) as client:
            >>>     transactions = await client.transactions.get_transactions(
            >>>         limit=50,
            >>>         start_date="2023-01-01",
            >>>         end_date="2023-12-31"
            >>>     )
            >>>     print(f"Получено {len(transactions)} транзакций")
        """
        params = self.remove_none_values({
            "user_cache": user_cache,
            "limit": limit,
            "offset": offset,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "start_date": self.format_date_param(start_date),
            "end_date": self.format_date_param(end_date),
            "search_field": search_field,
            "search_value": search_value,
        })
        
        self.logger.info(f"Получение списка транзакций с параметрами: {params}")
        return await self._get("transaction/view", params=params)