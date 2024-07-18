# Техническое задание для [О-комплекс](https://hh.ru/employer/5454644?hhtmFrom=vacancy)

## Выполненые задачи

1. Получение прогноза погода для пользователя
2. контейнерезация
3. тесты
4. автодополнение
5. возможность смотртеь последний запрос погоды
6. API для получения списка город, которые запрашивали
7. Сохранение истории запросов пользователя

## Используемые технологии в проекте:

[![Python][Python-badge]][Python-url]

[![Django][Django-badge]][Django-url]

[![Docker][Docker-badge]][Docker-url]

## Установка и работа.

1. Клоним репозиторй через ssh или https

```
git clone <ключ или ссылка>
```
2. Инсталим и разворачиваем виртуальное окружение
```
pythom -m venv venv
```
```
source venv/Scripts/activate
```

3. Инсталим зависимости из requirements.txt
```
pip install -r requirements.txt
```

4. Создаем модуль .env и копируем в него содержимое из .env.example

5. Выполнить миграции из директории с модулем manage.py
```
python manage.py migrate
```
6. запуск localhost
```
python manage.py runserver
```

7. перейти по адресу http://127.0.0.1:8000/users/register/ для регистрации и двигаться по навигации.

## Работа с API

Документацию можно посмотреть по адресу http://127.0.0.1:8000/swagger-ui/ (локалхост должен быть поднят)

Там же можно отправить запросы на api эндпоинты

## Docker

Сначала в .env необходимо DEBUG константу изменить на False, что бы в settings.py подтянулись конфиги для postgres вместо sqlite

Для работы с контейнерами перейдите в директорию infra/ 

При первом запуске для инициализации образов

```
docker compose -f docker-compose.dev.yaml up --build -d
```

в дальнейшем 

```
docker compose -f docker-compose.dev.yaml up  -d
```

Когда контейнеры успешно будут запущены необходимо собратить статику и выполнить миграции

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py collectstatic
```

```
docker compose -f docker-compose.dev.yaml exec backend sh -c "cp -r /app/collected_static/. /backend_static/static/"
```

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py migrate
```

## Тесты

На уровне модуля manage.py
```
python manage.py test
```

из контейнера

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py test
```





<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/downloads/release/python-3110/

[Python-badge]: https://img.shields.io/badge/python-v3.11-yellow?style=for-the-badge&logo=python

[Django-url]: https://docs.djangoproject.com/en/4.2/releases/4.2.6/

[Django-badge]: https://img.shields.io/badge/Django-v4.2.6-008000?logo=django&style=for-the-badge

[Docker-url]: https://www.docker.com/

[Docker-badge]: https://img.shields.io/badge/docker-red?style=for-the-badge&logo=docker

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgresql-gray?style=for-the-badge&logo=postgresql
