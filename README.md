# 🏔️ API для отправки данных о горных перевалах (SQLite Edition) 

## 🎯 Задача проекта 
Система позволяет туристам отправлять информацию о покорённых перевалах через мобильное приложение.
Данные передаются на сервер, сохраняются в БД (SQLite), проходят модерацию сотрудниками ФСТР.
## ✅ Реализовано 
- REST API на Django REST Framework 
- - **SQLite** — лёгкая встраиваемая БД, идеальна для разработки 
- - Методы: 
- - `POST /api/submitData` — создание новой записи 
- - `GET /api/submitData/<id>` — получение записи по ID 
- - `PATCH /api/submitData/<id>` — редактирование (только если статус `new`) 
- - `GET /api/submitData/?user__email=...` — список записей пользователя 
- - Админ-панель Django для модерации статусов 
- - Валидация email и телефона 
- - Хранение изображений как файлов 
- - Тесты на pytest 
- - Документация Swagger (`http://localhost:8000/swagger/`) 
- - Поддержка Docker 
- 
- --- 
- 
- ## 🧩 Установка и запуск (локально) 
- 
- ### 1. Клонирование и зависимости 
- ```bash 
- git clone https://github.com/Northwest3246/pereval1 
- cd fstr-drf-api 
- pip install -r requirements.txt
- ### 2. Настройка окружения
- Создай .env файл:

- SECRET_KEY=your_secret_key_here 
- DEBUG=True 
- ALLOWED_HOSTS=localhost,127.0.0.1,*
- ### 3. Миграции и запуск
- python manage.py makemigrations 
- python manage.py migrate 
- python manage.py createsuperuser 
- python manage.py runserver

🐳 Запуск с Docker
- docker-compose up --build

🌐 API Endpoints
- (описания как выше — с примерами JSON)

📚 Swagger

- http://localhost:8000/swagger/

🧪 Тесты

- pytest passes/tests/ -v --cov=passes

👨‍💻 Автор

- Дмитрий П.