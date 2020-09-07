import multiprocessing
import website
import os

# import threading
# from threading import Thread

from facebook_config import SERVER_START_COMMAND_FOR_CLI


"""Точка входа всего приложения, регистрация и запуск дочерних процессов.
После запуска всех дочерних процессво, в главном процессе запускается сайт,
для управления ботами."""


def all_process_start():
    """В главном процессе запускается сайт, в дочерних процессы для Telegram, FaceBook.
    p1.join() - эта команд ожидает завершение процесса."""
    # telegram_process = multiprocessing.Process(target=telegram_process_register)
    # Thread

    telegram_process = multiprocessing.Process(target=telegram_process_register)
    facebook_process = multiprocessing.Process(target=facebook_process_register)
    facebook_process_host = multiprocessing.Process(target=facebook_process_host_register)
    # nlp_process = multiprocessing.Process(target=nlp_process_register)

    telegram_process.start()
    facebook_process.start()
    facebook_process_host.start()
    # nlp_process.start()

    # print('================' * 10)
    # print("Запущено потоков: %i." % threading.active_count())
    # print('================' * 10)

def telegram_process_register():
    """Метод регистрирует процесс для запуска Telegram бота """
    import Telegram.bot


def facebook_process_register():
    """Метод регистрирует процесс для запуска FaceBook бота """
    import Facebook.app


def facebook_process_host_register():
    """Выполнение команды как, командв CLi на расшариваение локального хоста в Сеть."""
    # print('================'*10)
    # print(SERVER_START_COMMAND_FOR_CLI)
    # print('================' * 10)
    os.system(SERVER_START_COMMAND_FOR_CLI)


# def nlp_process_register():
#     """Метод регистрирует процесс для запуска Бота обработки текста """
#     pass


# def website_process_register():
#     website.website_server_start()  # Запуск сайта в главном процессе


all_process_start()  # Метод запускает дочерние процессы, для запуска ботов
website.website_server_start()  # Запуск сайта в главном процессе


