# NIR Cloud

Облачное файловое хранилище для бакалаврской ВКР. Локальный прототип разрабатывается для браузера. В следующем семестре Telegram-бот и MAX-бот будут подключаться к тому же серверному API.

## Локальный запуск FastAPI и PostgreSQL в Linux

Откройте терминал в папке проекта. Если файла `.env` ещё нет, создайте его из примера и замените `POSTGRES_PASSWORD` на пароль для локальной базы.

```bash
cp .env.example .env
```

Затем выполните команды запуска и проверки.

```bash
docker compose up --build -d --wait --wait-timeout 60
docker compose ps
curl -i http://127.0.0.1:8000/health
```

Сохраните значения `POSTGRES_DB`, `POSTGRES_USER` и `POSTGRES_PASSWORD` для последующих запусков с тем же томом. Образ PostgreSQL использует их для создания базы и роли при первом запуске с пустым томом. [Переменные окружения PostgreSQL](https://hub.docker.com/_/postgres/#environment-variables).

- [Интерактивная документация API](http://127.0.0.1:8000/docs) открывается в браузере. В ней можно выполнить `GET /health`.
- `/health` выполняет `SELECT 1` в PostgreSQL. При успешном запросе API возвращает HTTP `200` и `{"status":"ok","database":"ok"}`. При недоступности базы ответ содержит HTTP `503`.
- Если порт `8000` занят, измените `API_PORT` в `.env` и подставьте новый порт в адрес.

Compose запускает API после прохождения проверки готовности PostgreSQL. Именованный том `postgres_data` хранит данные базы, а `file_data` смонтирован в `/data/uploads` для содержимого файлов. `docker compose down` останавливает и удаляет контейнеры с сохранением обоих томов. [Порядок запуска в Docker Compose](https://docs.docker.com/compose/how-tos/startup-order/), [официальный образ PostgreSQL](https://hub.docker.com/_/postgres/).

## Материалы

- [Архитектурная схема и черновая ER-диаграмма](docs/architecture.md)
- [Фактические результаты проверок](docs/testing.md)
