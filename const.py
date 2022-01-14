request_schedule_url_a = "https://dnevnik.ru/api/userfeed/persons/1000016690040/schools/1000008291793/groups" \
                         "/1847065517303242479/schedule?"  # request link like that(ctrl + shift + i -> network ->
# choose schedule -> take request link)
auth_a = {
    "login": "example",  # login A group account
    "password": "example"  # password A group account
}

request_schedule_url_b = "https://dnevnik.ru/api/userfeed/persons/1000016690052/schools/1000008291793/groups" \
                         "/1847065517303242479/schedule?"  # like upper guide
auth_b = {
    "login": "example",  # login B group account
    "password": "example"  # password B group account
}

TOKEN = "example"  # vkbot token
LINK = "example"  # link to dialog with bot
ADMIN_ID = []  # vk ids who can send schedule


# don`t touch this
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
from json import load

with open('userList.json') as f:
    user_list = load(f)