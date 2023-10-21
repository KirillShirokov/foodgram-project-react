# Foodgram
![FOODGRAM](https://github.com/KirillShirokov/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Если вы любите делиться вкусно поесть и делиться рецептами, то вы на правильном пути. Данный проект позволяет авторизованным пользователям публиковать рецепты с ваших любимых блюд. 
 Готовый проект можно посмотреть здесь
 https://foodcat-yandex.ddns.net

 **Данный репозиторий имеет два файла docker-compose.yml и docker-compose.production.yaml которые позволяют развернуть проект как на локальном, так и на удаленном сервере**


##  Установка и настройка проекта
**(Данное описание подразумевает, что на вашем сервере установлен Git, настроен фаерволл, безопасность и получен и настроен SSL -сертификат, пакетный менеджер npm, создана ветка на репозиторий https://github.com/KirillShirokov/foodgram-project-react/)**
### Подготовка сервера к установке проекта
- Склонируйте проект из репозитория
- Создайте файл .env в директории */infra* проекта и укажите в нем переменные указанные в .env.example
- Настройте виртуальное окружение
- Установите пакеты из файла requirements.txt
- Запустите Docker Compose 
- Выполните миграции и сбор статики
```
git clone https://github.com/<your_profile>/foodgram-project-react/
python3 -m venv venv
pip install -r requirements.txt
docker compose -f docker-compose.yml up
python manage.py migrate
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/

```
- Перезагрузите конфигурацию Nginx
```
sudo systemctl reload nginx
```
## CI/CD. Подготовка и настройка
- Перейдите в настройки репозитория — Settings, выберите на панели слева Secrets and Variables → Actions, нажмите New repository secret. Создайте ключи с именами: 
  - DOCKER_PASSWORD (Пароль от вашего докер хаба)
  - DOCKER_USERNAME (Ваш логин от докер хаба)
  - HOST (IP адресс вашего сервера)
  - SSH_KEY (SSH ключ вашего сервера)
  - SSH_PASSPHRASE (Пароль вашего сервера)
  - TELEGRAM_TO (Ваш ID в телеграм)
  - TELEGRAM_TOKEN (Токен вашего бота в телеграм)
  - USER (Логин вашего сервера)
- Замените в файле docker-compose.ptoduct.yml наименования образов в соответвии с вашим логином на DockerHub(Например your_name/kittygram_backend)
- Далее git add ./ git commit/ git push
Ваш Git Action проведет тесты, соберет образы и отправит их на репозиторий, задеплоит ваш проект на сервер и даже уведомит вас в стучае успеха в телеграм.

## Технологии:
**Docker Compose**
**Docker**
**GitHub Actions**
**Python**
**Django**
**Gunicorn**
**Nginx**
**Cerbot**
## Разработчик
Кирилл Широков
