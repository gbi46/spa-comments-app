FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN django-admin startproject app .

COPY . .

# Запуск приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
