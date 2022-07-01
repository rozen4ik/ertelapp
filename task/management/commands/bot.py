import telebot
from telebot import types
from django.core.management.base import BaseCommand

from ertelapp import settings

bot = telebot.TeleBot(settings.TOKEN)


class Command(BaseCommand):
    help = "Телеграм бот"

    def handle(self, *args, **options):
        pass


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выполняется")
    btn2 = types.KeyboardButton("Выполнено")
    btn3 = types.KeyboardButton("Не выполнено")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет ✌️!\nЯ бот компании ЭРТЭЛ, через меня тебе будут ставить задания.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Выполняется":
        bot.send_message(message.chat.id, text="Функция в разработке")
    elif message.text == "Выполнено":
        bot.send_message(message.chat.id, text="Функция в разработке")
    elif message.text == "Не выполнено":
        bot.send_message(message.chat.id, text="Функция в разработке")


bot.infinity_polling()
