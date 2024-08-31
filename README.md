# Сервис объявлений на FastAPI

Этот проект представляет собой учебный сервис объявлений, разработанный с использованием FastAPI и PostgreSQL. Проект создан в рамках курса по Python веб-разработке.

## Описание задания

https://github.com/netology-code/py-homeworks-web/tree/new/3.1-fast-api-1

## Функциональность

- Создание объявлений
- Получение объявления по ID
- Обновление объявлений
- Удаление объявлений
- Поиск объявлений по различным параметрам

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Установка и запуск

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/JuliiaZhuravleva/fastapi-ads-service.git
   ```

2. Создайте файл `.env` в корневой директории проекта и заполните его следующим образом:
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. Запустите проект с помощью Docker Compose:
   ```
   docker-compose up --build
   ```

4. Приложение будет доступно по адресу `http://localhost:8000`

## API Endpoints

- `POST /advertisement`: Создание нового объявления
- `GET /advertisement/{advertisement_id}`: Получение объявления по ID
- `PATCH /advertisement/{advertisement_id}`: Обновление объявления
- `DELETE /advertisement/{advertisement_id}`: Удаление объявления
- `GET /advertisement`: Поиск объявлений (с параметрами запроса)

## Тестирование

Для тестирования API можно использовать скрипт `client.py`, который находится в корневой директории проекта.