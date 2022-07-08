import telebot
import datetime
from django.db.models import Q
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


def get_message(task):
    message_task = f"<b>Номер задачи:</b> {task.id}\n<b>Дата:</b> " \
                   f"{task.date_task}\n<b>Время:</b> {task.time_task}\n<b>Кто поручил:</b> " \
                   f"{task.author_task}\n<b>Статус задачи:</b> {task.status_task}\n<b>Задача:</b> " \
                   f"{task.text_task}\n<b>Место выполнения:</b> {task.address_task}\n" \
                   f"<b>Сроки выполнения:</b> {task.line_task}"
    return message_task


def find_task(o_task, task_id):
    task = o_task.objects.get(id=task_id)
    return task


find_task_id = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выполняется")
    btn2 = types.KeyboardButton("Выполнено")
    btn3 = types.KeyboardButton("Указать местоположение", request_location=True)
    btn4 = types.KeyboardButton("Выбрать задачу")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Привет ✌️!\nЯ бот компании ЭРТЭЛ, через меня тебе будут ставить задания.",
                     reply_markup=markup)


# Функционал для работы с местоположением и фиксацией времени
@bot.message_handler(content_types=['location'])
def location_message(message):
    dt_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
    token_dadata = settings.TOKEN_DADATA
    dadata = Dadata(token_dadata)
    result = dadata.geolocate(name="address", lat=message.location.latitude, lon=message.location.longitude, count=1)
    result = result[0]
    if message.location is not None:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выехал на объект', callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='Прибыл на объект', callback_data=2))
        markup.add(telebot.types.InlineKeyboardButton(text='Убыл с объекта', callback_data=3))

        def create_row_work_tas(status):
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
            user = User.objects.all().select_related("profile")
            user = user.get(profile__chat_id=message.chat.id)
            end_task = Task.objects.filter(employee_task=f"{user.first_name} {user.last_name}").latest("id")
            end_task_fullname = end_task.employee_task
            work_task = WorkTask()
            work_task.date_work_task = dt[0]
            work_task.time_work_task = dt[1]
            work_task.employee_work_task = f"{end_task_fullname}"
            work_task.address_work_task = result["value"]
            work_task.task_id = end_task.id
            work_task.status_work_task = status
            work_task.save()

        # Обработка статуса работника относительно местоположения
        @bot.callback_query_handler(func=lambda call: True)
        def status_local(call):
            bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
            answer = ''
            if call.data == '1':
                answer = 'Вы убыли на объект'
                create_row_work_tas("Выехал на объект")
            elif call.data == '2':
                answer = 'Вы прибыли на объект'
                create_row_work_tas("Прибыл на объект")
            elif call.data == '3':
                answer = 'Вы убыли с объекта'
                create_row_work_tas("Убыл с объекта")
            bot.send_message(call.message.chat.id, answer)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        bot.send_message(message.chat.id, parse_mode="HTML",
                         text=f"<b>Ваше местоположение:</b> {result['value']}\n<b>Время отправки сообщения:</b> "
                              f"{dt_message[0]} {dt_message[1]}",
                         reply_markup=markup)
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
        if find_task_id == 0:
            end_task.status_task = "Выполняется"
            end_task.save()
            end_task = Task.objects.filter(employee_task=f"{end_task_firstname} {end_task_lastname}").latest("id")
            message_task = get_message(end_task)
        else:
            end_task = find_task(Task, find_task_id)
            end_task.status_task = "Выполняется"
            end_task.save()
            end_task = find_task(Task, find_task_id)
            message_task = get_message(end_task)
            print(end_task)

        bot.send_message(message.chat.id, text=f"Статус задачи {end_task.id} изменен на\n<b>Выполняется</b>",
                         parse_mode="HTML")
        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML")
    elif message.text == "Выполнено":
        if find_task_id == 0:
            end_task.status_task = "Выполнено"
            end_task.save()
            end_task = Task.objects.filter(employee_task=f"{end_task_firstname} {end_task_lastname}").latest("id")
        else:
            end_task = find_task(Task, find_task_id)
            end_task.status_task = "Выполнено"
            end_task.save()
            end_task = find_task(Task, find_task_id)
        message_task = get_message(end_task)
        bot.send_message(message.chat.id, text=f"Статус задачи {end_task.id} изменен на\n<b>Выполнено</b>",
                         parse_mode="HTML")
        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML")
    elif message.text == "Выбрать задачу":
        mark = telebot.types.InlineKeyboardMarkup()
        tasks = Task.objects.filter(Q(status_task="Выполняется") | Q(status_task="Отдано в разработку"),
                                    employee_task=f"{end_task_firstname} {end_task_lastname}")
        message_task = ""
        for task in tasks:
            mark.add(
                telebot.types.InlineKeyboardButton(text=f"Переключиться на задачу №{task.id}", callback_data=task.id))

            message_task += "-----------------------"
            message_task += f"{get_message(task)}\n"

        @bot.callback_query_handler(func=lambda call: True)
        def all_my_task(call):
            tasker = Task.objects.get(id=call.data)
            global find_task_id
            find_task_id = tasker.id
            tasker.save()

            answer = f"{get_message(tasker)}\n"

            bot.send_message(call.message.chat.id, text=f"Выбрана задача №{tasker.id}")
            bot.send_message(call.message.chat.id, answer, parse_mode="HTML")

        bot.send_message(message.chat.id, text=message_task, parse_mode="HTML", reply_markup=mark)


bot.infinity_polling()
