request_schedule_url_a = "https://dnevnik.ru/api/userfeed/persons/1000016690040/schools/1000008291793/groups" \
                         "/1847065517303242479/schedule? "  # request link like that(ctrl + shift + i -> network ->
# choose schedule -> take request link)
auth_a = {
    "login": "",  # login A group account
    "password": ""  # password A group account
}

request_schedule_url_b = "https://dnevnik.ru/api/userfeed/persons/1000016690052/schools/1000008291793/groups" \
                         "/1847065517303242479/schedule? "  # like upper guide
auth_b = {
    "login": "",  # login B group account
    "password": ""  # password B group account
}

TOKEN = ""  # vkbot token
LINK = ""  # link to dialog with bot
ADMIN_ID = []  # vk ids who can send schedule

USER_LIST = []  # users who take schedule
