"""
Модуль для работы с финансами в API G-Engine.

Предоставляет методы для получения данных о финансах по кошелькам пользователей.
"""
from datetime import date
from typing import Any, Dict, List, Optional, Union

from .base import BaseApiModule


class FinancesModule(BaseApiModule):
    """
    Модуль для работы с финансами.
    
    Предоставляет методы для получения финансовой информации по кошелькам пользователей.
    """
    
    async def get_finances(
        self,
        user_cache: bool = True,
        funds_type: Optional[str] = None,
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
        Получает данные о финансах по кошелькам пользователей.
        
        Args:
            user_cache: Использовать кэш пользователя
            funds_type: Тип средств ("balance" или "cashback")
            limit: Ограничение на количество результатов (макс. 500)
            offset: Смещение для пагинации
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки ("asc" или "desc")
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            search_field: Поле для поиска
            search_value: Значение для поиска
            
        Returns:
            List[Dict[str, Any]]: Список финансовых данных
            
        Examples:
            >>> async with Client(...) as client:
            >>>     finances = await client.finances.get_finances(
            >>>         funds_type="balance",
            >>>         limit=50,
            >>>         sort_by="amount",
            >>>         sort_order="desc"
            >>>     )
            >>>     print(f"Получено {len(finances)} финансовых записей")
        """
        params = self.remove_none_values({
            "user_cache": user_cache,
            "funds_type": funds_type,
            "limit": limit,
            "offset": offset,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "start_date": self.format_date_param(start_date),
            "end_date": self.format_date_param(end_date),
            "search_field": search_field,
            "search_value": search_value,
        })
        
        self.logger.info(f"Получение финансовых данных с параметрами: {params}")
        response = await self._get("finances", params=params)
        
        # В этом API ожидаем список данных в поле "data"
        data = self.extract_data(response)
        if data is None:
            return []
        
        return data