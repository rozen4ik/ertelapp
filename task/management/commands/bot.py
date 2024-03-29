import telebot
from django.contrib.auth.models import User
from telebot import types
from django.core.management.base import BaseCommand
from ertelapp import settings
from task.services.bot_service import BotService
from dadata import Dadata


class Command(BaseCommand):
    help = "Телеграм бот"

    def handle(self, *args, **options):
        pass


bot = telebot.TeleBot(settings.TOKEN_TG_BOT)
bot_service = BotService()


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
    tasks = bot_service.get_tasks(user)
    count_task = tasks.count()

    if message.location is not None:
        bot_service.set_location(message)
        my_location = message

        match my_location:
            case "Местоположение":
                my_location = "Местоположение не определено"
            case _:
                token_dadata = settings.TOKEN_DADATA
                dadata = Dadata(token_dadata)
                result = dadata.geolocate(name="address", lat=my_location.location.latitude,
                                          lon=my_location.location.longitude, count=1)
                result = result[0]
                result = result["value"]
                my_location = result

        for task in tasks:
            loc_mark = telebot.types.InlineKeyboardMarkup()
            loc_btn1 = telebot.types.InlineKeyboardButton(text="Убыл на объект", callback_data=f"loc:1:{task.id}")
            loc_btn2 = telebot.types.InlineKeyboardButton(text="Прибыл на объект", callback_data=f"loc:2:{task.id}")
            loc_btn3 = telebot.types.InlineKeyboardButton(text="Убыл с объекта", callback_data=f"loc:3:{task.id}")
            loc_mark.add(loc_btn1, loc_btn2)
            loc_mark.add(loc_btn3)
            message_task = f"{bot_service.get_message(task)}"
            bot.send_message(user.profile.chat_id, text=message_task, parse_mode="HTML", reply_markup=loc_mark)

        bot.send_message(user.profile.chat_id, text=f"Всего задач: {count_task}")

        @bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "loc")
        def show_tasks(call):
            task_id = call.data.split(":")[2]
            location_code = call.data.split(":")[1]
            msg_local = ""

            match location_code:
                case "1":
                    msg_local = "Вы убыли на объект"
                    bot_service.create_work_task(task_id, "Убыл на объект")
                case "2":
                    msg_local = "Вы прибыли на объект"
                    bot_service.create_work_task(task_id, "Прибыл на объект")
                case "3":
                    msg_local = "Вы убыли с объекта. Не забудьте поставить отметку выполнено.\n" \
                                "Если задача не выполнена, а вы убываете с объекта, тогда напишите сообщение\n" \
                                "почему вы убываете, сообщение должно начинаться с фразы \"ЗАДАЧА Х ...\"\n" \
                                "где X это номер задачи, а ... примечание."
                    bot_service.create_work_task(task_id, "Убыл с объекта")
                case _:
                    bot.send_message(call.message.chat.id, text="Поступили неправильные данные")

            bot.send_message(call.message.chat.id, msg_local, parse_mode="HTML")

        bot.send_message(message.chat.id, text=f"<b>Ваше местоположение:</b> "
                                               f"{my_location}\n<b>Время отправки "
                                               f"сообщения:</b> {bot_service.get_datetime()[0]} "
                                               f"{bot_service.get_datetime()[1]}", parse_mode="HTML")


@bot.message_handler(content_types=["text"])
def edited_status_task(message):
    user = User.objects.get(profile__chat_id=message.chat.id)
    tasks = bot_service.get_tasks(user)
    count_task = tasks.count()
    match message.text:
        case "Выбрать задачу":
            for task in tasks:
                status_mark = telebot.types.InlineKeyboardMarkup()
                status_mark.add(
                    telebot.types.InlineKeyboardButton(text="Выполняется", callback_data=f"status:1:{task.id}"),
                    telebot.types.InlineKeyboardButton(text="Выполнено", callback_data=f"status:2:{task.id}"),
                )

                message_task = f"{bot_service.get_message(task)}"
                bot.send_message(user.profile.chat_id, text=message_task, parse_mode="HTML", reply_markup=status_mark)

            bot.send_message(user.profile.chat_id, text=f"Всего задач: {count_task}")

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

                task = bot_service.get_find_task(data_id)
                bot_service.set_status_task(status, task)
                bot_service.set_datetime_task(task)
                bot_service.create_history_status_task(task, status)
                message_updated_task = bot_service.get_message(task)

                bot.send_message(call.message.chat.id, text=f"Статус задачи {task.id} изменен на\n<b>{status}</b>",
                                 parse_mode="HTML")
                bot.send_message(call.message.chat.id, text=message_updated_task, parse_mode="HTML")
        case _:
            if message.text[0].lower() == "з":
                msg = message.text.split()[0].lower()
                number = message.text.split()[1]
                if msg == "задача" and number.isdigit():
                    number = int(number)
                    msg = message.text.split(" ", 2)[2].capitalize()
                    task = bot_service.get_find_task(number)
                    bot_service.set_note_task(task, msg)
                    bot_service.set_datetime_task(task)
                    bot_service.create_history_note_task(task, msg)
                    bot.send_message(user.profile.chat_id, text="Данные записаны.")
                else:
                    msg = "Используйте кнопки для взаимодействия со мной!"
                    bot.send_message(user.profile.chat_id, text=msg)
            else:
                msg = "Используйте кнопки для взаимодействия со мной!"
                bot.send_message(user.profile.chat_id, text=msg)


bot.infinity_polling()
