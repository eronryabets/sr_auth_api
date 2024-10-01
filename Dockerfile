# Базовый образ
FROM python:3.10-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Скопируем requirements.txt и установим зависимости
# Сначала копируется файл requirements.txt в рабочую директорию контейнера.
# Затем устанавливаются все зависимости, указанные в этом файле, с помощью pip.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все файлы проекта в контейнер
COPY . /app/

# Открываем порт 8000 для доступа к приложению из контейнера.
EXPOSE 8000

# Команда для запуска Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "sr_auth_api.wsgi:application"]