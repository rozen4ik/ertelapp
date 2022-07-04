import telebot
import datetime
from telebot import types
from django.core.management.base import BaseCommand
from ertelapp import settings
from task.models import *
from dadata import Dadata

bot = telebot.TeleBot(settings.TOKEN_TG_BOT)


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
    btn4 = types.KeyboardButton("Выехал на объект", request_location=True)
    btn5 = types.KeyboardButton("Прибыл на объект", request_location=True)
    btn6 = types.KeyboardButton("Убыл с объекта", request_location=True)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, text="Привет ✌️!\nЯ бот компании ЭРТЭЛ, через меня тебе будут ставить задания.", reply_markup=markup)


# Функционал для работы с местоположением и фиксацией времени
@bot.message_handler(content_types=['location'])
def location_message(message):
    token_dadata = settings.TOKEN_DADATA
    dadata = Dadata(token_dadata)
    result = dadata.geolocate(name="address", lat=message.location.latitude, lon=message.location.longitude, count=1)
    result = result[0]
    if message.location is not None:
        user = User.objects.all().select_related("profile")
        user = user.filter(profile__chat_id=message.chat.id)
        end_task = Task.objects.filter(employee_task=f"{user[0].first_name} {user[0].last_name}").latest("id")
        dt_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
        work_task = WorkTask()
        work_task.date_work_task = dt_message[0]
        work_task.time_work_task = dt_message[1]
        work_task.employee_work_task = f"{user[0].first_name} {user[0].last_name}"
        work_task.address_work_task = result["value"]
        work_task.task_id = end_task.id
        work_task.save()
        bot.send_message(message.chat.id, parse_mode="HTML", text=f"<b>Ваше местоположение:</b> {result['value']}\n<b>Время отправки сообщения:</b> {dt_message[0]} {dt_message[1]}")
    else:
        bot.send_message(message.chat.id, parse_mode="HTML", text="Не удалось отправить ваше местонахождение")


# Обработка команд подоваемых пользователем боту для изменения состояния статуса задачи
@bot.message_handler(content_types=['text'])
def task_message(message):
    user = User.objects.all().select_related("profile")
    user = user.filter(profile__chat_id=message.chat.id)
    end_task = Task.objects.filter(employee_task=f"{user[0].first_name} {user[0].last_name}").latest("id")
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
