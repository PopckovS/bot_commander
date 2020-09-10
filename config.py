LOCAL_TUNEL_FACEBOOK = 'lt -h http://serverless.social --subdomain sergio-fb-bot -p 9001'

# Хост для запуска сайта
WEBSITE_HOST = 'localhost'

# База Данных которую мы используем для работы
DB = 'bot_commander'

# ХОСТ для подключения к БД
DB_HOST = 'localhost'

# Имя пользователя для доступа к БД
DB_USERNAME = 'serg'

# Пароль для Доступа к БД
DB_PASSWORD = '11'

# Подключения к БД через Flask SQLAlchemy
CONNECT_DB = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB
