# simple_blog_api

Веб-сервис с использованием фреймворка FastAPI. API мини-блога, в котором вы можете создавать пользователей, посты, лайкать и дизлайкать их. Все созданные эндпоинты задокументированы на /docs/, для некоторых эндпоинтов необходимо авторизоваться и получить токен. Его можно получить на эндпоинте /users/token/

## Как запустить

### Клонируйте код
```
git clone https://github.com/EshiNanase/simple_blog_api.git
```

### Создайте .env файл со следующими переменными окружения

- `POSTGRES_DB` — название базы данных Postgres.
- `POSTGRES_USER` — имя юзера для входа в базу данных Postgres.
- `POSTGRES_PASSWORD` — пароль для входа под именем юзера сверху.

### Соберите образ Docker
```
docker compose build
```

### Запустите Docker
```
docker compose up
```

### Откройте сайт в браузере

Вы можете работать с API, пользуясь пользовательским интерфейсом Swagger. Он находится по ссылке:
```
http://127.0.0.1:8000/docs/
```
