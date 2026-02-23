# Test Assignment OneSimple

**Test Assignment OneSimple** - тестовое задание по реализации сервиса на **Django + DRF**, который синхронизирует контент из Instagram в локальную базу данных и позволяет управлять комментариями через API.

## Оглавление

- [Основные технологии](#основные-технологии)
- [Структура проекта](#структура-проекта)
- [Установка и запуск](#установка-и-запуск)
- [Примеры работы с API](#примеры-работы-с-api)
- [Запуск тестов](#запуск-тестов)
- [Автор](#автор)

## Основные технологии
- Python 3.14
- Django 5.2.11
- Django REST Framework 3.16.1
- Requests 2.32.5 - HTTP-запросы
- Pydantic 2.12.5 - валидация данных и сериализация
- pytest + pytest-django + requests-mock - тестирование


## Структура проекта
```
test-assignment-onesimple
│  instagram_sync/                # Django-проект
│  ├─ api/                        # Каталог приложения
│  │  │  ├─ clients/              # Каталог с клиентами
│  │  │  ├─ api_client.py         # Клиент для работы с Instagram Graph API
│  │  │  ├─ exceptions.py         # Кастомные исключения для клиента
│  │  │  └─ schemas.py            # Pydantic схемы для валидации данных клиента
│  │  ├─ migrations/              # Каталог с миграциями базы данных
│  │  │  ├─ 0001_initial.py       # Начальная миграция базы данных
│  │  ├─ services/                # Каталог с сервисами
│  │  │  ├─ create_comment.py     # Сервис для создания комментариев к посту Instagram
│  │  │  └─ sync_posts.py         # Сервис для синхронизации постов Instagram
│  │  ├─ apps.py                  # Конфигурация приложения
│  │  ├─ models.py                # Модели базы данных
│  │  ├─ pagination.py            # Кастомная пагинация
│  │  ├─ serializers.py           # Сериализаторы
│  │  ├─ urls.py                  # Роутинг приложения
│  │  └─ views.py                 # Представления
│  ├─ instagram_sync/             # Конфигурация Django-проекта
│  │  ├─ asgi.py                  # ASGI конфигурация
│  │  ├─ settings.py              # Настройки проекта
│  │  ├─ urls.py                  # Роутинг проекта
│  │  └─ wsgi.py                  # WSGI конфигурация
│  ├─ tests/                      # Каталог с тестами
│  │  ├─ conftest.py              # Конфигурация тестового окружения
│  │  └─ test_comment.py          # Тесты для комментариев
│  ├─ Dockerfile                  # Контейнеризация проекта
│  ├─ entrypoint.sh               # Скрипт для выполнения миграций
│  ├─ manage.py                   # Django CLI
│  ├─ pytest.ini                  # Конфигурация pytest
│  └─ requirements.txt            # Зависимости Python
├─ .env.example                   # Шаблон переменных окружения
├─ .gitignore                     # Файлы/каталоги, игнорируемые git
├─ docker-compose.yml             # Конфигурация Docker для проекта
└─ README.md                      # Описание проекта, инструкции по запуску
```

## Установка и запуск
```bash
git clone https://github.com/aksianchuk/test-assignment-onesimple.git # Клонируйте репозиторий
cd test-assignment-onesimple                                          # Перейдите в каталог проекта
cp .env.example .env                                                  # Создайте и укажите настройки
docker-compose up --build                                             # Запустите контейнеры
```
Проект будет доступен по адресу:  
http://localhost:8000

## Примеры работы с API
### 1. Синхронизация постов из Instagram Graph API (POST)
```http
http://localhost:8000/api/sync/
```
**Пример успешного ответа:**
```json
{
  "message": "Синхронизация прошла успешно"
}
```

### 2. Список всех сохраненных постов из локальной базы данных (GET)
```http
http://localhost:8000/api/posts/
```
**Пример успешного ответа:**
```json
{
  "next": "http://localhost:8000/api/posts/?cursor=cD0yMDI2LTAyLTIxKzE5JTNBNTklM0E1NSUyQjAwJTNBMDA33D",
  "previous": null,
  "results": [
    {
      "id": 1,
      "children": [],
      "ig_id": "18340892314300765",
      "ig_media_type": "IMAGE",
      "ig_media_url": "https://cdninstagram.com/v/9219978297555024373_n.jpg",
      "ig_timestamp": "2026-02-23T17:04:56Z",
      "ig_caption": "Sample post caption",
      "ig_comments_count": 0,
      "ig_like_count": 10
    },
    {
      "id": 2,
      "children": [
        {
          "ig_id": "18127843645599789",
          "ig_media_type": "VIDEO",
          "ig_media_url": "https://cdninstagram.com/v/9212378297555024373_a.mp4",
          "ig_timestamp": "2026-02-21T19:59:52Z"
        },
        {
          "ig_id": "17901070667232606",
          "ig_media_type": "IMAGE",
          "ig_media_url": "https://cdninstagram.com/v/9212378297123424373_r.jpg",
          "ig_timestamp": "2026-02-21T19:59:53Z"
        }
      ],
      "ig_id": "17976677884825485",
      "ig_media_type": "CAROUSEL_ALBUM",
      "ig_media_url": "https://cdninstagram.com/v/9212376537123424373_r.jpg",
      "ig_timestamp": "2026-02-21T19:59:55Z",
      "ig_caption": null,
      "ig_comments_count": 2,
      "ig_like_count": 37
    }
  ]
}
```

### 3. Комментирование постов (POST)
```http
http://localhost:8000/api/posts/{id}/comment/
```
`{id}` - внутренний Primary Key поста в локальной базе данных.  

**Тело запроса:**  
```json
{
  "ig_text": "This is a sample comment for testing."
}
```

**Пример успешного ответа:**
```json
{
  "id": 1,
  "ig_id": "18127613083567499",
  "ig_text": "This is a sample comment for testing.",
  "post": 1
}
```

## Запуск тестов
Выполните команду:
```
docker compose exec backend pytest
```

## Автор
https://github.com/aksianchuk (Никита Оксенчук)