# #! /usr/bin/python3

# Есть несколько классов загпуска приложения
# from Class.start_first import CommandRegister
from Class.start_two import CommandRegister


# Класс для регистрации процессов на исполнение
Register = CommandRegister()

# Регистрация процессов
Register.process_register('Telegram/bot.py')  # Порт не используется
Register.process_register('Facebook/bot.py')  # 9001
Register.process_register('Website/app.py')   # 9000
Register.process_register('nlp_bot/app.py')   # 9003

# Регистрация Сайтов, через localtunnel
# https://sergio-fb-bot.serverless.social/
Register.localtunnel_register('sergio-fb-bot', 9001)
# https://nlp-bot-sergey.serverless.social
Register.localtunnel_register('nlp-bot-sergey', 9003)

# Показать что будет зарегестрировано для исполнения
Register.get_register_process()
Register.get_register_tunnels()

# Запуск всех зарегестрированных процесов
Register.start()
