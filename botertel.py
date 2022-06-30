import telebot
from telebot import types
from ertelapp import settings
from task.models import Task


def read_from_db(employee_task):
    task = Task.objects.all()
    result = []
    for row in task:
        if row.employee_task == employee_task:
            result.append(f"<u><b>№</b></u> {row.id} \n<u><b>Дата:</b></u> {row.date_task} \n<u><b>Время:</b></u> {row.time_task} \n<u><b>Кто поручил:</b></u> {row.author_task} \n<u><b>Задача:</b></u> {row.text_task} \n<u><b>Место выполнения:</b></u> {row.address_task} \n<u><b>Сроки выполнения:</b></u> {row.line_task}")
    print("Обращение к базе данных")
    return result


bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Получить задачу")
    markup.add(btn2)
    CHAT_ID = message.chat.id
    bot.send_message(CHAT_ID,
                     text="Привет, {0.first_name}! Я тестовый бот для компании ERTEL".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(func=lambda call: True)
def func(id, message):
    if message.text == "Получить задачу":
        employee_task = f"{message.from_user.first_name} {message.from_user.last_name}"
        row = read_from_db(employee_task)
        len_row = len(row)
        bot.send_message(id, text=row[len_row-1], parse_mode="HTML")

bot.polling(none_stop=True)
