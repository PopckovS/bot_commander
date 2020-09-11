#! /usr/bin/python3

from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response
from flask_sqlalchemy import SQLAlchemy

import requests
import config
import json
import sys
import os

# Добавляем путь к родительской директории
two_up = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(two_up)

# Импорт Моделей
from models.Telegram_User import Telegram_User
from models.Telegram_Projects import Telegram_Projects


# Создаем Сервре, и подключение к БД
app = Flask(__name__)

# Этот параметр создает подключение к БД
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECT_DB

# Этот параметр отслеживает изменение Моделей прямо во время работы приложения
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаем подключение к БД
db = SQLAlchemy(app)


@app.route("/")
def page_index():
    """Главня страница сайта, со статистикой о ботах."""

    # Получить всех пользователей
    user = db.session.query(Telegram_User).filter(Telegram_User.telegramID != config.BOT_ID).all()

    # Получить все проекты
    project = db.session.query(Telegram_Projects).all()

    return render_template('index.html',
                           # bot_status = page_get_bot(),  # Информация о самом боте
                           # bot_link = config.BOT_LINK,   # URL сылка на телеграм бота
                           user_count=len(user),        # Информация о Пользователях
                           project_count=len(project),  # Информация о Проектах
                           )

# TODO делать страницу
@app.route("/<telegram>/users")
def page_telegram_get_all_users(telegram):
    """Все пользователи для Телеграмма."""

    # Получить всех пользователей
    users = db.session.query(Telegram_User).filter(Telegram_User.telegramID != config.BOT_ID).all()

    return render_template('users.html', users=users)


# TODO делать страницу
@app.route("/<telegram>/projects")
def page_all_projects(telegram):
    """Все проекты для Телеграмма."""

    # Получить всех пользователей джоиных с их проектами
    projects = db.session.query(Telegram_User, Telegram_Projects).\
        join(Telegram_Projects, Telegram_User.telegramID == Telegram_Projects.telegramID).\
        filter(Telegram_User.telegramID != config.BOT_ID).all()

    return render_template('projects.html', projects=projects)


if __name__ == "__main__":
    app.run(debug=True, port=config.WEBSITE_PORT)
