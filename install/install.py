#! /usr/bin/python3

import os
import sys
from config import LIBRARY


class Install():
    """Класс установкщик всех нужных пакетов для работы приложения."""

    def __init__(self):
        self.library = LIBRARY

    def insall_library(self):
        """Метод в цикле устанавливает библиотеки."""
        for key, value in self.library.items():
            for elem in value:
                os.system(elem)


""" 
Вызов этого метода начнет процесс установки всх нужных
библиотек для работы: python3 install/install.py
"""
instalObject = Install()
instalObject.insall_library()