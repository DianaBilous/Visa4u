# Базовый образ
FROM python:3.9-slim

# Установим рабочую директорию
WORKDIR /app

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установим зависимости из requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем проект
COPY . .

# Установим Django secret key и настройки
ENV PYTHONUNBUFFERED 1

# Открываем порт 8001 (для работы daphne)
EXPOSE 8001

# Запуск приложения с использованием Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "Visa4u.asgi:application"]

