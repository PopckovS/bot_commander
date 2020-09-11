

import multiprocessing
import config
import os

"""Точка входа всего приложения, регистрация и запуск дочерних процессов.
После запуска всех дочерних процессво, в главном процессе запускается сайт,
для управления ботами."""


def all_process_start():
    """В главном процессе запускается сайт, в дочерних процессах:
     - Сайт     PORT: 9000
     - Facebook PORT: 9001
     - locTunel PORT: 9001
     - Telegram PORT: 9002
     - NLP bot  PORT: 9003
    p1 = multiprocessing.Process(target=<Имя Регистрируемой функции>)
    p1.start() - запуск работы процесса.
    p1.join() - эта команд ожидает завершение процесса."""

    telegram_process = multiprocessing.Process(target=telegram_process_register)
    facebook_process = multiprocessing.Process(target=facebook_process_register)
    facebook_process_host = multiprocessing.Process(target=facebook_process_host_register)

    telegram_process.start()
    facebook_process.start()
    facebook_process_host.start()


def telegram_process_register():
    """Метод регистрирует процесс для запуска Telegram бота """
    os.system('python3 Telegram/bot.py')


def facebook_process_register():
    """Метод регистрирует процесс для запуска FaceBook бота """
    os.system('python3 Facebook/bot.py')


def facebook_process_host_register():
    """Выполнение команды как, командв CLi на расшариваение локального хоста в Сеть."""
    # os.system("lt -h http://serverless.social --subdomain sergio-fb-bot -p 9001")
    os.system(config.LOCAL_TUNNEL_FACEBOOK + str(config.TUNNEL_PORT))


def website_process_register():
    """Запуск сайта"""
    os.system('python3 Website/app.py')


all_process_start()  # Метод запускает дочерние процессы, для запуска ботов
website_process_register()  # Запуск сайта в главном процессе
