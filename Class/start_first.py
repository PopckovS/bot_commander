#! /usr/bin/python3

from Class.Fabrica import AbstractCommandRegister

from multiprocessing import Process
from multiprocessing import Pool

from threading import Thread

import config
import os


# TODO Не исполняется запуск сайта на caltunnel из за этого пока что нельзя установить вэбхук с FaceBook.
class CommandRegister(AbstractCommandRegister):

    """Класс наследуется AbstractCommandRegister.
     Реализует регистрацию запускаемых процессов, и сайтов которые будут открыты в Интернет."""

    process_prefix = 'python3'
    process_list = []
    tunnels_list = []
    domain = {}

    def start(self):
        """Запускает все что было зарегестрировано для процессов и для сайтов,
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

    def process_register(self, script):
        """Регистрирует команду для исполнения в своем процессе."""
        self.process_list.append(self.process_prefix + ' ' + script)

    def localtunnel_register(self, domain, port):
        """Регистрирует какие сайты и на каком порту открыть в мир."""
        self.domain[domain] = port
        self.tunnels_list.append(
            f"lt -h http://serverless.social --subdomain {domain} -p {port}"
        )

    def wrapper_show(func_name):
        """Функция обертка для вывода зарегестрированных процессов."""
        def wrapper(self):
            result = func_name(self)
            print(result)
        return wrapper

    @wrapper_show
    def get_register_process(self):
        """Показать все зарегестрированные процессы."""
        return self.process_list

    @wrapper_show
    def get_register_tunnels(self):
        """Показать все зарегестрированные сайты и их порты."""
        return self.domain
