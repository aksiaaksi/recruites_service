# Recruitment Service


[Recruitments-service](https://recruitments-service.herokuapp.com/rservice/)


Перечень необходимых файлов для взаимодействия с Heroku:

* runtime.txt: язык программирования и его версию.
* requirements.txt: необходимые для Python компоненты, включая Django.
* Procfile: Список процессов, которые будут выполнены для старта веб-приложения. Для Django это обычно сервер веб-приложений Gunicorn (скрипт .wsgi).
wsgi.py: конфигурация WSGI для вызова нашего приложения Django в окружении Heroku.


Описание процесса  создания и загрузки на сервис Heroku:
1) Необходимо установить клиент Heroku;
2) Авторизируемся на сервесе Heroku: heroku authorizations
3) Создаем приложение при помощи клиента Heroku: heroku create recruitments-service
4) Отправляем приложение в репозитарий Heroku: git push heroku master
5) Производим настройку таблиц БД: heroku run python manage.py migrate
6) Создаем суперпользователя: heroku run python manage.py createsuperuser
7) Открываем приложение: heroku open     