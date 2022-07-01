import telebot
from telebot import types
from django.core.management.base import BaseCommand
from ertelapp import settings
from task.models import *

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
    end_task = Task.objects.all().latest("id")
    end_task_fullname = end_task.employee_task.split()
    end_task_firstname = end_task_fullname[0]
    end_task_lastname = end_task_fullname[1]
    if message.text == "Выполняется":
        end_task.status_task = "Выполняется"
        end_task.save()
        end_task = Task.objects.filter(employee_task=f"{end_task_firstname} {end_task_lastname}").latest("id")
        message_task = f"<b>Номер задачи:</b> {end_task.id}\n<b>Дата:</b> {end_task.date_task}\n<b>Время:</b> {end_task.time_task}\n<b>Кто поручил:</b> {end_task.author_task}\n<b>Статус задачи:</b> {end_task.status_task}\n<b>Задача:</b> {end_task.text_task}\n<b>Место выполнения:</b> {end_task.address_task}\n<b>Сроки выполнения:</b> {end_task.line_task}"
        bot.send_message(message.chat.id, text=f"Статус задачи {end_task.id} изменен на\n<b>Выполняется</b>", parse_mode="HTML")
        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML")
    elif message.text == "Выполнено":
        end_task.status_task = "Выполнено"
        end_task.save()
        end_task = Task.objects.filter(employee_task=f"{end_task_firstname} {end_task_lastname}").latest("id")
        message_task = f"<b>Номер задачи:</b> {end_task.id}\n<b>Дата:</b> {end_task.date_task}\n<b>Время:</b> {end_task.time_task}\n<b>Кто поручил:</b> {end_task.author_task}\n<b>Статус задачи:</b> {end_task.status_task}\n<b>Задача:</b> {end_task.text_task}\n<b>Место выполнения:</b> {end_task.address_task}\n<b>Сроки выполнения:</b> {end_task.line_task}"
        bot.send_message(message.chat.id, text=f"Статус задачи {end_task.id} изменен на\n<b>Выполнено</b>", parse_mode="HTML")
        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML")
    elif message.text == "Не выполнено":
        end_task.status_task = "Не выполнено"
        end_task.save()
        end_task = Task.objects.filter(employee_task=f"{end_task_firstname} {end_task_lastname}").latest("id")
        message_task = f"<b>Номер задачи:</b> {end_task.id}\n<b>Дата:</b> {end_task.date_task}\n<b>Время:</b> {end_task.time_task}\n<b>Кто поручил:</b> {end_task.author_task}\n<b>Статус задачи:</b> {end_task.status_task}\n<b>Задача:</b> {end_task.text_task}\n<b>Место выполнения:</b> {end_task.address_task}\n<b>Сроки выполнения:</b> {end_task.line_task}"
        bot.send_message(message.chat.id, text=f"Статус задачи {end_task.id} изменен на\n<b>Не выполнено</b>", parse_mode="HTML")
        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML")


bot.infinity_polling()
