# указываем базовый образ, который будет использоваться
# для установки зависимостей
FROM python:3.14-slim-bookworm AS builder

ARG EXTRA_GROUPS=""

#создаём и устанавливаем рабочую директорию
RUN mkdir app
WORKDIR /app

# TODO: нужно скопировать файлы, которые содержат список зависимостей

# устанавливаем зависимости из скопированных файлов
RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-root --only main \
  ${EXTRA_GROUPS:+--only $EXTRA_GROUPS} \
  --no-interaction --no-ansi \
  && rm -rf $(poetry config cache-dir)/{cache,artifacts}
# в результате выполнения данной команды будет созданно виртуальное окружение
# в папке /app/.venv В это окружение будут поставлены все зависимости

# указываем какой образ использоваться в качестве рабочего
FROM python:3.14-slim-bookworm AS runtime

# TODO: нужно скопировать содержимое папки /app из слоя builder
# в слой runtime в папку /app


WORKDIR /app

# TODO: необходимо изменить переменную PATH. Почитайте за что она отвечает.
# В переменную PATH необходимо вставить в начало путь до python
# в окружении /app/.venv/

ENV PYTHONPATH=./
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
RUN unset PYTHONHOME

# В самую последнюю очередь копируем исходный код из папки
# src в папку src в образе
COPY src/ ./src/

ENTRYPOINT [ "python" ]
CMD ["-m",\
  "uvicorn",\
  "src.main:app",\
  "--host", "0.0.0.0",\
  "--port", "5000" ]
