import telebot
from django.contrib.auth.models import User
from telebot import types
from django.core.management.base import BaseCommand
from ertelapp import settings
from task.controllers.bot_controller import BotController


class Command(BaseCommand):
    help = "Телеграм бот"

    def handle(self, *args, **options):
        pass


bot = telebot.TeleBot(settings.TOKEN_TG_BOT)
bot_controller = BotController()


@bot.message_handler(commands=["start"])
def start_message(message):
    user = User.objects.get(profile__chat_id=message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать задачу")
    btn2 = types.KeyboardButton("Указать местоположение", request_location=True)
    markup.add(btn1, btn2)
    bot.send_message(user.profile.chat_id,
                     text="Привет ✌️!\nЯ бот компании ЭРТЕЛ, через меня тебе будут ставить задания.",
                     reply_markup=markup)


@bot.message_handler(content_types=["location"])
def show_location(message):
    user = User.objects.get(profile__chat_id=message.chat.id)
    tasks = bot_controller.get_tasks(user)

    if message.location is not None:
        bot_controller.set_location(message)

        for task in tasks:
            loc_mark = telebot.types.InlineKeyboardMarkup()
            loc_btn1 = telebot.types.InlineKeyboardButton(text="Убыл на объект", callback_data=f"loc:1:{task.id}")
            loc_btn2 = telebot.types.InlineKeyboardButton(text="Прибыл на объект", callback_data=f"loc:2:{task.id}")
            loc_btn3 = telebot.types.InlineKeyboardButton(text="Убыл с объекта", callback_data=f"loc:3:{task.id}")
            loc_mark.add(loc_btn1, loc_btn2)
            loc_mark.add(loc_btn3)
            message_task = f"{bot_controller.get_message(task)}"
            bot.send_message(user.profile.chat_id, text=message_task, parse_mode="HTML", reply_markup=loc_mark)

        @bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "loc")
        def show_tasks(call):
            task_id = call.data.split(":")[2]
            location_code = call.data.split(":")[1]
            msg_local = ""

            match location_code:
                case "1":
                    msg_local = "Вы убыли на объект"
                    bot_controller.create_work_task(task_id, "Убыл на объект")
                case "2":
                    msg_local = "Вы прибыли на объект"
                    bot_controller.create_work_task(task_id, "Прибыл на объект")
                case "3":
                    msg_local = "Вы убыли с объекта"
                    bot_controller.create_work_task(task_id, "Убыл с объекта")
                case _:
                    bot.send_message(call.message.chat.id, text="Поступили неправильные данные")

            bot.send_message(call.message.chat.id, msg_local)

        bot.send_message(message.chat.id, text=f"<b>Ваше местоположение:</b> "
                                               f"{bot_controller.get_location()}\n<b>Время отправки "
                                               f"сообщения:</b> {bot_controller.get_datetime()[0]} "
                                               f"{bot_controller.get_datetime()[1]}", parse_mode="HTML")


@bot.message_handler(content_types=["text"])
def edited_status_task(message):
    user = User.objects.get(profile__chat_id=message.chat.id)
    tasks = bot_controller.get_tasks(user)
    match message.text:
        case "Выбрать задачу":
            for task in tasks:
                status_mark = telebot.types.InlineKeyboardMarkup()
                status_mark.add(
                    telebot.types.InlineKeyboardButton(text="Выполняется", callback_data=f"status:1:{task.id}"),
                    telebot.types.InlineKeyboardButton(text="Выполнено", callback_data=f"status:2:{task.id}")
                )

                message_task = f"{bot_controller.get_message(task)}"
                bot.send_message(user.profile.chat_id, text=message_task, parse_mode="HTML", reply_markup=status_mark)

            @bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "status")
            def show_tasks(call):
                data_id = call.data.split(":")[2]
                status_code = call.data.split(":")[1]
                status = ""

                match status_code:
                    case "1":
                        status = "Выполняется"
                    case "2":
                        status = "Выполнено"
                    case _:
                        bot.send_message(user.profile.chat_id, text="Поступили неправильные данные")

                task = bot_controller.get_find_task(data_id)
                bot_controller.set_status_task(status, task)
                message_updated_task = bot_controller.get_message(task)

                bot.send_message(call.message.chat.id, text=f"Статус задачи {task.id} изменен на\n<b>{status}</b>",
                                 parse_mode="HTML")
                bot.send_message(call.message.chat.id, text=message_updated_task, parse_mode="HTML")
        case _:
            msg = "Используйте кнопки для взаимодействия со мной!"
            bot.send_message(user.profile.chat_id, text=msg)


bot.infinity_polling()
