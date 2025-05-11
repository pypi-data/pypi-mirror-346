# GEngineAPI

Асинхронный модульный клиент для взаимодействия с API G-Engine.

## Особенности

- Полностью асинхронный интерфейс на базе `aiohttp` и `asyncio`
- Модульная структура с разделением по доменам API
- Детальная обработка ошибок и исключений
- Автоматические повторные попытки для временных ошибок
- Поддержка JWT-аутентификации
- Поддержка прокси, включая SOCKS5
- Ферма клиентов с балансировкой нагрузки и стратегиями ротации
- Подробное логирование
- Строгая типизация с помощью аннотаций типов
- Класс-конфигурация для централизованной настройки и повторного использования

## Установка

```bash
pip install gengineapi
```

Для поддержки SOCKS5 прокси убедитесь, что установлен пакет `aiohttp-socks`:

```bash
pip install aiohttp-socks
```

## Использование

### Быстрый старт

```python
import os
import asyncio
import logging
from gengineapi import ClientFarm
from dotenv import load_dotenv

load_dotenv()

GTOKEN = os.getenv("GTOKEN")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("gengine")

gfarm = ClientFarm(logger=logger)

gfarm.create_config(name="base",
        base_url="https://b2b-api.ggsel.com/api/v2",
        jwt_token=GTOKEN,
        timeout=60,
        max_retries=5,
        proxy="socks5://username:password@host:port") # Прокси опциональные

async def main():
    client = await gfarm.get_client("base")

    async with client:
        me = await client.users.get_me()

        logger.info(me)


if __name__ == "__main__":
    asyncio.run(main())
```
### Инициализация с существующим токеном

```python
import asyncio
from gengineapi import GEngineClient

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
from gengineapi import GEngineClient

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
from gengineapi import GEngineClient

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
from gengineapi import GEngineConfig

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

### Использование фермы клиентов

Ферма клиентов позволяет управлять множеством клиентов с разными конфигурациями и стратегиями ротации:

```python
import asyncio
from gengineapi import ClientFarm

async def main():
    # Создаем ферму клиентов
    farm = ClientFarm()
    
    # Добавляем несколько конфигураций с разными прокси
    farm.create_config(
        name="client1",
        base_url="https://api.example.com/api/v2",
        jwt_token="token1",
        proxy="socks5://user1:pass1@host1:port1",
        tags=["group1", "production"]
    )
    
    farm.create_config(
        name="client2",
        base_url="https://api.example.com/api/v2",
        jwt_token="token2",
        proxy="socks5://user2:pass2@host2:port2",
        tags=["group1", "backup"]
    )
    
    # Устанавливаем стратегию выбора клиента
    farm.set_selection_strategy("round_robin")  # или "random", "least_errors", "least_recently_used"
    
    # Получаем клиент по имени
    client1 = await farm.get_client("client1")
    await client1.users.get_me()
    
    # Получаем следующий клиент согласно стратегии
    client = await farm.get_next_client()
    await client.currencies.get_rate(source="cb_rf", pair="USD:RUB")
    
    # Получаем клиент по тегу
    client = await farm.get_next_client(tag="production")
    await client.transactions.get_transactions(limit=5)
    
    # При завершении работы закрываем все клиенты
    await farm.close_all()

asyncio.run(main())
```

### Работа с платежами

```python
import asyncio
import uuid
from decimal import Decimal
from gengineapi import GEngineClient

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

## Доступные модули API

- `payments` - создание и выполнение платежей
- `finances` - работа с финансовыми данными
- `auth` - аутентификация и управление токенами
- `users` - работа с пользователями и их балансами
- `transactions` - работа с транзакциями
- `currencies` - работа с курсами валют

## Дополнительная документация

Ручки, которые дергаем - https://b2b-api.ggsel.com/api/v2/docs#

## Зависимости

- Python 3.7+
- aiohttp >= 3.8.0
- typing-extensions >= 4.0.0
- aiohttp-socks >= 0.7.1 (опционально, для поддержки SOCKS5 прокси)

## Лицензия

MIT
