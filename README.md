# 💻💚 Coder-Poster | От блога до IT-соцсети 

<div align="center">
  <img src="https://drive.google.com/thumbnail?id=1ozACcT_38eK7Pv4pMIbctpvEy0N2YsK0&sz=w500" alt="Coder-Poster Preview" width="700">
  
  ![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
  ![Redis](https://img.shields.io/badge/Redis-%23DD0031?logo=redis)
  ![OAuth](https://img.shields.io/badge/OAuth-2.0-EB5424?logo=auth0)
</div>

---

## ✨ **Концепция**
> "Каждый уважающий себя программист когда-нибудь пишет блог... но что если пойти дальше?"

**Coder-Poster** начинался как типичный сайт IT-постов, но его судьба — стать полноценной **IT-соцсетью**. 

- 🐣 **Сейчас**: Простая платформа для постов/мемов
- 🚀 **Планы**: Чат, подписки, live-кодинг, система рейтингов
- 🔥 **Философия**: От `print("Hello World")` до сложных фич — эволюция в действии!

---

## 🛠 **Технологический стек**
| Категория       | Технологии                                                                 |
|----------------|---------------------------------------------------------------------------|
| **🐍Backend**    | Django 5.2.4                                                             |
| **🗃️База данных**| PostgreSQL                                                               |
| **⚡Кеш**       | Redis                                                                    |
| **🔐Аутентификация** | OAuth 2.0 (GitHub, Google)                                           |
| **🎨Фронт**     | HTML5, CSS3, немного JS для анимаций                                     |

---
## 🌱 Почему стоит следить за проектом?

- **Эволюция на глазах** — от простого блога до IT-соцсети с реальными фичами  
- **Open-Source** — все этапы разработки открыты, можно учиться на живом примере  
- **Гибкая архитектура** — Django + PostgreSQL + Redis = масштабируемость  
- **Сообщество** — буду добавлять фичи по запросам пользователей  
- **Для портфолио** — отличный кейс, как развивать проект с нуля  

---

## 📸 **Скриншоты**
<div align="center">
  <img src="https://drive.google.com/thumbnail?id=1uqlmfcSRqJ82Qihqq_7gwEmrW7-dUF5S&sz=w500" alt="Coder-Poster Preview" width="500">
  <img src="https://drive.google.com/thumbnail?id=10ShveSJpRvmpKRwLbVAkXRonUNuQuSNG&sz=w500" alt="Coder-Poster Preview" width="500">
  <img src="https://drive.google.com/thumbnail?id=173ycvUWKuCGFSXsD-L86GnwXNthc-cUY&sz=w500" alt="Coder-Poster Preview" width="500">
  <img src="https://drive.google.com/thumbnail?id=1iZB5dVInIA6UjqmFGFeJA0N1BjWKKomP&sz=w500" alt="Coder-Poster Preview" width="500">
</div>

---
## 🚧 Roadmap 2024-2025

### Q3 2025
- [x] Базовый функционал постов  
- [ ] OAuth-авторизация (GitHub, Google)
- [ ] Реакции (лайки/дизлайки/💀)  

### Q4 2025
- [ ] Лента подписок    
- [ ] Теги и поиск
- [ ] Система комментариев с markdown

### 2026
- [ ] Вебсокет-чат между пользователями  
- [ ] Система рейтингов и достижений  
- [ ] API для мобильного приложения  

---

## 🚀 Как запустить проект локально?

### 0️⃣ Подготовка (обязательно!)
Убедитесь, что у вас установлены:
- Python 3.10+
- PostgreSQL (или SQLite для теста)
- Redis (для кеширования)


#### Для Linux (Ubuntu/Debian):
sudo apt update
sudo apt install python3 python3-pip postgresql redis-server

#### Для Windows:
#### Скачайте PostgreSQL и Redis с официальных сайтов

### 1️⃣ Клонирование и настройка окружения

#### 🟢 Клонируем репозиторий
git clone https://github.com/Tami555/Coder_Poster.git
cd coder-poster
#### 🟢 Создаём виртуальное окружение (обязательно!)
python -m venv venv

#### 🟢 Активируем его:
#### Linux/Mac:
source venv/bin/activate
#### Windows:
.\venv\Scripts\activate

### 2️⃣ Настройка зависимостей и переменных
#### 🟢 Устанавливаем зависимости

pip install -r requirements.txt

#### 🟢 Копируем пример .env файла (и редактируем под себя!)
cp .env.example .env

### 3️⃣ Настройка базы данных и Redis
#### 🟢 Для PostgreSQL:

sudo service postgresql start

psql -c "CREATE DATABASE ваша_бд;"

psql -c "CREATE USER ваш_юзер WITH PASSWORD 'ваш_пароль';"

psql -c "GRANT ALL PRIVILEGES ON DATABASE ваша_бд TO ваш_юзер;"


#### 🟢 Для Redis (кеширование):

sudo service redis-server start
##### Если Redis не работает, можно временно использовать заглушку в settings.py:
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

### 4️⃣ Запуск проекта
bash
#### 🟢 Применяем миграции
python manage.py migrate

#### 🟢 Создаём суперпользователя (по желанию)
python manage.py createsuperuser

#### 🟢 Заполняем БД данными
python manage.py loaddata fixtures/db.json

### 5️⃣ Запускаем сервер 
python manage.py runserver

### 💻 Откройте в браузере:  http://127.0.0.1:8000

## 🤝 Хочешь помочь проекту?
### 🟢 Форкни репозиторий
### 🟢Создай ветку:
git checkout -b feature/your-feature
### 🟢Закоммить:
git commit -m "Add: ваша супер-фича"
### Отправь PR — обсудим!