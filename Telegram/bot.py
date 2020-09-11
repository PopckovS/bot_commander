#! /usr/bin/python3

from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from emoji import emojize
import telebot
import sys
import os

# Добавляем путь к родительской директории
two_up = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(two_up)

from Telegram.config import config

from models.Company import Company
from models.CompanyDescription import CompanyDescription

from models.Telegram_User import Telegram_User
from models.Telegram_Admin import Telegram_Admin
from models.Telegram_Projects import Telegram_Projects
from models.Telegram_Messages import Telegram_Messages


# Запускаем сервер на lask
app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECT_DB

db = SQLAlchemy(app)
# db.create_all()

#
# def create_telegram_bot(api):
#     """Создаем Экземпляр бота, и передаем ему API ключ."""
#     global bot
#     bot = telebot.TeleBot(api)
#
#
# # Запуск приложения
# create_telegram_bot(config.API_KEY)

bot = telebot.TeleBot(config.API_KEY)

# ===========================================================
# ===========================================================
# ===========================================================
def convert_trace(func_trace):
    '''Метод декоратор(обертка) для методов отладки.'''
    def result_func(arg1):
        print('========================')
        func_trace(arg1)
        print('========================')
    return result_func


@convert_trace
def trace(object):
    '''Метод отладчик, выводи ID и текст сообщения'''
    print(object)
    print(type(object))


@convert_trace
def tracem(message):
    '''Метод отладчик, выводи ID и текст сообщения'''
    print(f'id сообщения = {message.message_id}')
    print(f'text сообщения =  {message.text}')




def save_message(message, text='', mod='user'):
    '''Метод сохраняет в Бд переданное сообщение, сохранение
    может быть как сообщений пользователю боту, так и бота пользователю
    recepient - string сохранение сообщения от кого кому
        user Сохраняется как сообщение от пользователя к телеграм боту
        bot  Сохраняется как сообщение от бота к пользователю
    '''

    if mod is 'user':
        # Сохранение сообщения от пользователя к боту
        message = Telegram_Messages(telegramID=message.chat.id, message=message.text, recipient=config.BOT_ID, messageID=message.message_id)
    elif mod is 'bot':
        # Сохранение сообщения от бота пользователю
        message = Telegram_Messages(telegramID=config.BOT_ID, message=text, recipient=message.chat.id, messageID=message.message_id)

    db.session.add(message)
    db.session.commit()




def save_user(message):
    '''Метод делает запрос к БД проверяет существует ли пользователь
    с таким telegramID если его не существует, то создаем нового пользователя.'''

    # Получаем первую запись из Бд с таким telegramID
    result = db.session.query(Telegram_User).filter(Telegram_User.telegramID == message.chat.id).first()

    # Если пользователь не существует, то создаем его
    if result is None:
        # Создаем обьект и вносим данные в его атрибуты
        user = User(
            telegramID=message.chat.id,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
            username=message.chat.username,
            type=message.chat.type
        )

        db.session.add(user)  # Вносим пользователя в сессию
        db.session.commit()  # Сохраняем данные о пользователе в БД
        print('Новый пользователь создан')
    else:
        print('Пользователь с таким id уже существует')



@bot.message_handler(commands=['start'])
def start_message(message):
    '''Главный базовый метод, срабатвает в момент активайии бота, выводит приветствие, и создает кнопки.'''

    # Создаем кнопки с общим функционалом который увидит пользователь при начале работы
    # При создании передаем параметр = True это ркгулирует размер кнопок под ширину экрана
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Реквизиты', 'Наши услуги', 'Факты о нас')
    keyboard.add('Заполнить БРИФ для вашего сайта')
    keyboard.add('Контакты наших Менеджеров')

    # Выводим притствие, и показываем кнопки нашему пользователю
    bot.send_message(message.chat.id, 'Привет {0} {1} вас приветствует бот компании {2} \n'
                     .format(message.from_user.first_name, message.from_user.last_name, 'MitLabs'),
                     reply_markup=keyboard)

    # Создаем и отправляем кнопу для перехода на сайт компании
    keyboard_inline = telebot.types.InlineKeyboardMarkup()
    btn_url_mitlabs = telebot.types.InlineKeyboardButton(text="Перейти на сайт компании MitLabs", url="https://mitlabs.ru")
    keyboard_inline.add(btn_url_mitlabs)
    text = '''Анализируем, планируем, помогаем развиваться:
        - Анализ вашего бизнеса
        - Выявление эффективных каналов продаж
        - Анализ ЦА и конкурентов
        - Разработка детальной стратегии развития
        Планирование digital-стратегии — это создание полного, 
        пошагового руководства к действию, по которому можно развивать и поддерживать свою компанию с нуля.
    '''

    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, text, reply_markup=keyboard_inline)

    # message.text Содержит в себе текст сообщения от пользоватеял
    save_user(message)
    save_message(message)





@bot.message_handler(commands=['help'])
def default_test(message):
    '''Метод помошник, выводит справочную информацию.'''

    text = "/start Начало работы с ботом \n" \
           "/help Получить список всех доступных команд \n" \
           "/info Получить информацию о пользователе\n"\
           "/adminRegistration Регистрация Администратора для бота\n"
    bot.send_message(message.from_user.id, text)





# TODO сделать регистрацию пароля
@bot.message_handler(commands=['adminRegistration'])
def admin_registration(message):
    '''Регистрация администратора.'''

    bot.send_message(message.from_user.id, "Как вас зовут?")
    bot.register_next_step_handler(message, registration_admin_name)




def registration_admin_name(message):
    '''Метод регистрацции имени нового администратора.'''

    admin = db.session.query(Telegram_Admin).filter(Telegram_Admin.telegramID == message.chat.id).first()

    # Такого Администратора еще нету, так что создадим его
    if admin is None:
        admin = Telegram_Admin(
            telegramID=message.chat.id,
            name=message.text,
            password='-',
            get_messages=0,
        )
        db.session.add(admin)
        db.session.commit()
    else:
        admin.name = message.text
        db.session.add(admin)
        db.session.commit()

    bot.send_message(message.from_user.id, 'Готовы работать с клиентом и \nполучать сообщения в телеграме ?')
    bot.register_next_step_handler(message, registration_admin_get_messages)




def registration_admin_get_messages(message):
    '''Метод регистрации администратора, будет ли он получать сообщения ?.'''

    admin = db.session.query(Telegram_Admin).filter(Telegram_Admin.telegramID == message.chat.id).first()
    if message.text == 'да':
        admin.get_messages = 1
    else:
        admin.get_messages = 0

    db.session.add(admin)
    db.session.commit()

    bot.send_message(message.from_user.id, 'Введите секретный пароль полученный на сайте ?')
    bot.register_next_step_handler(message, registration_admin_password)




def registration_admin_password(message):
    '''Метод регистрации пароль нового администратора.'''

    admin = db.session.query(Telegram_Admin).filter(Telegram_Admin.telegramID == message.chat.id).first()
    admin.password = message.text
    db.session.add(admin)
    db.session.commit()

    # bot.send_message(message.from_user.id, 'Вы зарегестрированы ! \nПерейдите на сайт <a>{sait}'.format(sait=SAIT))

    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_url_mitlabs = telebot.types.InlineKeyboardButton(text="Mitlabs BotFather", url="https://mitlabs.ru")
    keyboard.add(btn_url_mitlabs)
    bot.send_message(message.chat.id, "Вы зарегестрированы ! \nПерейдите на сайт для управления ботом", reply_markup=keyboard)





@bot.message_handler(commands=['get_project'])
def get_project(message):
    '''Получить данные о проекте, данного пользователя по его id в системе'''
    project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()
    print(project.__repr__())
    bot.send_message(message.chat.id, project.__repr__())





@bot.message_handler(commands=["info"])
def handle_docs_audio(message):
    '''Выводит информацию о текущем состоянии чата'''
    # bot.send_poll(message.chat.id, 'вопрос', options=['1', '2', '3'])
    # bot.send_message(message.chat.id, 'Привет')
    # bot.send_message(message.chat.id, message.chat.id)

    '''В ответе с сервера telegram мы получаем'''
    # # bot.send_poll(message.chat.id, 'вопрос', options=['1', '2', '3'])

    bot.send_message(message.chat.id, 'Содержимое переменной message.chat текущем состоянии чата')
    bot.send_message(message.chat.id, f'id = {message.chat.id}')
    bot.send_message(message.chat.id, f'first_name = {message.chat.first_name}')
    bot.send_message(message.chat.id, f'last_name = {message.chat.last_name}')
    bot.send_message(message.chat.id, f'username = {message.chat.username}')
    bot.send_message(message.chat.id, f'type = {message.chat.type}')




@bot.message_handler(commands=['document'])
def handle_docs_photo(message):
    '''Прием документов от пользователя'''

    # global src
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # src = '/home/users-name/received/' + message.document.file_name;
        # src = '/document/' + message.document.file_name
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            # new_file.write(downloaded_file)
            new_file.write('/document/' + downloaded_file)
        bot.reply_to(message, "Я сохраню ваш файл")
    except Exception as e:
        bot.reply_to(message, 'Возникла ошибка: ' + e)

    # bot.send_message(message.chat.id, 'message.document.file_name = '+message.document.file_name)




@bot.message_handler(commands=['name'])
def handle_email(message):
    bot.send_message(message.chat.id, str(__name__))




@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Метод обработчик любого введенного текста, также обрабатывает нажатие Inline кнопок."""

    tracem(message)
    save_message(message)

    # Получаем пользователя из БД
    user = db.session.query(Telegram_User).filter(Telegram_User.telegramID == message.chat.id).first()

    # Режим работы бота с пользователем, общение с человеком/ботом
    if user.bot_command == 0:
        if message.text == 'Реквизиты':

            company = db.session.query(Company).filter(Company.name == config.COMPANY).first()

            save_message(message, "Пользователю показан блок 'Наши реквизиты'", 'bot')
            bot.send_message(message.from_user.id, company.requisites)
        elif message.text == 'Наши услуги':
            photo = open('file/mitlabs-price.png', 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption='аши цены на разработку сайта')

            keyboard = telebot.types.InlineKeyboardMarkup()

            btn1 = telebot.types.InlineKeyboardButton(text='Дизайн от А до Я', callback_data='Дизайн от А до Я')
            btn2 = telebot.types.InlineKeyboardButton(text='Маркетинг', callback_data='Маркетинг')
            btn3 = telebot.types.InlineKeyboardButton(text='Разработка сайта', callback_data='Разработка сайта')
            btn4 = telebot.types.InlineKeyboardButton(text='E-COMMERCE', callback_data='E-COMMERCE')
            btn5 = telebot.types.InlineKeyboardButton(text='DEVOPS', callback_data='DEVOPS')
            btn6 = telebot.types.InlineKeyboardButton(text='AI И ML', callback_data='AI И ML')
            em1 = emojize('\N{page facing up}', use_aliases=True)
            btn7 = telebot.types.InlineKeyboardButton(text=em1 + ' Документы и право', callback_data='Документы и право')

            keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

            save_message(message, "Пользователю показан блок 'Услуг Компании'", 'bot')
            # em2 = emojize('gear', use_aliases=True)
            bot.send_message(message.chat.id, f"Услуги компании:", reply_markup=keyboard)

        elif message.text == 'Факты о нас':
            company = db.session.query(Company).filter(Company.name == config.COMPANY).first()
            save_message(message, "Пользователю показан блок 'Факты о нас'", 'bot')
            bot.send_message(message.from_user.id, company.facts)

        elif message.text == 'Заполнить БРИФ для вашего сайта':
            '''Начало цикла заполнения информации по проекту'''
            keyboard = telebot.types.InlineKeyboardMarkup()

            btn_questions = telebot.types.InlineKeyboardButton(text='Короткий опрос', callback_data='Короткий опрос')
            btn_brif = telebot.types.InlineKeyboardButton(text='Полноценный БРИФ', callback_data='Полноценный БРИФ')
            keyboard.add(btn_questions, btn_brif)
            bot.send_message(message.from_user.id, "Есть несколько способов заполнить анкету:", reply_markup=keyboard)
        elif message.text == 'Контакты наших Менеджеров':
            send_contacts_manager(message)
        else:
            text = 'Я вас не понимаю :( Чем я могу тебе помочь?'
            bot.send_message(message.from_user.id, text)
            save_message(message, text, 'bot')



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    '''Метод обработчик нажатых Inline кнопок, тоесть заранее заготов.кнопок меню.'''

    # Получить из БД компанию и ее описание для панельных кнопок
    company = db.session.query(Company).filter(Company.name == config.COMPANY).first()
    descriptions = db.session.query(CompanyDescription).filter(CompanyDescription.Company_id == company.id).all()

    current = None
    # Получаем текущую нажатую кнопку
    for elem in descriptions:
        if call.data == elem.title:
            current = elem

    if call.message:
        # Это для обработки запроса на показ Услуг компании.
        # Если callback_data что была передана есть в массиве данных
        if current is not None:
            # Нажатая кнопка найдена
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=current.text)
        if call.data == 'project_stop':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Анкета стерта")
        if call.data == 'stop_step':
            # Метод очистки всех зарегестрированных шагов
            bot.clear_step_handler(call.message)
        if call.data == 'Короткий опрос':
            '''Заполнение короткой Анкеты'''
            keyboard = telebot.types.InlineKeyboardMarkup()
            btn_stop = telebot.types.InlineKeyboardButton(text="❌ Закончить", callback_data='stop_step')
            keyboard.add(btn_stop)

            save_message(call.message, 'Пользователь начал заполнение анкеты', 'bot')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Начнем заполнение анкеты:\nКак вас зовут ?", reply_markup=keyboard)
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Начнем заполнение анкеты:\nКак вас зовут ?")
            bot.register_next_step_handler(call.message, get_name)
        if call.data == 'Полноценный БРИФ':
            keyboard = telebot.types.InlineKeyboardMarkup()
            btn_google_brif = telebot.types.InlineKeyboardButton(text="В Google форме", url=config.GOOGLE_FORM_BRIF)
            keyboard.add(btn_google_brif)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Заполнить БРИФ вы можете по ссылке:", reply_markup=keyboard)
        if call.data == 'project_yes':
            # Пользователь подтвердил заполнение анкеты
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Прекрасно, мы обработаем вашу анкету.')
        if call.data == 'project_no':
            """Пользователь хочет перезаполнить анкету"""
            keyboard = telebot.types.InlineKeyboardMarkup()
            btn_stop = telebot.types.InlineKeyboardButton(text="❌ Закончить", callback_data='stop_step')
            keyboard.add(btn_stop)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Хорошо, давайте с начала')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Как Вас зовут?', reply_markup=keyboard)
            bot.register_next_step_handler(call.message, get_name)




def send_contacts_manager(message):
    '''Показать клиенту контакты наших менеджеров.'''

    admin = db.session.query(Telegram_Admin).filter(Telegram_Admin.get_messages == 1).all()

    if admin != False:
        bot.send_message(message.chat.id, "Доступные контакты:")
        for elem in admin:
            bot.send_contact(chat_id=message.from_user.id, first_name=elem.first_name, phone_number=elem.phone_number)
        save_message(message, "Пользователю показаны контакты Менеджеров'", 'bot')
    else:
        bot.send_message(message.chat.id, "Извините, сейчас некому с вами связаться")
        save_message(message, "Пользователь запросил контакты менеджеров, но никого не нашлось", 'bot')

    bot.send_venue(chat_id=message.from_user.id, latitude=51.668194, longitude=39.208174, title="Mitlabs",
                   address="г. Воронеж, Проспект \nРеволюции 33Б — 5 Этаж")


def get_name(message):
    '''Метод получает от пользователя Имя Фамилию по установленному паттерну'''

    project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()

    if project is None:
        project = Telegram_Projects(telegramID=message.chat.id, fio=message.text)
    else:
        project.fio = message.text

    db.session.add(project)
    db.session.commit()

    # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
    save_message(message)
    save_message(message, "Контактная информация ?", 'bot')

    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_stop = telebot.types.InlineKeyboardButton(text="❌ Закончить", callback_data='stop_step')
    keyboard.add(btn_stop)

    em_email = emojize('\N{envelope}', use_aliases=True)
    em_phone = emojize('☎', use_aliases=True)
    bot.send_message(message.from_user.id, f'Контактная информация: email {em_email} телефон {em_phone} другое ?', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_contacts)



def get_contacts(message):
    '''Метод получает от пользователя контактную информацию'''
    save_message(message)

    project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()
    project.contacts = message.text

    db.session.add(project)
    db.session.commit()

    bot_message = 'Расскажите о Вашем проекте'
    save_message(message, bot_message, 'bot')

    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_stop = telebot.types.InlineKeyboardButton(text="❌ Закончить", callback_data='stop_step')
    keyboard.add(btn_stop)

    bot.send_message(message.from_user.id, bot_message, reply_markup = keyboard)
    bot.register_next_step_handler(message, get_about_project)




# TODO РАЬНЬШЕ ЭТОЛТ МЕТОД ВЫПОЛНЯЛ ФУНКЦИЮ РЕГИСТРАЦИИ EMAIL ПОЛЬЗОВАТЕЛЯ, ПОКА НЕ ИСПОЛЬЗУЕТСЯ
def get_email(message):
    '''Метод получает от пользователя email'''

    result = re.search(r'[\w.-]+@[\w.-]+\.?[\w]+?', message.text)

    if result == None:

        # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
        save_message(message)
        save_message(message, "Кажется, это неправильный email :( Попробуй еще раз!", 'bot')

        bot.send_message(message.from_user.id, 'Кажется, это неправильный email :( Попробуй еще раз!')
        bot.register_next_step_handler(message, get_email)
    else:
        # Email введен правильно, сохраняем его в БД
        # Обновляем поле email в БД, по ее id
        # Сохраняяем Почту проекта в поле email модели Projects
        project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()
        project.email = message.text
        db.session.add(project)
        db.session.commit()

        # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
        save_message(message)
        save_message(message, "Ваш телефон ?", 'bot')

        em = emojize('☎', use_aliases=True)
        bot.send_message(message.from_user.id, f'{em} Ваш телефон  ?')
        bot.register_next_step_handler(message, get_phone)



# TODO РАЬНЬШЕ ЭТОЛТ МЕТОД ВЫПОЛНЯЛ ФУНКЦИЮ РЕГИСТРАЦИИ PHONE ПОЛЬЗОВАТЕЛЯ, ПОКА НЕ ИСПОЛЬЗУЕТСЯ
def get_phone(message):
    '''Метод получает от пользователя телефон'''

    result = re.search(r"\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b", message.text)

    if result == None:

        # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
        save_message(message)
        save_message(message, "Кажется, это неправильный телефона :( Попробуй еще раз!", 'bot')

        bot.send_message(message.from_user.id, 'Кажется, это неправильный телефона :( Попробуй еще раз!')
        bot.register_next_step_handler(message, get_phone)
    else:
        # Если мы попали сюда, то телефон введен правильно, и мы его сохраняем.
        # Обновляем поле phone в БД, по ее id
        # Сохраняяем Телефон проекта в поле phone модели Projects
        project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()
        project.phone = message.text
        db.session.add(project)
        db.session.commit()

        # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
        save_message(message)
        save_message(message, "Расскажите о Вашем проекте", 'bot')

        bot.send_message(message.from_user.id, 'Расскажите о Вашем проекте')
        bot.register_next_step_handler(message, get_about_project)




def get_about_project(message):
    """Метод сохраняет данные о проекте, опрашивает пользователя на правильность заполнения данных."""

    # Сохраняяем Описание проекта в поле aboutProject модели Projects
    project = db.session.query(Telegram_Projects).filter(Telegram_Projects.telegramID == message.chat.id).first()
    project.aboutProject = message.text
    db.session.add(project)
    db.session.commit()

    # Сохраняем и ответ пользователя на превыдущий вопрос и новый вопрос бота
    save_message(message)
    save_message(message, "Пользователю задан вопрос 'Правильно ли он заполнил данные'", 'bot')


    keyboard = get_btn_project()
    result_text = f"Все правильно ? \nВас зовут = {project.fio}"
    # result_text += f'\nВаш email = {project.email}'
    # result_text += f'\nВаш телефон = {project.phone}'
    result_text += f'\nВаши котакты = {project.contacts}'
    result_text += f'\nОписание проекта = {project.aboutProject}'


    # btn_stop = telebot.types.InlineKeyboardButton(text="❌ Закончить", callback_data='stop_step')
    # keyboard.add(btn_stop)


    bot.send_message(message.from_user.id, result_text, reply_markup=keyboard)
    bot.register_next_step_handler(message, get_answer)





# Завершающий вопрос о правильности заполнения данных.
def get_answer(message):
    save_message(message)



def get_btn_project():
    '''Создаем и добавляем inline кнопки, да/нет для продолжения или сброса опроса'''

    keyboard = telebot.types.InlineKeyboardMarkup()

    emoji_yes = emojize('✅', use_aliases=True)
    emoji_no = emojize('❌', use_aliases=True)

    btn_yes = telebot.types.InlineKeyboardButton(text=f'{emoji_yes} Да все верно', callback_data='project_yes')
    btn_no = telebot.types.InlineKeyboardButton(text=f'{emoji_no} Нет, хочу изменить', callback_data='project_no')
    btn_stop = telebot.types.InlineKeyboardButton(text=f'Стереть анкету', callback_data='project_stop')
    keyboard.add(btn_yes, btn_no)
    keyboard.add(btn_stop)

    return keyboard
# ===========================================================
# ===========================================================
# ===========================================================





def telegram_start():
    """Включение опроса Телеграм бота на сообщения от пользователя, если пользователь
    присылает сообщение, то оно автоматически приходит сюда. Если Бот отключен то,
    Telegram хранит все сообщения от всех пользователей в течении 24 часов."""
    bot.polling(none_stop=True, interval=0)


# Запуск Телеграм Бота
telegram_start()
