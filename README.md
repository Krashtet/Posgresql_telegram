# Telegram Bot с PostgreSQL

Простой Telegram бот, который сохраняет информацию о пользователях в базу данных PostgreSQL.

## Структура проекта

```
Posgresql_telegram/
├── main.py          # Основной файл бота
├── database.py      # Работа с базой данных
├── config.py        # Конфигурация и переменные окружения
├── requirements.txt # Зависимости Python
├── .env            # Переменные окружения (не коммитить!)
└── README.md       # Этот файл
```

## Установка и настройка

### 1. Установка PostgreSQL

**Windows:**
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Запустите установщик и следуйте инструкциям
3. Запомните пароль для пользователя `postgres`

**Альтернатива - Docker:**
```bash
docker run --name postgres-bot -e POSTGRES_PASSWORD=yourpassword -d -p 5432:5432 postgres
```

### 2. Установка pgAdmin (опционально)

1. Скачайте pgAdmin с https://www.pgadmin.org/download/
2. Установите и настройте подключение к вашей базе данных

### 3. Создание базы данных

Подключитесь к PostgreSQL и создайте базу данных:
```sql
CREATE DATABASE telegram_bot_db;
```

### 4. Установка зависимостей Python

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Отредактируйте файл `.env`:
```
BOT_TOKEN=ваш_токен_бота_из_BotFather
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telegram_bot_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль_от_postgres
```

### 6. Запуск бота

```bash
python main.py
```

## Функции бота

- `/start` - Начать работу с ботом и сохранить информацию о пользователе
- `/help` - Показать список команд
- `/myinfo` - Показать информацию о пользователе из базы данных
- `/stats` - Показать количество пользователей в базе данных

## База данных

Бот создает таблицу `users` со следующей структурой:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Безопасность

- Никогда не коммитьте файл `.env` в репозиторий
- Используйте сильные пароли для базы данных
- Рассмотрите использование переменных окружения системы вместо `.env` файла в продакшене

## Дальнейшее развитие

- Добавить больше команд и функций
- Реализовать систему ролей пользователей
- Добавить логирование в базу данных
- Создать админ-панель для управления пользователями 