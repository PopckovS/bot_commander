#! /usr/bin/python3

from abc import ABC, abstractmethod


class AbstractCommandRegister(ABC):
    """Абстрактный класс для регистрации процессов и запуска приложения."""

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def process_register(self, script):
        pass

    @abstractmethod
    def localtunnel_register(self, domain, port):
        pass

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







