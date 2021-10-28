import datetime as dt
import json
import webbrowser as wb

import requests
from vkbottle import Bot, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message

from const import *

# Словарь для перевода числа в месяц
month_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}

day_dict = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб",
}

schedule = None
user_list = []


# Получить расписание ##################################################################################################
def get_schedule(date, auth, request):
    # Авторизация на сайте (адрес страницы, параметры юзер агента, логин и пароль)
    url = "https://login.dnevnik.ru/login/esia/tomsk"

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76"
    }

    s = requests.Session()  # Создаем объект сессии
    s.post(url, data=auth, headers=header)  # Отправляем запрос на авторизацию группа А

    # Указываем запрос и параметры к запросу

    params = {
        "date": f"{date}",
        "takeDays": "1"
    }
    # Получаем расписание на один день
    schedule_dict = json.loads(s.get(request, params=params).text)  # Получаем расписание по запросу
    lesson = schedule_dict['days'][0]['lessons']  # Отрезаем список уроков

    return get_txt(lesson)


###################
def get_txt(lesson):
    dict = ''
    for elem in lesson:
        if elem['id'] == '0' or elem["isCanceled"] == True:

            continue
        else:  # Проходимся по всему списку с данными уроков
            number = elem['number']  # Номер занятия
            place = elem['place']  # Кабинет
            start_time = elem['hours']['startHour'] + ":" + elem['hours']['startMinute']  # Время начала пары
            end_time = elem['hours']['endHour'] + ":" + elem['hours']['endMinute']  # Время конца пары
            subject = elem['subject']['name']
            row = f"{number}. {subject}({place}) [{start_time} - {end_time}]"  # Объединяем
            dict += f"{row}\n"
    return dict


def check_equality(a, b):
    dict = []
    if a == b:
        dict.append(a)
    else:
        dict.append(a)
        dict.append(b)

    make_schedule(dict)


def make_schedule(dict):
    global schedule
    if len(dict) == 1:

        schedule += f"""Общее расписание
        
{dict[0]}"""
    else:
        schedule += f"""Группа А

{dict[0]}

Группа Б

{dict[1]}
"""
    print(schedule)


########################################################################################################################


bot = Bot(token=token)

# Пользовательская клавиатура
keyboard_user = (
    Keyboard(one_time=False, inline=False)
        .add(Text("Расписание", payload={"command": 3}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Рассылка", payload={"command": 3}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
)
keyboard_auth = (
    Keyboard(one_time=False, inline=False)

        .add(Text("Расписание", payload={"command": 3}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Отключить рассылку", payload={"command": 3}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
)
keyboard_admin = (
    Keyboard(one_time=False, inline=False)
        .add(Text("Расписание", payload={"command": 3}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Обновить расписание", payload={"button": 2}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Отправить", payload={"button": 1}), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
)


###############################################################################################

@bot.on.private_message(payload={"button": 1})
async def mailing(message: Message):
    global schedule, user_list
    await bot.api.messages.send(peer_ids=user_list, message=schedule, random_id=0)


@bot.on.private_message(payload={"button": 2})
async def reload(message: Message):
    await bot.api.messages.set_activity(message.peer_id, "typing")

    global schedule
    tomorrow = dt.datetime.now().date() + dt.timedelta(days=1)
    if dt.datetime.weekday(tomorrow) == 6:
        tomorrow += dt.timedelta(days=1)

    intTomorrow = int(tomorrow.strftime("%s")) + 25200
    schedule = f"""Расписание на  {day_dict[dt.datetime.weekday(tomorrow)]}   {tomorrow}

"""
    a = get_schedule(intTomorrow, auth_a, request_schedule_url_a)
    b = get_schedule(intTomorrow, auth_b, request_schedule_url_b)
    check_equality(a, b)

    await message.answer("Обновил текст")


#############################################################################
@bot.on.private_message(text="Расписание")
async def send_schedule(message: Message):
    await bot.api.messages.set_activity(message.peer_id, "typing")
    global schedule
    await message.answer(schedule)


###############################################################################################
@bot.on.private_message(text=['Рассылка', 'рассылка'])
async def reg(message: Message):
    global user_list
    if message.peer_id in ADMIN_ID:
        await message.answer('Ты меня не троль', keyboard=keyboard_admin)
    elif message.peer_id in user_list:
        await message.answer("У вас уже подключена рассылка", keyboard=keyboard_auth)
    else:
        user_list.append(message.peer_id)
        await message.answer("Вам подключена рассылка", keyboard=keyboard_auth)


###############################################################################################
@bot.on.private_message(text=['Отключить рассылку', 'отключить рассылку', 'отключить'])
async def reg(message: Message):
    await bot.api.messages.set_activity(message.peer_id, "typing")
    global user_list

    if message.peer_id in ADMIN_ID:
        await message.answer('Ты меня не троль', keyboard=keyboard_admin)
    elif message.peer_id in user_list:
        user_list.remove(message.peer_id)
        await message.answer("Вы отключили рассылку", keyboard=keyboard_user)
    else:
        await message.answer("У вас не было рассылки", keyboard=keyboard_user)


###############################################################################################
@bot.on.private_message()
async def reg(message: Message):
    await bot.api.messages.set_activity(message.peer_id, "typing")
    global user_list
    if message.peer_id in ADMIN_ID:
        await message.answer('''Приветствую, хозяин''', keyboard=keyboard_admin)
    elif message.peer_id in user_list:
        await message.answer("da", keyboard=keyboard_auth)
    else:
        await message.answer("da", keyboard=keyboard_user)


###############################################################################################
wb.open_new_tab('https://vk.com/im?sel=-204089367')

bot.run_forever()
