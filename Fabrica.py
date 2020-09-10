#! /usr/bin/python3
from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Process
from multiprocessing import Pool
import config
import os
from threading import Thread

"""Унаследовать метод можно указанием специального слова 
super().<Название еметода родителя>
"""


class AbstractCommandRegister(ABC):
    """Абстрактный класс для реализауии Класса запуска приложения."""

    @abstractmethod
    def process_register(self, script):
        pass

    @abstractmethod
    def localtunnel_register(self, cli_command, port):
        pass


class CommandRegister(AbstractCommandRegister):
    """Класс регистрации запускаемых процессов, и сайтов
    которые будут открыты в Интернет."""

    process_prefix = 'python3'
    processing = set()
    process_list = []
    tunnels_list = []
    domain = {}

    def process_register(self, script):
        """Регистрирует команду для исполнения в своем процессе."""
        self.process_list.append(self.process_prefix + ' ' + script)

    def localtunnel_register(self, domain, port):
        """Регистрирует какие сайты и на каком порту открыть в мир."""
        self.domain[domain] = port
        self.tunnels_list.append(
            f"lt -h http://serverless.social --subdomain {domain} -p {port}"
        )

    def start(self):
        """Запускает все что было зарегестрировано для процессво,для сайтов
        на исполнения в своем собственном процессе."""
        self.creaet_process(self.process_list)
        self.creaet_process(self.tunnels_list)


    def creaet_process(self, commands):
        """Метод Pool из модуля multiprocessing регистрирует не один как Process.
        А сразу енсколько процессво, параметр processes - количество процессов для исполнения
        Функция map - применяет указанную функцию к каждому из аргументов."""
        pool = Pool(processes=len(commands))
        pool.map(self.cli_run, commands)


    def cli_run(self, command):
        """Функция исполняет команду как bash скрипт в своем собственном процессе."""
        os.system(command)

    def wrapper_show(func_name):
        """Функция обертка для вывода зарегестрированных процессво."""
        def wrapper(self):
            result = func_name(self)
            print(result)
        return wrapper

    @wrapper_show
    def get_register_process(self):
        return self.process_list

    @wrapper_show
    def get_register_tunnels(self):
        return self.tunnels_list

    @wrapper_show
    def get_domain(self):
        return self.domain



# Класс для регистрации процессов на исполнение
Register = CommandRegister()

# Регистрация процессов
Register.process_register('Telegram/bot.py')
Register.process_register('Facebook/bot.py')
# Register.process_register('Website/app.py')

# Регистрация Сайтов
Register.localtunnel_register('sergio-fb-bot', 9001)

# Показать что будет зарегестрировано
Register.get_register_process()
Register.get_register_tunnels()
Register.get_domain()

# Запуск всех зарегестрированных процесов
Register.start()
