#! /usr/bin/python3

from Class.Fabrica import AbstractCommandRegister

from multiprocessing import Process
from multiprocessing import Pool

from threading import Thread

import config
import os


class CommandRegister(AbstractCommandRegister):

    """Класс наследуется AbstractCommandRegister.
     Реализует регистрацию запускаемых процессов, и сайтов которые будут открыты в Интернет."""

    process_prefix = 'python3'
    process_list = []
    tunnels_list = []
    domain = {}

    def start(self):
        """Запускает все что было зарегестрировано для процессов и для сайтов,
        на исполнения в своем собственном процессе я каждого."""
        self.run_process(self.process_list)
        self.run_process(self.tunnels_list)

    def process_register(self, script):
        """Регистрирует команду для исполнения в своем процессе."""
        self.process_list.append(self.process_prefix + ' ' + script)

    def localtunnel_register(self, domain, port):
        """Регистрирует какие сайты и на каком порту открыть в мир."""
        self.domain[domain] = port
        command = f"lt -h http://serverless.social --subdomain {domain} -p {port}"
        self.tunnels_list.append(command)

    def run_process(self, commands):
        """Метод запускает на исполнение процессы. Определяет в себе функцию запуска,
        и сдесь же запускает в ней новый проуесс, для всех зарегестрированных процессов."""
        for command in commands:
            def cli_run():
                """Функция исполняет команду как bash скрипт в своем собственном процессе."""
                os.system(command)
            process = Process(target=cli_run)
            process.start()

