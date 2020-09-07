

# Ссылка на БРИФ в гугул страницах
GOOGLE_FORM_BRIF = 'https://docs.google.com/forms/d/e/1FAIpQLSdAhEeEfNyv4fnTHRt_EmxfbZ3JQtU1uH5lQr7bvgIXfP_ZVA/viewform'

# Хост для запуска сайта
WEBSITE_HOST = 'localhost'

# Порт для запуска сайта
WEBSITE_PORT = '9000'

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
