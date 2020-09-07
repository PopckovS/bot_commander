import telebot
# import Telegram.config
import config

# bot = telebot.TeleBot(Telegram.config.API_KEY)
bot = telebot.TeleBot(config.API_KEY)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = 'Привет !'
    bot.send_message(message.from_user.id, text)


def telegram_start():
    bot.polling(none_stop=True, interval=0)


telegram_start()
