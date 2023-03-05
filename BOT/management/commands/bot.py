import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta

from .db import BotRaspDB
from .rasp import BotRasp, BotResponce
from django.core.management.base import BaseCommand
from django.conf import settings
class Command(BaseCommand):
    help = 'BotRASP'

    def handle(self, *args, **options):
        print('Bot start')

BotRaspDB = BotRaspDB('db.sqlite3')
bot = telebot.TeleBot(settings.TOKEN)

x = globals()
usid = []

mnths = {
    1: 'Января',
    2: 'Февраля',
    3: 'Марта',
    4: 'Апреля',
    5: 'Мая',
    6: 'Июня',
    7: 'Июля',
    8: 'Августа',
    9: 'Сентября',
    10: 'Октября',
    11: 'Ноября',
    12: 'Декабря',
}

timeObjects = {
    1: '8:30-10:00',
    2: '10:20-11:50',
    3: '12:25-13:55',
    4: '14:05-15:35',
    5: '15:45-17:00',
}

@bot.message_handler(commands=['start'])
def start(message):
    responceText = """
Привет, Я умный помощник по расписанию ТСПК.
Ниже показаны все команды, которые я могу исполнять:

Расписание:
/rasp - Расписание на сегодняшний день
/trasp - Расписание на завтра
/orasp - Расписание на какое то другое число

Группа:
/mygroup - Установленная группа
/setgroup - Установить группу для поиска
/chgroup - Изменить группу

Поиск:
/search - Поиск в расписании на сегодняшнее число
/osearch - Поиск в расписании на другое число

/help - Для всех существующих команд

Так же я могу присылать тебе свежее расписание как только оно появится!
Чтобы отключить данную функцию просто напиши мне /raspalerts
    """
    bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    responceText = """
    Ниже показаны все команды, которые я могу исполнять:

Расписание:
/rasp - Расписание на сегодняшний день
/trasp - Расписание на завтра
/orasp - Расписание на какое то другое число

Группа:
/mygroup - Установленная группа
/setgroup - Установить группу для поиска
/chgroup - Изменить группу

Поиск:
/search - Поиск в расписании на сегодняшнее число
/osearch - Поиск в расписании на другое число

/help - Для всех существующих команд

Так же я могу присылать тебе свежее расписание как только оно появится!
Чтобы отключить данную функцию просто напиши мне /raspalerts
    """
    bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['rasp'])
def rasp(message):
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = BotResponce.noGroup()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    elif BotRasp.raspUrl() == '#norasp':
        responceText = BotResponce.noRasp()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        try:
            group = BotRaspDB.get_user_group(message.from_user.id)
            listName = BotRasp.resRasp(BotRasp.raspUrl(), group)
            responceText = (f"&#128198 {date.today().day} {mnths[date.today().month]} {date.today().year}г\n"
                            f"&#128195 Группа: {group}\n")
            num = 1
            for i in range(0, 5):
                if type(listName[i]) != float:
                    responceText += f"{num} |{timeObjects[num]}| {listName[i]} \n"
                else:
                    responceText += f"{num} |{timeObjects[num]}|  \n"
                num += 1
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Ссылка на Google', url=BotRasp.raspUrl()))
            bot.send_message(message.chat.id, responceText, parse_mode='html', reply_markup=markup)
        except:
            responceText = BotResponce.requestError()
            bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['trasp'])
def trasp(message):
    NextDate = date.today() + timedelta(days=1)
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = BotResponce.noGroup()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    elif BotRasp.raspUrl(NextDate) == '#norasp':
        responceText = BotResponce.noRasp()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        try:
            group = BotRaspDB.get_user_group(message.from_user.id)
            listName = BotRasp.resRasp(BotRasp.raspUrl(NextDate), group)
            responceText = (f"&#128198 {NextDate.day} {mnths[NextDate.month]} {NextDate.year}г\n"
                            f"&#128195 Группа: {group}\n")
            num = 1
            for i in range(0, 5):
                if type(listName[i]) != float:
                    responceText += f"{num} |{timeObjects[num]}| {listName[i]} \n"
                else:
                    responceText += f"{num} |{timeObjects[num]}|  \n"
                num += 1
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Ссылка на Google', url=BotRasp.raspUrl(NextDate)))
            bot.send_message(message.chat.id, responceText, parse_mode='html', reply_markup=markup)
        except:
            responceText = BotResponce.requestError()
            bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['orasp'])
def orasp(message):
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = BotResponce.noGroup()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        usid.append(message.from_user.id)
        calendar = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Выберите год:", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберите месяц и день",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        if BotRasp.raspUrl(result) == False:
            responceText = BotResponce.bigDate()
            bot.edit_message_text(responceText, c.message.chat.id, c.message.message_id, parse_mode='html')
        elif BotRasp.raspUrl(result) == '#norasp':
            responceText = BotResponce.noRasp()
            bot.edit_message_text(responceText, c.message.chat.id, c.message.message_id, parse_mode='html')
        else:
            try:
                group = BotRaspDB.get_user_group(usid[0])
                listName = BotRasp.resRasp(BotRasp.raspUrl(result), group)
                responceText = (f"&#128198 {result.day} {mnths[result.month]} {result.year}г\n"
                                f"&#128195 Группа: {group}\n")
                num = 1
                for i in range(0, 5):
                    if type(listName[i]) != float:
                        responceText += f"{num} |{timeObjects[num]}| {listName[i]} \n"
                    else:
                        responceText += f"{num} |{timeObjects[num]}|  \n"
                    num += 1
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Ссылка на Google', url=BotRasp.raspUrl(result)))
                bot.edit_message_text(responceText, c.message.chat.id, c.message.message_id, parse_mode='html', reply_markup=markup)
            except:
                responceText = BotResponce.requestError()
                bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['setgroup'])
def setgroup(message):
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = ("\n"
                f"&#128195 Сейчас у тебя нет группы, но давай это исправим!\n"
                "Напишите мне группу в которую ты хочешь, чтобы я тебя добавил\n"
                "Например: <i>ИСиП-42</i>\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')
        bot.register_next_step_handler(message, set_group)
    else:
        responceText = ("\n"
                f"&#128195 У тебя уже установленна группа!\n"
                "Чтобы её поменять используй - /chgroup \n"
                "Подробнее - /help\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')


def set_group(message):
    if BotRaspDB.add_user(message.text, message.from_user.id, message.from_user.username):
        responceText = ("\n"
                f"&#128195 Я успешно установил твою группу!"
                f" Теперь ты в группе <b>{message.text}</b>\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = BotResponce.requestError()
        bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['mygroup'])
def mygroup(message):
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = BotResponce.noGroup()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = ("\n"
                f"&#128195 Установленная для поиска группа - <b>{BotRaspDB.get_user_group(message.from_user.id)}</b>\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['chgroup'])
def chgroup(message):
    if BotRaspDB.user_exists(message.from_user.id) == False:
        responceText = BotResponce.noGroup()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = ("\n"
                f"&#128195 Установленная для поиска группа - <b>{BotRaspDB.get_user_group(message.from_user.id)}</b>\n"
                "&#129302 Напишите мне группу на которую мне следует поменять\n"
                "<i>Например: ИСиП-42</i>\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')
        bot.register_next_step_handler(message, change_group)


def change_group(message):
    if BotRaspDB.change_user_group(message.text, message.from_user.id):
        responceText = ("\n"
                f"&#128195 Я успешно обновил твою группу!"
                f"Теперь ты в группе: <b>{message.text}</b>\n"
                "        ")
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = BotResponce.requestError()
        bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['search'])
def search(message):
    responceText = ("\n"
            "&#129302 Напишите параметр поиска\n"
            "Например: <i>Атаманюк</i> или <i>207</i>\n"
            "        ")
    bot.send_message(message.chat.id, responceText, parse_mode='html')
    bot.register_next_step_handler(message, srch_result)


def srch_result(message):
    try:
        responceText = ("\n"
                        f"&#129302 Это пока что не доступно!\n"
                        f"Но я совершенствуюсь каждый день!\n"
                        "        ")
        #responceText = BotRasp.srchRasp(BotRasp.raspUrl(), message.text)
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    except:
        responceText = BotResponce.requestError()
        bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['osearch'])
def osearch(message):
    responceText = ("\n"
            f"&#129302 Это пока что не доступно!\n"
            f"Но я совершенствуюсь каждый день!\n"
            "        ")
    bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['raspalerts'])
def raspalerts(message):
    if BotRaspDB.get_user_alertStatus(message.from_user.id) == '1':
        responceText = BotResponce.alertsOn()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = BotResponce.alertsOff()
        bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['startrasp'])
def startrasp(message):
    if BotRaspDB.get_user_alertStatus(message.from_user.id) == '1':
        responceText = BotResponce.alertsStatusOn()
        bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        try:
            BotRaspDB.on_user_alertStatus(message.from_user.id)
            responceText = BotResponce.alertsOn()
            bot.send_message(message.chat.id, responceText, parse_mode='html')
        except:
            responceText = BotResponce.requestError()
            bot.send_message(message.chat.id, responceText, parse_mode='html')


@bot.message_handler(commands=['stoprasp'])
def stoprasp(message):
    if BotRaspDB.get_user_alertStatus(message.from_user.id) == '1':
        try:
            BotRaspDB.off_user_alertStatus(message.from_user.id)
            responceText = BotResponce.alertsOff()
            bot.send_message(message.chat.id, responceText, parse_mode='html')
        except:
            responceText = BotResponce.requestError()
            bot.send_message(message.chat.id, responceText, parse_mode='html')
    else:
        responceText = BotResponce.alertsStatusOff()
        bot.send_message(message.chat.id, responceText, parse_mode='html')


bot.polling(none_stop=True)