# G-Engine API Client

Асинхронный модульный клиент для взаимодействия с API G-Engine.

## Особенности

- Полностью асинхронный интерфейс на базе `aiohttp` и `asyncio`
- Модульная структура с разделением по доменам API
- Детальная обработка ошибок и исключений
- Автоматические повторные попытки для временных ошибок
- Поддержка JWT-аутентификации
- Поддержка прокси, включая SOCKS5
- Подробное логирование
- Строгая типизация с помощью аннотаций типов
- Класс-конфигурация для централизованной настройки и повторного использования

## Установка

```bash
pip install -r requirements.txt
```

Или с помощью setup.py:

```bash
pip install .
```

## Структура проекта

```
gengine_client/
├── __init__.py            # Экспорт основных классов
├── client.py              # Основной класс клиента
├── http.py                # HTTP клиент с поддержкой аутентификации
├── exceptions.py          # Иерархия исключений API
├── config.py              # Класс-конфигурация для настройки параметров
└── modules/               # Папка с модулями API
    ├── __init__.py
    ├── base.py            # Базовый класс для всех модулей
    ├── payments.py        # Модуль для работы с платежами
    ├── finances.py        # Модуль для работы с финансами
    ├── auth.py            # Модуль для аутентификации
    ├── users.py           # Модуль для работы с пользователями
    ├── transactions.py    # Модуль для работы с транзакциями
    └── currencies.py      # Модуль для работы с валютами
```

## Использование

### Инициализация с существующим токеном

```python
import asyncio
from gengine_client import GEngineClient

async def main():
    # Создаем клиент с существующим токеном
    async with GEngineClient(
        base_url="https://api.example.com/api/v2",
        jwt_token="your-jwt-token",
        timeout=30,
        max_retries=3
    ) as client:
        # Используем API
        user_info = await client.users.get_me()
        print(f"Текущий пользователь: {user_info['login']}")

asyncio.run(main())
```

### Получение нового токена

```python
import asyncio
from gengine_client import GEngineClient

async def main():
    # Создаем клиент без токена
    async with GEngineClient(
        base_url="https://api.example.com/api/v2",
        timeout=30,
        max_retries=3
    ) as client:
        # Аутентифицируемся и получаем токен
        token_info = await client.auth.login(
            login="user@example.com",
            password="secure_password"
        )
        
        # Получаем токен
        token = token_info["access_token"]
        print(f"Получен токен: {token}")
        
        # Обновляем токен в клиенте
        client.update_token(token)
        
        # Используем API
        user_info = await client.users.get_me()
        print(f"Текущий пользователь: {user_info['login']}")

asyncio.run(main())
```

### Использование прокси

Клиент поддерживает работу через прокси, включая SOCKS5:

```python
import asyncio
from gengine_client import GEngineClient

async def main():
    # Создаем клиент с использованием SOCKS5 прокси
    async with GEngineClient(
        base_url="https://api.example.com/api/v2",
        jwt_token="your-jwt-token",
        timeout=60,  # Увеличиваем таймаут для прокси
        max_retries=5,  # Увеличиваем количество повторных попыток
        proxy="socks5://user:pass@host:port"  # Адрес SOCKS5 прокси
    ) as client:
        # Используем API через прокси
        user_info = await client.users.get_me()
        print(f"Текущий пользователь: {user_info['login']}")
        
        # Можно изменить настройки прокси на лету
        client.update_proxy("socks5://another-host:port")
        
        # Или отключить прокси
        client.update_proxy(None)

asyncio.run(main())
```

### Использование класса-конфигурации

Класс-конфигурация позволяет настроить параметры клиента один раз и затем использовать их многократно:

```python
import asyncio
from gengine_client import GEngineConfig

async def main():
    # Настройка параметров клиента
    GEngineConfig.setup(
        base_url="https://api.example.com/api/v2",
        jwt_token="your-jwt-token",
        timeout=30,
        max_retries=3,
        proxy="socks5://127.0.0.1:9050"  # Опционально - прокси
    )
    
    # Получение глобального экземпляра клиента
    client = await GEngineConfig.get_client()
    
    # Использование клиента
    user_info = await client.users.get_me()
    print(f"Текущий пользователь: {user_info['login']}")
    
    # Не нужно закрывать клиент при каждом использовании,
    # так как он хранится глобально
    
    # В другой части приложения
    # Получение того же экземпляра клиента
    client = await GEngineConfig.get_client()
    
    # Использование клиента
    balance = await client.users.get_balance()
    print(f"Баланс: {balance['balance']} {balance['currency']}")
    
    # Обновление настройки прокси в конфигурации
    await GEngineConfig.update_proxy(None)  # Отключение прокси
    
    # При завершении приложения
    await GEngineConfig.reset()  # Закрывает глобальный клиент

asyncio.run(main())
```

### Загрузка конфигурации из переменных окружения

```python
import asyncio
import os
from gengine_client import GEngineConfig

# Установка переменных окружения
os.environ["GENGINE_BASE_URL"] = "https://api.example.com/api/v2"
os.environ["GENGINE_TOKEN"] = "env_jwt_token"
os.environ["GENGINE_TIMEOUT"] = "45"
os.environ["GENGINE_MAX_RETRIES"] = "5"
os.environ["GENGINE_PROXY"] = "socks5://127.0.0.1:9050"  # Опционально - прокси

async def main():
    # Загрузка настроек из переменных окружения
    GEngineConfig.load_from_env()
    
    # Получение клиента с настройками из переменных окружения
    client = await GEngineConfig.get_client()
    
    # Использование клиента
    # ...
    
    # При завершении приложения
    await GEngineConfig.reset()

asyncio.run(main())
```

### Работа с платежами

```python
import asyncio
import uuid
from decimal import Decimal
from gengine_client import GEngineClient

async def main():
    async with GEngineClient(
        base_url="https://api.example.com/api/v2",
        jwt_token="your-jwt-token"
    ) as client:
        # Генерируем уникальный идентификатор транзакции
        transaction_id = str(uuid.uuid4())
        
        # Создаем и верифицируем платеж
        payment = await client.payments.verify(
            transaction_id=transaction_id,
            service_id=1,
            account="user123",
            amount=Decimal("10.99"),
            currency="USD"
        )
        print(f"Создан платеж: {payment['transaction_id']}")
        
        # Выполняем платеж
        result = await client.payments.execute(transaction_id=transaction_id)
        print(f"Статус платежа: {result['status_code']}")
        
        # Получаем статус платежа
        status = await client.payments.get_status(transaction_id=transaction_id)
        print(f"Текущий статус платежа: {status['status_code']}")

asyncio.run(main())
```

## Примеры

В репозитории есть примеры использования клиента с разными сценариями:

- `examples.py` - полный набор примеров использования, включая работу с прокси
- `old_examples/` - директория с устаревшими примерами

## Зависимости

- Python 3.7+
- aiohttp >= 3.8.0
- typing-extensions >= 4.0.0
- aiohttp-socks >= 0.7.1 (для поддержки SOCKS5 прокси)

## Лицензия

MIT
