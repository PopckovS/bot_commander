#! /usr/bin/python3

from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response

app = Flask(__name__)


@app.route("/")
def page_index():
    '''Главная страница со статистикой работы Бота'''
    return 'Telegram'


if __name__ == "__main__":
    app.run(debug=True, port=9002)

