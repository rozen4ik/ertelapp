import telebot
from telebot import types
import sqlite3


a_task = "Евгений Маслов"


def read_from_db(author_task):
    try:
        sqlite_connection = sqlite3.connect("dbertel.sqlite3")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from task_task WHERE author_task = ?"""
        cursor.execute(sqlite_select_query, (author_task, ))
        records = cursor.fetchall()
        result = ""
        for row in records:
            result = f"№ {row[0]} \nДата: {row[1]} \nВремя: {row[2]} \nКто поручил: {row[4]} \nЗадача: {row[3]} \nМесто выполнения: {row[6]} \nСроки выполнения: {row[7]}"

        cursor.close()

        return result

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


read_from_db(a_task)

TOKEN = "5590862368:AAEAghHqrgaaZnoHf6A17y6BiUFhwkFksb0"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("Получить задачу")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")
    elif message.text == "Получить задачу":
        row = read_from_db(a_task)
        bot.send_message(message.chat.id, text=row)


bot.polling(none_stop=True)
