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

- 🐣 **Сейчас**: Простая платформа для постов/мемов. Версия v.1.
- 🚀 **Планы**: Чат, подписки, live-кодинг, система рейтингов
- 🔥 **Философия**: От `print("Hello World")` до сложных фич — эволюция в действии!

---

## 🛠 **Технологический стек**
| Категория       | Технологии                                                                 |
|----------------|---------------------------------------------------------------------------|
| **🐍Backend**    | Django 5.2.4                                                             |
| **🗃️База данных**| PostgreSQL                                                               |
| **⚡Кеш**       | Redis
| **🐇Брокер**       | RabbitMQ
| **🥬Задачи в фоне** | Celery                                                                     |
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
## 🚧 Roadmap

### версия v.1
- [x] Базовый функционал постов  
- [x] OAuth-авторизация (GitHub, Google)
- [x] Теги и поиск
- [x] Базовая проверка постов на цензурность (используем Celery)

### версия v.2
- [X] Реакции (лайки/дизлайки/❤️)   
- [ ] Лента подписок
- [ ] Проверка постов на благиат
- [ ] Система комментариев с markdown

### версия v.3
- [ ] Вебсокет-чат между пользователями  
- [ ] Система рейтингов и достижений  
- [ ] API для мобильного приложения  

---

## 🚀 Как запустить проект локально?

### 0️⃣ Подготовка (обязательно!)
- Установите Docker Desktop
- Больше ничего не требуется! Docker сам установит PostgreSQL, Redis и всё остальное

### 1️⃣ Клонирование и настройка окружения

#### 🟢 Клонируем репозиторий
git clone https://github.com/Tami555/Coder_Poster.git
cd coder-poster
#### 🟢 Запускаем все сервисы одной командой!
docker-compose up -d

### 2️⃣ Настройка базы данных
#### 🟢 Подключаемся к контейнеру Django

docker-compose exec django python manage.py migrate

#### 🟢 Загружаем тестовые данные (опционально)
docker-compose exec django python manage.py loaddata fixtures/db.json

#### 🟢 Создаём суперпользователя (опционально)
docker-compose exec django python manage.py createsuperuser

### 3️⃣ Доступ к сервисам
После запуска откройте в браузере:
- 🚀 Основное приложение: http://localhost:8000
- 📊 Adminer (управление БД): http://localhost:8080
- 📈 Flower (мониторинг задач): http://localhost:5555

### 4️⃣ Управление контейнерами
#### 🟢 Остановить все сервисы:
docker-compose down

#### 🟢 Перезапустить конкретный сервис:
docker-compose restart djangor

#### 🟢 Просмотр логов:
docker-compose logs -f django

#### 🟢 Проверить статус всех контейнеров:
docker-compose ps

## 🛠️ Доступные сервисы в Docker:
- django - основное приложение на Django
- postgresql - база данных PostgreSQL
- redis - кеширование и брокер для Celery
- rabbit - очередь сообщений для Celery
- celery_worker - обработка фоновых задач
- flower - мониторинг задач Celery
- adminer - веб-интерфейс для управления БД

## 🤝 Хочешь помочь проекту?
### 🟢 Форкни репозиторий
### 🟢Создай ветку:
git checkout -b feature/your-feature
### 🟢Закоммить:
git commit -m "Add: ваша супер-фича"
### Отправь PR — обсудим!