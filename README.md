# ClickCheck Project

Проект визового центра на Django с использованием **Django Channels**, **Daphne**, и **Redis** для поддержки WebSocket и чата в реальном времени. Для проксирования и обслуживания статических файлов используется **Nginx**.

## Требования

- **Python** 3.9 или выше
- **Redis** сервер (для поддержки WebSocket и каналов)
- **Daphne** (для обработки запросов WebSocket)
- **Nginx** (для обслуживания статических файлов и обратного проксирования)
- Виртуальное окружение для Python (рекомендуется)

## Установка

### 1. Клонируйте репозиторий

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone <URL вашего репозитория>
cd Visa4u_project
```

### 2. Создайте виртуальное окружение

Создайте и активируйте виртуальное окружение для изоляции зависимостей:

```bash
python3 -m venv venv
source venv/bin/activate  # Для MacOS и Linux
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройка Redis

Redis требуется для работы с каналами Django. Убедитесь, что Redis установлен и запущен:

# На MacOS с использованием Homebrew
```bash
brew install redis
brew services start redis
```

Проверьте, что Redis запущен:
```bash
redis-cli ping
```

Ожидаемый ответ: PONG

### 5. Настройка Daphne

Daphne используется для обработки WebSocket-соединений. Убедитесь, что Daphne установлена:

```bash
pip install daphne
```

### 6. Настройка Nginx

Nginx используется для обратного проксирования и обслуживания статических файлов. Пример конфигурации Nginx находится в config/nginx.conf.

Установите Nginx:
```bash
brew install nginx  # Для MacOS
```

Скопируйте файл конфигурации Nginx из config/nginx.conf в основную директорию конфигурации Nginx:
```bash
sudo cp config/nginx.conf /opt/homebrew/etc/nginx/nginx.conf  # Укажите правильный путь при необходимости
```

Перезапустите Nginx для применения изменений:
```bash
sudo nginx -s reload
```

### 7. Соберите статические файлы для обслуживания их через Nginx:

```bash
python manage.py collectstatic
```

### 8. Примените миграции базы данных

```bash
python manage.py migrate
```

### 9. Запустите Daphne

```bash
daphne -p 8001 Visa4u.asgi:application
```

