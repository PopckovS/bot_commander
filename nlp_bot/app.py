#! /usr/bin/python3

from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy

import requests
import json
import sys
import os

# Добавляем путь к родительской директории
two_up = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(two_up)

import nlp_bot.config as config
from nlp_bot.bot import nlp_bot_get_message

app = Flask(__name__)
app.secret_key = 'some_secret'
sslify = SSLify(app)
# # Этот параметр отслеживает изменение Моделей прямо во время работы приложения
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECT_DB


@app.route('/', methods=['GET', 'POST'])
def page_index():
    """Главная страница, сформой отправки для общения с ботом."""

    if request.method == 'POST':

        question = request.form.get('message')
        answer = nlp_bot_get_message(question)

        print('Вопрос = ', question)
        print('Ответ = ', answer)
        return render_template('index.html')

    return render_template('index.html')


@app.route("/SendMessage/", methods=['POST'])
def send_message_from():
    """Получаем сообщение от пользователя через AJAX запрос.
    Передаем сообщение nlp боту и получаем от него ответ,
    Возвращаем ответ пользователю."""

    # Сообщение от пользователя
    question = request.form.get('message')
    question = question.strip()

    # Сообщение от бота
    answer = nlp_bot_get_message(question)

    return {
        'result': 'ok',
        'msg': answer
    }


if __name__ == "__main__":
    app.run(debug=True, port=config.SERVER_PORT)
