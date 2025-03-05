# README #

Описание проекта
Приложение позволяет пользователям оставлять комментарии, загружать файлы и взаимодействовать с записями. Данные хранятся в реляционной базе данных, используется Django (backend) и Vue/React (frontend).

Стек технологий
Backend: Django, Django ORM, Django REST Framework
Frontend: Vue / React
База данных: PostgreSQL / MySQL / SQLite
Кеширование и очереди: Redis / RabbitMQ
Контейнеризация: Docker, Docker Compose
Аутентификация: JWT
Веб-сокеты: WebSockets (Django Channels)

Регистрация и аутентификация пользователей
✅ Добавление комментариев с поддержкой ответов (дерево комментариев)
✅ Фильтрация и сортировка комментариев
✅ Загрузка изображений (JPG, PNG, GIF ≤ 320×240) и текстовых файлов (TXT ≤ 100 KB)
✅ CAPTCHA для защиты от ботов
✅ Предпросмотр сообщения перед отправкой
✅ Валидация данных на клиенте и сервере
✅ Защита от XSS-атак и SQL-инъекций
✅ Разбиение комментариев по страницам (по 25 сообщений)
✅ API для работы с комментариями

Развертывание проекта
1. Клонирование репозитория

git clone https://github.com/username/comment-app.git
cd comment-app

2. Запуск с Docker

docker-compose up --build -d
Открыть в браузере: http://localhost:8000

Структура проекта

comment-app/
│── backend/            # Django backend
│   ├── api/            # API для работы с комментариями
│   ├── auth/           # Аутентификация
│   ├── models/         # Модели БД
│   ├── serializers/    # Django REST Framework сериализаторы
│   ├── views/          # Представления API
│   ├── templates/      # HTML-шаблоны (если нужен SSR)
│   ├── static/         # Статика (CSS, JS, изображения)
│   ├── tests/          # Тесты API
│   └── manage.py
│
│── frontend/           # Статический фронтенд
│   ├── css/            # Стили
│   │   ├── styles.css  # Основной файл стилей
│   │   ├── reset.css   # Сброс стилей
│   │   └── theme.css   # Цветовые темы
│   │
│   ├── js/             # JavaScript файлы
│   │   ├── main.js     # Основной JS
│   │   ├── api.js      # Запросы к API
│   │   ├── ui.js       # UI-эффекты (анимации, модалки)
│   │   └── validation.js # Валидация форм
│   │
│   ├── img/            # Изображения (иконки, логотипы)
│   │   ├── logo.png
│   │   └── bg.jpg
│   │
│   ├── index.html      # Главная страница с комментариями
│   ├── form.html       # Страница формы добавления комментария
│   ├── preview.html    # Предпросмотр комментария
│   ├── error.html      # Страница ошибки
│
│── docker/             # Docker-файлы
│── .gitignore
│── docker-compose.yml
│── README.md
│── requirements.txt    # Python-зависимости
