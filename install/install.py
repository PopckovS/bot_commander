#! /usr/bin/python3

import os
import sys
from install.config import LIBRARY


class Install():
    """Класс установкщик всех нужных пакетов для работы приложения."""

    def __init__(self):
        self.library = LIBRARY

    def insall_library(self):
        """Метод в цикле устанавливает библиотеки."""
        for key, value in self.library.items():
            for elem in value:
                os.system(elem)
