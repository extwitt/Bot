import json
from gettext import find
from io import BytesIO

import telebot
from telebot import types
import requests
import bs4
import random
from time import sleep

from menuBot import Menu, Users
import DZ

bot = telebot.TeleBot('5250127657:AAHt1NuvGHkdcm3jmxLioOLwyK4FDIHaUXY')
game21 = None

def inputBot(message, text):
    a = []

    def ret(message):
        a.clear()
        a.append(message.text)
        return False

    a.clear()
    mes = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ret)
    while a == []:
        pass
    return a[0]

@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот Артёма на языке Python"
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAIPbGJq2ycHS3EKrG3rIAVgEb7eLT4xAAJ2DAACnGRhSfg32ECwVJVwJAQ')
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)

@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)

@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)

@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)

@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)

@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")

@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)

@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21

    chat_id = message.chat.id
    ms_text = message.text

    cur_user = Users.getUser(chat_id)
    if cur_user == None :
        cur_user = Users(chat_id, message.json["from"])

    result = goto_menu(chat_id, ms_text)
    if result :
        return

    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:
        cur_user.set_cur_menu(ms_text)

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка")

        elif ms_text == "Прислать лису":
            bot.send_photo(chat_id, photo=get_Cat())

        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == "Прислать фильм":
            send_film(chat_id)

        elif ms_text == "мЭЭм":
            im = get_lol()
            bot.send_photo(chat_id, photo=im[0])



        elif ms_text == "Задание 1" :
            DZ.dz1(bot, chat_id)
        elif ms_text == "Задание 2" :
            DZ.dz2(bot, chat_id)
        elif ms_text == "Задание 3" :
            DZ.dz3(bot, chat_id)
        elif ms_text == "Задание 4,5" :
            DZ.dz45(bot, chat_id)
        elif ms_text == "Задание 6" :
            DZ.dz6(bot, chat_id)
        elif ms_text == "Задание 7.1" :
            DZ.dz7n(bot, chat_id)
        elif ms_text == "Задание 7.2":
            DZ.dz7a(bot, chat_id)
        elif ms_text == "Задание 8" :
            DZ.dz8(bot, chat_id)
        elif ms_text == "Задание 9.1" :
            DZ.dz91(bot, chat_id)
        elif ms_text == "Задание 9.2" :
            DZ.dz92(bot, chat_id)
        elif ms_text == "Задание 10" :
            DZ.dz10(bot, chat_id)

    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду:" + ms_text)
        goto_menu(chat_id, "Главное меню")




@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    pass
    if call.data == "ManorNot_GoToSite":
        bot.answer_callback_query(call.id)


def goto_menu(chat_id, name_menu):
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "⬅ Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None :
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        return True
    else:
        return False





def send_help(chat_id) :
    global bot
    bot.send_message(chat_id, "Автор: Ямолова Софья")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору",
                                      url="https://t.me/ex_twitt")
    markup.add(btn1)
    img = open("котейка.jpg", 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)



def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["Фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


def get_randomFilm() :
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1 :
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]
    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["Фильм_url"] = url + details[7].contents[0]["href"]
    return infoFilm


def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200 :
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find :
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0 :
        return array_anekdots[0]
    else :
        return ""


def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json["url"]
    return url


def get_Cat():
    url1 = ""
    req1 = requests.get('https://randomfox.ca/floof/')
    if req1.status_code == 200:
        r_json1 = req1.json()
        url1 = r_json1["link"]
    return url1

def get_lol():
    req_anime = requests.get('https://www.anekdot.ru/random/mem/')
    soup = bs4.BeautifulSoup(req_anime.text, "html.parser")
    result_find = soup.find("div", class_="col-left col-left-margin")

    im = []
    for img in result_find.findAll("img"):
        im.append(img.get("src"))
    return im



bot.polling(none_stop=True, interval=0)

print()