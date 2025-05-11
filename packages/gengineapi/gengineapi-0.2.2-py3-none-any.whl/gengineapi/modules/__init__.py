"""
Пакет с модулями API клиента G-Engine.

Экспортирует классы модулей для различных функциональных областей API.
"""

from .auth import AuthModule
from .base import BaseApiModule
from .currencies import CurrenciesModule
from .finances import FinancesModule
from .payments import PaymentsModule
from .transactions import TransactionsModule
from .users import UsersModule

__all__ = [
    'AuthModule',
    'BaseApiModule',
    'CurrenciesModule',
    'FinancesModule',
    'PaymentsModule',
    'TransactionsModule',
    'UsersModule',
]