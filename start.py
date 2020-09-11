# #! /usr/bin/python3

from Fabrica import CommandRegister

# Класс для регистрации процессов на исполнение
Register = CommandRegister()

# Регистрация процессов
Register.process_register('Telegram/bot.py')
Register.process_register('Facebook/bot.py')
Register.process_register('Website/app.py')

# Регистрация Сайтов
# Register.localtunnel_register('sergio-fb-bot', 9001)
Register.rrr('sergio-fb-bot', 9001)
Register.rrr('sergio-fb-bot1',9000)

# Показать что будет зарегестрировано
Register.get_register_process()
Register.get_register_tunnels()

# Запуск всех зарегестрированных процесов
Register.start()

