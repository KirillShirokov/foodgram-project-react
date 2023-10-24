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
После первого деплоя, для заполнения БД ингредиентами необходимо на удаленном сервере из директории *foodgram/infra* выполнить команду:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py csv_loader
```
## Справка
- Nginx сервера можно проверить командой:
```
sudo nano /etc/nginx/sites-enabled/default

```
```
server {
    server_name <Имя_вашего_домена.домен>;

    location / {
        client_max_body_size 20M;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-Proto $scheme;
        proxy_pass              http://127.0.0.1:здесь_указать_порт_контейнера_nginx;
    }

#Ниже код, созданный автоматически Cerbot при получении сертификата SSL

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/foodcat-yandex.ddns.net/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/foodcat-yandex.ddns.net/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}


server {
    if ($host = foodcat-yandex.ddns.net) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    server_name 158.160.22.151 foodcat-yandex.ddns.net;
    listen 80;
    return 404; # managed by Certbot


}

```
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
