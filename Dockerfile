# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN python3 -m venv venv
RUN ./venv/bin/pip install -r requirements.txt

# Устанавливаем переменную окружения для работы с виртуальным окружением
ENV PATH="/app/venv/bin:$PATH"

# Открываем порт для приложения (если это веб-сервер)
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "start.py"]
