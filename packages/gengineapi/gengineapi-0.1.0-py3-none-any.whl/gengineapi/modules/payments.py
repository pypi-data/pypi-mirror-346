"""
Модуль для работы с платежами в API G-Engine.

Поддерживает создание и верификацию платежей, выполнение платежей и получение статуса платежей.
"""
from decimal import Decimal
from typing import Any, Dict, Optional, Union

from .base import BaseApiModule


class PaymentsModule(BaseApiModule):
    """
    Модуль для работы с платежами.
    
    Предоставляет методы для создания, верификации и выполнения платежей,
    а также для получения статуса платежей.
    """
    
    async def verify(
        self,
        transaction_id: str,
        service_id: int,
        account: str,
        amount: Union[Decimal, float, str],
        currency: str,
    ) -> Dict[str, Any]:
        """
        Создает и верифицирует платеж.
        
        Args:
            transaction_id: Идентификатор транзакции (UUID)
            service_id: Идентификатор сервиса
            account: Аккаунт для пополнения
            amount: Сумма транзакции
            currency: Код валюты (3 символа)
            
        Returns:
            Dict[str, Any]: Информация о созданном платеже
            
        Examples:
            >>> async with Client(...) as client:
            >>>     payment = await client.payments.verify(
            >>>         transaction_id="b3f1c8d2-4e9a-42f5-bb8d-8e3b6c6c6a7f",
            >>>         service_id=1,
            >>>         account="user@example.com",
            >>>         amount=10.99,
            >>>         currency="USD"
            >>>     )
            >>>     print(f"Создан платеж: {payment['transaction_id']}")
        """
        # Преобразуем amount в строку, если это не строка
        if not isinstance(amount, str):
            amount = str(amount)
            
        data = {
            "transaction_id": transaction_id,
            "service_id": service_id,
            "account": account,
            "amount": amount,
            "currency": currency,
        }
        
        self.logger.info(f"Создание платежа: {transaction_id}, сервис: {service_id}, сумма: {amount} {currency}")
        response = await self._post("payment/verify", data=data)
        
        return self.extract_data(response)
    
    async def execute(self, transaction_id: str) -> Dict[str, Any]:
        """
        Выполняет платеж на основе идентификатора транзакции.
        
        Args:
            transaction_id: Идентификатор транзакции (UUID)
            
        Returns:
            Dict[str, Any]: Результат выполнения платежа
            
        Examples:
            >>> async with Client(...) as client:
            >>>     result = await client.payments.execute(
            >>>         transaction_id="b3f1c8d2-4e9a-42f5-bb8d-8e3b6c6c6a7f"
            >>>     )
            >>>     print(f"Статус платежа: {result['status_code']}")
        """
        data = {"transaction_id": transaction_id}
        
        self.logger.info(f"Выполнение платежа для транзакции: {transaction_id}")
        response = await self._post("payment/execute", data=data)
        
        return self.extract_data(response)
    
    async def get_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Получает статус платежа.
        
        Args:
            transaction_id: Идентификатор транзакции (UUID)
            
        Returns:
            Dict[str, Any]: Статус платежа
            
        Examples:
            >>> async with Client(...) as client:
            >>>     status = await client.payments.get_status(
            >>>         transaction_id="b3f1c8d2-4e9a-42f5-bb8d-8e3b6c6c6a7f"
            >>>     )
            >>>     print(f"Текущий статус платежа: {status['status_code']}")
        """
        params = {"transaction_id": transaction_id}
        
        self.logger.info(f"Получение статуса платежа для транзакции: {transaction_id}")
        response = await self._get("payment/status", params=params)
        
        return self.extract_data(response)