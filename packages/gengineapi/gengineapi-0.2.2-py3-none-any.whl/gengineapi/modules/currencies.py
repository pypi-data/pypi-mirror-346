"""
Модуль для работы с курсами валют в API G-Engine.

Предоставляет методы для получения актуальных курсов валют.
"""
from typing import Any, Dict, Literal, Optional, Union

from .base import BaseApiModule


# Типы для параметров API
RateSource = Literal["cb_rf", "steam"]
CurrencyPair = Literal["USD:RUB", "EUR:RUB"]


class CurrenciesModule(BaseApiModule):
    """
    Модуль для работы с курсами валют.
    
    Предоставляет методы для получения актуальных курсов валют.
    """
    
    async def get_rate(
        self,
        source: RateSource,
        pair: CurrencyPair,
    ) -> Dict[str, Any]:
        """
        Получает актуальный курс валют.
        
        Args:
            source: Источник курса валют ("cb_rf" или "steam")
            pair: Валютная пара ("USD:RUB" или "EUR:RUB")
            
        Returns:
            Dict[str, Any]: Информация о курсе валют
            
        Examples:
            >>> async with Client(...) as client:
            >>>     rate = await client.currencies.get_rate(
            >>>         source="cb_rf",
            >>>         pair="USD:RUB"
            >>>     )
            >>>     print(f"Курс USD:RUB по ЦБ РФ: {rate['currency_rate']}")
        """
        params = {
            "source": source,
            "pair": pair,
        }
        
        self.logger.info(f"Получение курса валют: источник {source}, пара {pair}")
        response = await self._get("currencies", params=params)
        
        return self.extract_data(response)