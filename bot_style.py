import requests

from setting import *
from file_img import *
from setting import TG_TOKEN

import os
import telebot
from telebot import types
from datetime import datetime
from telebot import TeleBot
import time

# import json
# import random

# # === обращение к БД Replit, поддержка работы 24/7
# import os
# from background import keep_alive  # #импорт функции для поддержки работоспособности
#
# from replit import db
# import base
#
# import pip
# pip.main(['install', 'pytelegrambotapi'])
#

# my_secret = os.environ['token']
# -----------------------------

bot = telebot.TeleBot(TG_TOKEN, skip_pending=True)

# -  - - - - - Объявление переменных
# ----Константы
id_support = '5170069430'

# --- Маркеры
add_marker = {}  # маркер добавления продукта

# !!!!!!!!!!!!!!!!!!!!!
style_marker = {}  # маркер стиля изображения

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

edit_marker = {}  # маркер кнопка Edit
alien_marker = {}  # маркер управление чужим списком
union_marker = {}  # маркер добавить целый список
share_marker = {}  # маркер расшаривания списка (изменение ID на список для просмотра)
back_marker = {}  # маркер вернуть позицию обратно в список
sms_marker = {}  # маркер написания СМС в поддержку от User
drop_id_marker = {}  # маркер удаления из Базы Данных по ID
serv_marker = {}  # маркер сервесный
avail_marker = {}  # маркер выбранного чужого списка

activ_list = {}  # маркер активного списка мой / общий  my/all

# ---Кнопки
share_but = {}  # кнопка расшарить свой список
friendly_but = {}  # кнопка доступные списки моих друзей
alien_but = {}  # кнопка ID кто имеет доступ к моим спискам
y_but = {}  # кнопка да
n_but = {}  # кнопка нет
up_but = {}  # кнопка обновить

# --- Словари


# if not dic_list:
#     dic_list = dict(base.out_dict_list())
# else:
#    pass
# ---------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dic_numb = {}  # название (номер) изображения для стиля
dic_img = {}   # название загруженного файла и размер

# !!!!!!!!!!!!!!!!!!!!!!!!!!
# if not dic_numb:
#     dic_numb = dict(base.out_dict_numb())
# else:
#    pass
# -----

dic_list_union = {}  # новый список из сообщения
dic_list_clear = {}  # список для удаления названий основного списка при "Заменить"
dic_alien_user = {}  # ID активного чужого списка (только одна пара Ключ(мой ID)=Значение(ID чужого списка))

dic_share = {}  # список ID-мой и ID-кому открыт доступ к списку
dic_availibale = {}  # список ID доступных списков для просмотра -> ID(кому открыт доступ): [ID кто предоставил]

list_user_id = {}  # список всех iD и логинов участников бота
# if not list_user_id:
#     list_user_id = dict(base.out_user_id())
# else:
#   pass
# -----------

# ---------------
# = = = Описание команд и функций
# --------------- вызов справки
HELP = """
Приветствую!✌️ 
Я Чат-Бот! Помогу сформировать список покупок, и отследить выполнение этого списка.
Нажми на кнопку ниже, что бы узнать функционал доступных команд и их описание:
©️
"""

# ©️®️™️
#  ---------------- описание вызываемых команд
TEAM = """✏️ Команды доступные в приложении:
/menu - (Menu, Меню) - Меню - список доступных команд приложения.
/help - (Нelp, Справка, ? ) - вызов справки о программе, знакомство с приложением.
/info - (Info, Описание) - описание действия команд и кнопок приложения.

/select - (Select, Выбор) - выбор доступных списков ( мой  / общий) !!!

/add - (Add, Добавить) -  добавить наименование в список покупок.
/show - (Show, Список) - вывод списка покупок.

/update - (Update, Обновить) - обновление списка покупок, убрать из списка уже отмеченные позиции.
/del - (Del, Удалить) -  удалить все наименования из списка.
/end - (End, Отмена, /) - отмена, завершение команды.


"""

# ----- Блок описания команд
Info = """
Описание действия кнопок приложения:
1. Добавить - добавление нового наименования в список покупок.
2. Редактировать - заменить одно наименование из списка на другое.
3. Отметить - вычеркнуть (отметить) уже купленную позицию из списка.
4. Обновить - обновление списка покупок, в списке остаются только не отмеченные позиции.
5. Удалить - удалить весь список покупок.
6. Вернуть - вернуть обратно в список ранее вычеркнутую позицию.
7. Завершить - завершение всех команд.
8. Новый список - создание нового списка для покупок.
"""

# ---Блок Управление списками: набор команд/описание
Management = """✏️ Команды доступные для управления списками:
/select - (Select, Выбор) - выбор доступных списков ( мой  / общий)

/add_all - создать общий список

/share - (Share, поделиться) -  поделиться своим списком с другими пользователями (создается копия текущего списка)

/friendly - списки моих друзей  (доступные мне для просмотра чужие списки)
/del_friendly  --> удалить список (user + login)//удалить все списки// посмотреть (выбрать для просмотра список)

/users ( /alien ) - пользователи, которые видят мой общий список
 /del_users - -> удалить пользователя//добавить//удалить всех (кнопки)
"""
# ----- Сервисные команды (только для разработчика)
SERV = """
/iduser - список всех участников чата
/idsms - отправка сообщений конкретному пользователю (??реализация чата между пользователями одного списка??)
/drop - очистка БД
/read - чтение всех списков
/management - (Management, управление) - управление списками, предоставление доступа другим пользователям к своим спискам 
/share - (Share, поделиться) -  поделиться своим списком1
/id - (Id, имя) - ID пользователя
"""


#  = = = Общие функции приложения
# ----- Отмена всех команд
def cancel_id(user_id):
    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0
    _text = f'❌ Неизвестная команда.'
    return _text

# ----- Нормализация всех словарей - проверка на существование
def normalization(user_id):
    if add_marker.get(user_id) is None:
        add_marker[user_id] = 0
    if tag_marker.get(user_id) is None:
        tag_marker[user_id] = 0
    if edit_marker.get(user_id) is None:
        edit_marker[user_id] = 0
    if union_marker.get(user_id) is None:
        union_marker[user_id] = 0
    if share_marker.get(user_id) is None:
        share_marker[user_id] = 0
    if back_marker.get(user_id) is None:
        back_marker[user_id] = 0
    if sms_marker.get(user_id) is None:
        sms_marker[user_id] = 0
    if serv_marker.get(id_support) is None:
        serv_marker[id_support] = 0
    if drop_id_marker.get(user_id) is None:
        drop_id_marker[user_id] = 0
    if avail_marker.get(user_id) is None:
        avail_marker[user_id] = 0
    if share_marker.get(user_id) is None:
        share_marker[user_id] = 0

# ----- Запись всех ID и Логинов в список Чат-Бота
def id_log(user_id, user_name, time_sms):
    time_sms = str(datetime.fromtimestamp(time_sms).strftime('%d.%m.%Y'))
    list_user_id[user_id] = [user_name, time_sms]
    # base.in_user_id(user_id, list_user_id[user_id])  # запись в БД Repl.it


# ----- подмена  user_id для чужого списка -возможно функция не нужна ===!!!!!!!!!
def alien_user(user_id):
    user_id = dic_alien_user[user_id][0]  # - подмена  user_id
    user_name_alien = list_user_id[user_id][0]
    return [user_id, user_name_alien]


# ----- Показать список
def show_list(user_id, activ):
    prod = ""
    j = 0  # для счета позиций списка
    for i in dic_list[user_id][activ]:
        j += 1
        Z = str(j)
        if dic_numb[user_id].get(activ) is not None:
            if Z in dic_numb[user_id][activ]:
                text2 = '~' + str(i) + '~'  # ✅  ✔️
                # text2 = '~' + str(j) + " " + str(i) + '~'  # ✅  ✔️
                prod = (f'{prod}✅ {j} {text2} \n')
            else:
                prod = (f'{prod} {j}  {i} \n')
        else:
            prod = (f'{prod} {j}  {i} \n')
    return prod

# ----- Проверка активного списка мой/ общий
def list_activ(user_id):
    if activ_list.get(user_id) is None:
        activ_list[user_id] = 'Мой'
    activ = activ_list[user_id]

    if dic_list.get(user_id) is None:
        dic_list[user_id] = {}
    if dic_numb.get(user_id) is None:
        dic_numb[user_id] = {}
    return activ

# --------------------------------------------------------------
# = = =  Сервисные команды

# my_id='5170069430'

# user_name = str(message.from_user.username) # имя
# user_Fname = message.from_user.first_name
# user_surname = message.from_user.last_name   # фио пользователя message.chat.id
# /ch=str("586115676")
# bot.send_message(ch, f'{user_id} , @{user_name} - { user_Fname} ') #сообщение уходит в чат другого пользователя -----!!!!!!!!!!!!!!!!!!
# bot.send_message(ch, "123") #сообщение уходит в чат другого пользователя

# ----- Список сервисных команд
@bot.message_handler(commands=["serv", "Serv", "SERV"])
def Serv(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    time_sms = message.date
    id_log(user_id, user_name, time_sms)
    text = cancel_id(user_id)

    if user_id == id_support:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Мой список', callback_data='show')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, SERV, reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# -----  список всех участников бота --> сервисная команда == ! ! !
@bot.message_handler(commands=["iduser", "IDuser", "Iduser", "IDUser"])
def ID_User(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    time_sms = message.date
    id_log(user_id, user_name, time_sms)
    text = cancel_id(user_id)

    if user_id == id_support:
        text = ""
        for key in list_user_id.keys():
            val_1 = list_user_id[key][0]
            val_2 = list_user_id[key][1]
            text = f'{text}{key} @{val_1} дата: {val_2} \n'
        bot.send_message(message.chat.id, text)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ----- Отправка SMS пользователям
@bot.message_handler(commands=["idsms", "IDSMS", "IDsms", "idSMS"])
def SMS_ID(message):
    user_id = str(message.from_user.id)
    text = cancel_id(user_id)

    if user_id == id_support:
        buttons = [
            types.InlineKeyboardButton('SMS по ID', callback_data='sms_id'),
            types.InlineKeyboardButton('SMS Всем', callback_data='sms_all')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Отправить SMS Одному пользователю или Всем участникам чата:',
                         reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ----- Чтение списков приложения
@bot.message_handler(commands=["read", "Read", "READ", "чтение"])
def read(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    time_sms = message.date
    id_log(user_id, user_name, time_sms)
    text = cancel_id(user_id)
    if user_id == id_support:
        buttons = [
            types.InlineKeyboardButton('Shop', callback_data='read_shop'),
            types.InlineKeyboardButton('Share', callback_data='read_share'),
            types.InlineKeyboardButton('Availibale', callback_data='read_avail'),
            types.InlineKeyboardButton('Numb', callback_data='read_numb'),
            types.InlineKeyboardButton('User ID', callback_data='read_userid'),
            types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Вывод списка из словарей:', reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ----- Список позиций - вывод отмеченных номеров списка
@bot.message_handler(commands=["numb"])
def Nomer_ID(message):
    text = ""
    user_id = str(message.from_user.id)
    text = cancel_id(user_id)  # - -Отмена всех команд

    # проверка активного списка мой/ общий
    activ = list_activ(user_id)

    if user_id == id_support:
        if dic_numb[user_id].get(activ) is None:
            bot.send_message(message.chat.id, 'Список номеров пуст')
        else:
            for i in dic_numb[user_id][activ]:
                text = text + i + "\n"
                bot.send_message(message.chat.id, text)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# # ----- Очистить всю БД только на ReplIT
# @bot.message_handler(commands=["drop","DROP","Drop"])
# def drop_BD(message):
#   for key in db.keys():
#     del db[key]
#   bot.send_message(message.chat.id, 'БД - очищена')

# ----- Очистить БД только на ReplIT
@bot.message_handler(commands=["drop", "DROP", "Drop"])
def drop_BD(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    time_sms = message.date
    id_log(user_id, user_name, time_sms)
    text = cancel_id(user_id)

    if user_id == id_support:
        # for key in db.keys():
        #   del db[key]
        # bot.send_message(message.chat.id, 'БД - очищена')

        buttons = [
            types.InlineKeyboardButton('Удалить по ID', callback_data='drop_id'),
            types.InlineKeyboardButton('Удалить все', callback_data='drop_all')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Что следует удалить из БД?',
                         reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ------------------------------------------------------------
# = = = Команды для управления приложением
# -----  Справка
@bot.message_handler(
    commands=["Справка", "СПРАВКА", "справка", "help", "Help", "HELP", "hElp", "heLp", "helP", "HElp", "HElP", "HELp",
              "hELp", "hELP", "heLp", "heLP", "?", "start"])  # регистрация фун-ции на сервере телеграмм
def help(message):
    user_id = str(message.from_user.id)  # id пользователя
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям

    # блок нормализации списков по ID пользователя
    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Новый список', callback_data='add')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, HELP, reply_markup=keyboard)


# ----- Меню
@bot.message_handler(commands=["menu", "MENU", "Menu", "меню", "Меню", "МЕНЮ", "мЕНЮ", "меНЮ", "менЮ"])
def menu(message):
    user_id = str(message.from_user.id)  # id пользователя
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям
    # блок нормализации списков по ID пользователя
    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Новый список', callback_data='add')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, TEAM, reply_markup=keyboard)

# ----- Инфо - описание команд и кнопок
@bot.message_handler(commands=["info", "INFO", "Info", "iNfo", "Описание", "описание", "ОПИСАНИЕ"])
def info(message):
    user_id = str(message.from_user.id)  # id пользователя
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям
    # блок нормализации списков по ID пользователя
    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Новый список', callback_data='add')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, Info, reply_markup=keyboard)


# -----показ стилей для изображения


#  ----- выбор стиля для переноса
@bot.message_handler(commands=["style", "STYLE", "Style", "Стиль", "стиль", "СТИЛЬ"])
def style_img(message):
    user_id = str(message.from_user.id)  # id пользователя
    # блок нормализации списков по ID пользователя
    style_marker[user_id] = 1

    add_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'Выберите изображение для переноса стиля:\n {text_style}', reply_markup=keyboard)

# -----Редактирвать список
@bot.message_handler(commands=["edit", "EDIT", "Edit", "Редактировать", "редактировать", "РЕДАКТИРОВАТЬ"])
def Edit(message):
    user_id = str(message.from_user.id)
    # блок нормализации списков по ID пользователя
    edit_marker[user_id] = 1

    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    # блок проверка управления чужим списком
    if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
        user_id = dic_alien_user[user_id][0]
        user_name_alien = list_user_id[user_id][0]
        text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
        # проверка активного списка мой/ общий
        activ = 'Общий'
    else:
        # проверка активного списка мой/ общий
        activ = list_activ(user_id)

        text_alien = f'{activ} список:\n'
    # -----

    # блок редактирование
    if dic_list[user_id].get(activ) is not None:
        text = R' Выберите номер в списке для изменения и укажите новое наименование (пример: "7 карандаш"):'
        bot.send_message(message.chat.id, text_alien + text)
    else:
        edit_marker[user_id] = 0
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f'{text_alien} ❗ Список покупок пуст.', reply_markup=keyboard)

# ----- Обновить (убрать из списка отмеченные позиции)
@bot.message_handler(commands=["update", "Update", "UPDATE", "Обновить", "обновить", "ОБНОВИТЬ"])
def Update(message):
    user_id = str(message.from_user.id)  # id

    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    # блок проверка управления чужим списком
    if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
        user_id = dic_alien_user[user_id][0]
        user_name_alien = list_user_id[user_id][0]
        text = "📝 Список покупок:\n"
        # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
        bot.send_message(message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
        # проверка активного списка мой/ общий
        activ = 'Общий'
    else:
        # проверка активного списка мой/ общий
        activ = list_activ(user_id)
        text = f'{activ} список:\n📝 Покупки на сегодня:\n'
    # -----

    text = "️♻ Список покупок: \n"
    if dic_list[user_id].get(activ) is not None:
        # убираем отмеченные элементы из списка
        j = 0  # для счета позиций списка
        dic_list_clear[user_id] = []
        for i in dic_list[user_id][activ]:
            j += 1
            Z = str(j)
            if dic_numb[user_id].get(activ) is not None:
                if Z in dic_numb[user_id][activ]:
                    dic_numb[user_id][activ].remove(Z)  # убираем отмеченный элемент(номер позиции) из списка
                    dic_list_clear[user_id].append(i)  # название продукта для удаления из списка
                else:
                    pass
            else:
                break
        if len(dic_list_clear[user_id]) > 0:
            for i in (dic_list_clear[user_id]):
                if i in dic_list[user_id][activ]:
                    dic_list[user_id][activ].remove(i)  # убираем название Продукта из списка
                else:
                    pass
        else:
            pass
        # --- вывод на экран
        prod = show_list(user_id, activ)  # функция показать список
        # ----- запись списка в базу
        # base.in_dict_list(user_id, dic_list[user_id])
        # base.in_dict_numb(user_id, dic_numb[user_id])
        # --------
        buttons = [
            types.InlineKeyboardButton('Добавить', callback_data='add'),
            types.InlineKeyboardButton('Отметить', callback_data='Ok'),
            types.InlineKeyboardButton('Редактировать', callback_data='edit'),
            types.InlineKeyboardButton('Обновить', callback_data='up'),
            types.InlineKeyboardButton('Удалить', callback_data='del'),
            types.InlineKeyboardButton('Вернуть', callback_data='back')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text + prod, parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

# ----- Отмена всех команд /end
@bot.message_handler(commands=["Отмена", "ОТМЕНА", "отмена", "end", "END", "End", "/"])
def end(message):
    user_id = str(message.from_user.id)

    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Новый список', callback_data='add'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

# ----- Добвить название в список
@bot.message_handler(commands=["add", "ADD", "Add", "добавить", "Добавить", "ДОБАВИТЬ"])
def add(message):
    user_id = str(message.from_user.id)  # id пользователя
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям

    add_marker[user_id] = 1

    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     f'Введите наименование продукта:', reply_markup=keyboard)

# ----- Добвить название в Общий список add_all
@bot.message_handler(commands=["add_all", "ADD_ALL", "Add_All"])
def add_all(message):
    user_id = str(message.from_user.id)  # id пользователя
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям

    add_marker[user_id] = 1

    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    activ_list[user_id] = 'Общий'
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     f'Введите наименование продукта:', reply_markup=keyboard)

# ----- Добавить целый список в лист покупок
@bot.message_handler(commands=["union", "Unioin", "UNIOIN", "Объеденить", "объеденить", "ОБЪЕДЕНИТЬ"])
def Union(message):
    user_id = str(message.from_user.id)
    union_marker[user_id] = 1

    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id,
                     f'Добавьте список покупок в этот чат:', reply_markup=keyboard)

# -----Просмотр списка
@bot.message_handler(commands=["show", "SHOW", "Show", "список", "Список", "СПИСОК"])
def show(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)  # Log пользователя
    time_sms = message.date
    id_log(user_id, user_name, time_sms)  # отметка ID и Log в словаре Бота по всем пользователям

    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    # блок проверка управления чужим списком
    if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
        user_id = dic_alien_user[user_id][0]
        user_name_alien = list_user_id[user_id][0]
        text = "📝 Список покупок:\n"
        # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien}\n'
        bot.send_message(message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
        # проверка активного списка мой/ общий
        activ = 'Общий'
    else:
        # проверка активного списка мой/ общий
        activ = list_activ(user_id)

        # text_alien = f'{activ} список:\n'
        # text = '📝 Покупки на сегодня:\n'

        text = f'{activ} список:\n📝 Покупки на сегодня:\n'
    # ------
    if dic_list[user_id].get(activ) is not None:
        prod = show_list(user_id, activ)  # функция показать список
        buttons = [
            types.InlineKeyboardButton('Добавить', callback_data='add'),
            types.InlineKeyboardButton('Отметить', callback_data='Ok'),
            types.InlineKeyboardButton('Редактировать', callback_data='edit'),
            types.InlineKeyboardButton('Обновить', callback_data='up'),
            types.InlineKeyboardButton('Удалить', callback_data='del'),
            types.InlineKeyboardButton('Вернуть', callback_data='back'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        # bot.send_message(message.chat.id, text + prod, parse_mode='MarkdownV2', reply_markup=keyboard)
        bot.send_message(message.chat.id, text + prod, parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

# ----- Очистка списка
@bot.message_handler(commands=["del", "Del", "dEl", "deL", "DEl", "DEL", "dEL", "Удалить", "удалить", "УДАЛИТЬ"])
def _del(message):
    user_id = str(message.from_user.id)
    add_marker[user_id] = 0
    tag_marker[user_id] = 0
    edit_marker[user_id] = 0
    union_marker[user_id] = 0
    share_marker[user_id] = 0
    back_marker[user_id] = 0
    sms_marker[user_id] = 0
    drop_id_marker[user_id] = 0
    serv_marker[user_id] = 0

    share_but[user_id] = 0
    friendly_but[user_id] = 0
    alien_but[user_id] = 0
    y_but[user_id] = 0
    n_but[user_id] = 0
    up_but[user_id] = 0

    # блок проверка управления чужим списком
    if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
        user_id = dic_alien_user[user_id][0]
        user_name_alien = list_user_id[user_id][0]
        text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
        # проверка активного списка мой/ общий
        activ = 'Общий'
    else:
        # проверка активного списка мой/ общий
        activ = list_activ(user_id)
        # -----
        text_alien = f'{activ} список:\n'

    if dic_list[user_id].get(activ) is not None:
        del dic_list[user_id][activ]
        # ----- запись списка в базу DEL
        # base.del_dict_list(user_id)
    if dic_numb[user_id].get(activ) is not None:
        del dic_numb[user_id][activ]
        # ----- запись списка в базу DEL
        # base.del_dict_numb(user_id)
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Новый список', callback_data='add'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f' {text_alien}🟢 Cписок покупок очищен.', reply_markup=keyboard)

# ----- получение фото
# @bot.message_handler(content_types=['photo'])
@bot.message_handler(content_types=['document', 'audio', 'video', 'photo'])
def photo(message):
     # fileID = message.photo[-1].file_id
     fileID = message.document.file_id if message.content_type == 'document' else \
         message.audio.file_id if message.content_type == 'audio' else \
             message.video.file_id if message.content_type == 'video' else \
                 message.photo[-1].file_id if message.content_type == 'photo' else None
     file_info = bot.get_file(fileID)
     file_extension = os.path.splitext(file_info.file_path)[-1].lower()

     # тип файла # bot.send_message(message.chat.id, f' 🟢 {file_extension}')
     if file_extension in ['.jpg', '.jpeg', '.png']:

        downloaded_file = bot.download_file(file_info.file_path)
        ph = message.photo[len(message.photo) - 1].file_id

        #  загрузка изображения
        text = f'img_{user_id}.jpg'
        with open( text , 'wb' ) as new_file:
            new_img = new_file.write(downloaded_file)

        #     размер исходного изображения
        in_img_size = img_size(text)
        #  название исходного файла и размер
        dic_img[user_id] = [text, in_img_size ]
        if dic_numb.get(user_id) is not None:
            a = '1'
        else:
            # изображения стиля не выбрано
            # предложить варианты стиля
            pass

        # bot.send_message(message.chat.id, f' получено размер🟢 {in_img_size}')
     else:
        bot.send_message(message.chat.id, f'отправиь картинку в Jpeg')

     #    отправить фото в ответ
     # bot.send_photo(message.chat.id, ph, caption='Ваш текст')


# ---------------------------------------------
# = = = Реагирование на кнопки = = =
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = str(call.from_user.id)
    message_id = call.message.message_id
    chat_id = call.message.chat.id

    # проверка активного списка мой/ общий
    activ = list_activ(user_id)

    if call.message:
        # ----- Выполнение кнопки "Отметить"
        if call.data == "Ok":
            tag_marker[user_id] = 1

            add_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                # user_name_alien = list_user_id[user_id][0]
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
            #  ---

            if dic_list[user_id].get(activ) is not None:
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Завершить', callback_data='cancel')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'Выберите номер из списка:', reply_markup=keyboard)

            else:
                tag_marker[user_id] = 0
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add'),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'❗ Список покупок пуст.', reply_markup=keyboard)

        #  Выполнение Кнопки Вернуть (в список отмеченную позицию)
        elif call.data == "back":
            back_marker[user_id] = 1

            tag_marker[user_id] = 0
            add_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                # user_name_alien = list_user_id[user_id][0]
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)

            if dic_list[user_id].get(activ) is not None:

                if dic_numb[user_id].get(activ) is not None:
                    buttons = [
                        types.InlineKeyboardButton('Меню', callback_data='menu'),
                        types.InlineKeyboardButton('Завершить', callback_data='cancel')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                    keyboard.add(*buttons)
                    bot.send_message(call.message.chat.id, f'Выберите номер из списка, который необходимо вернуть:',
                                     reply_markup=keyboard)
                else:
                    back_marker[user_id] = 0
                    buttons = [
                        types.InlineKeyboardButton('Меню', callback_data='menu'),
                        types.InlineKeyboardButton('Новый список', callback_data='add'),
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)
                    bot.send_message(call.message.chat.id, '⚠️ В списке нет отмеченных позиций.',
                                     reply_markup=keyboard)
            else:
                back_marker[user_id] = 0
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add'),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, '❗ Список покупок пуст.', reply_markup=keyboard)

        # ----- Выполнение кнопки "Редактировать"
        elif call.data == "edit":
            edit_marker[user_id] = 1

            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                # user_name_alien = list_user_id[user_id][0]
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)

            if dic_list[user_id].get(activ) is not None:
                text = R'Выберите номер в списке для изменения и укажите новое наименование (пример: "7 карандаш"):'
                bot.send_message(call.message.chat.id, text)
            else:
                edit_marker[user_id] = 0
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add'),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, '❗ Список покупок пуст.', reply_markup=keyboard)

        # --- Выполнение кнопки "Показать список" при совпадении продуктов
        elif call.data == 'double':
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                text = "📝 Список покупок:\n"
                # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
                bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                # text_alien = f'{activ} список:\n'
                text = f'{activ} список:\n📝 Покупки на сегодня:\n'
            # -----
            if dic_list[user_id].get(activ) is not None:
                prod = show_list(user_id, activ)  # функция показать список
                buttons = [
                    types.InlineKeyboardButton('Добавить', callback_data='add'),
                    types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                    types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                    types.InlineKeyboardButton('Удалить', callback_data='del')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2',
                                 reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

        # --------Выполнение Кнопка "Обновить"
        elif call.data == 'up':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
                bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                text = f'{activ} список:\n📝 Покупки на сегодня:\n'
            # ---
            if dic_list[user_id].get(activ) is not None:
                text = "️♻ Список покупок обновлен: \n"
                # убираем отмеченные элементы из списка
                j = 0  # для счета позиций списка
                dic_list_clear[user_id] = []
                for i in dic_list[user_id][activ]:
                    j += 1
                    Z = str(j)
                    if dic_numb[user_id].get(activ) is not None:
                        if Z in dic_numb[user_id][activ]:
                            dic_numb[user_id][activ].remove(Z)
                            dic_list_clear[user_id].append(i)  # название продукта для удаления из списка
                        else:
                            pass
                    else:
                        break
                if len(dic_list_clear[user_id]) > 0:
                    for i in (dic_list_clear[user_id]):
                        if i in dic_list[user_id][activ]:
                            dic_list[user_id][activ].remove(i)
                        else:
                            pass
                else:
                    pass
                # ---  Вывод на экран
                prod = show_list(user_id, activ)  # функция показать список
                # ----- запись списка в базу
                # base.in_dict_list(user_id, dic_list[user_id])
                # base.in_dict_numb(user_id, dic_numb[user_id])
                buttons = [
                    types.InlineKeyboardButton('Добавить', callback_data='add'),
                    types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                    types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                    types.InlineKeyboardButton('Обновить', callback_data='up'),
                    types.InlineKeyboardButton('Удалить', callback_data='del'),
                    types.InlineKeyboardButton('Вернуть', callback_data='back')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2',
                                 reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add'),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

        # ----- Кнопка Справка
        elif call.data == "help":
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            # bot.send_message(call.message.chat.id, HELP, reply_markup=keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=HELP, reply_markup=keyboard)

        # ----- Кнопка Управлять Списками
        elif call.data == "manage":
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, Management, reply_markup=keyboard)

        # -----Выполнение Кнопка "Отмена" - завершение всех команд
        elif call.data == "cancel":
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

        # -----Выполнение Кнопка "Удалить" список
        elif call.data == 'del':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                text_alien = f'{activ} список:\n'
            # -------
            if dic_list[user_id].get(activ) is not None:
                del dic_list[user_id][activ]
                # ----- запись списка в базу DEL
                # base.del_dict_list(user_id)
            if dic_numb[user_id].get(activ) is not None:
                del dic_numb[user_id][activ]
                # base.del_dict_numb(user_id)
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Создать новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, f'{text_alien}🟢 Список покупок очищен.', reply_markup=keyboard)
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{text_alien}🟢 Список покупок очищен.', reply_markup=keyboard)

        # ---- Кнопка не используется---------------! "NO"
        elif call.data == "N":
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            bot.send_message(call.message.chat.id, 'кнопка Нет: ')

        # ----- Выполнение кнопка "Меню"
        elif call.data == 'menu':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            # bot.send_message(call.message.chat.id, TEAM)
            buttons = [
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Справка', callback_data='help'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=TEAM,
                                  reply_markup=keyboard)

        # ----- Выполнение кнопка "Info" Описание команд
        elif call.data == 'info':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Справка', callback_data='help'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            # bot.send_message(call.message.chat.id, Info, reply_markup=keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Info, reply_markup=keyboard)

        # ----- Выполнение кнопка "Serv" Сервисные команды
        elif call.data == 'serv':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Мой список', callback_data='show')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, SERV, reply_markup=keyboard)

        # ----- Выполнение кнопка "Add" добавить в список
        elif call.data == 'add':
            add_marker[user_id] = 1

            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id,
                             f'Введите наименование продукта:', reply_markup=keyboard)

        # ---- Выполнение кнопка "Добавить целый список" из смс
        elif call.data == 'union_list':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                text = "📝 Список покупок:\n"
                # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
                bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                # text_alien = f'{activ} список:\n'
                text = f'{activ} список:\n📝 Покупки на сегодня:\n'

            # блок добавление списка
            if dic_list[user_id].get(activ) is not None:
                pass
            else:
                dic_list[user_id][activ] = []

            for i in dic_list_union[user_id]:
                _text = i.split(maxsplit=1)
                if len(_text) > 1:  # проверка на разделение списка
                    nomer = _text[0]
                    if nomer.isnumeric() == True:  # провкрка на число
                        word = _text[1].capitalize()
                    else:
                        word = i.capitalize()
                else:
                    word = i.capitalize()
                dic_list[user_id][activ].append(word)

            # вывод на экран
            prod = show_list(user_id, activ)  # функция показать список
            # ----- запись списка в базу
            # base.in_dict_list(user_id, dic_list[user_id])
            buttons = [
                types.InlineKeyboardButton('Добавить', callback_data='add'),
                types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                types.InlineKeyboardButton('Обновить', callback_data='up'),
                types.InlineKeyboardButton('Удалить', callback_data='del'),
                types.InlineKeyboardButton('Вернуть', callback_data='back')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2', reply_markup=keyboard)

        # -----Заменить на новый список из сообщения из смс
        elif call.data == 'update_list':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                text = "📝 Список покупок:\n"
                # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
                bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                # text_alien = f'{activ} список:\n'
                # text = "📝 Покупки на сегодня:\n"
                text = f'{activ} список:\n📝 Покупки на сегодня:\n'
            # -- ---
            # Блок замена списка
            dic_list[user_id] = []
            dic_numb[user_id] = []
            for i in dic_list_union[user_id]:
                _text = i.split(maxsplit=1)
                if len(_text) > 1:  # проверка на разделение списка
                    nomer = _text[0]
                    if nomer.isnumeric() == True:  # провкрка на число
                        word = _text[1].capitalize()
                    else:
                        word = i.capitalize()
                else:
                    word = i.capitalize()
                dic_list[user_id].append(word)
            # вывод на экран
            prod = show_list(user_id)  # функция показать список
            # ----- запись списка в базу
            # base.in_dict_list(user_id, dic_list[user_id])
            # base.del_dict_numb(user_id)

            buttons = [
                types.InlineKeyboardButton('Добавить', callback_data='add'),
                types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                types.InlineKeyboardButton('Обновить', callback_data='up'),
                types.InlineKeyboardButton('Удалить', callback_data='del'),
                types.InlineKeyboardButton('Вернуть', callback_data='back')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2', reply_markup=keyboard)

        # ----- Кнопака Активация Управления Чужим списком  "ALIEN" ------В РАБОТЕ!
        elif call.data == 'alien':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            alien_marker[user_id] = 1  # управление чужим списком
            # - подмена ID
            user_id = dic_alien_user[user_id][0]
            user_name_alien = list_user_id[user_id][0]

            text = "📝 Список покупок:\n"
            # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
            bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
            # проверка активного списка мой/ общий
            activ = 'Общий'
            # -----
            if dic_list[user_id].get(activ) is not None:
                prod = show_list(user_id, activ)  # функция показать список
                buttons = [
                    types.InlineKeyboardButton('Добавить', callback_data='add'),
                    types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                    types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                    types.InlineKeyboardButton('Удалить', callback_data='del')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2',
                                 reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

        # ----- Выполнение Кнопка "Показать" список
        elif call.data == 'show':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # блок проверка управления чужим списком
            if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
                user_id = dic_alien_user[user_id][0]
                user_name_alien = list_user_id[user_id][0]
                text = "📝 Список покупок:\n"
                bot.send_message(call.message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
                # проверка активного списка мой/ общий
                activ = 'Общий'
            else:
                # проверка активного списка мой/ общий
                activ = list_activ(user_id)
                text = f'{activ} список:\n📝 Покупки на сегодня:\n'
            # -----
            if dic_list[user_id].get(activ) is not None:
                prod = show_list(user_id, activ)  # функция показать список
                buttons = [
                    types.InlineKeyboardButton('Добавить', callback_data='add'),
                    types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                    types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                    types.InlineKeyboardButton('Обновить', callback_data='up'),
                    types.InlineKeyboardButton('Удалить', callback_data='del'),
                    types.InlineKeyboardButton('Вернуть', callback_data='back')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, text + prod, parse_mode='MarkdownV2',
                                 reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Новый список', callback_data='add'),
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(call.message.chat.id, f'{text} ❗ Список покупок пуст.', reply_markup=keyboard)

        # ----- Выполнение Кнопка "Отправить SMS по ID
        elif call.data == 'sms_id':

            sms_marker[user_id] = 0
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            serv_marker[id_support] = 1
            text = 'Введите ID пользователя и текст сообщения для отправки: [ID Текст]'
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

        # ----- Выполнение Кнопка "Отправить SMS всем пользователям чата
        elif call.data == 'sms_all':
            sms_marker[user_id] = 0
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            serv_marker[id_support] = 'all'

            text = 'Введите текст сообщения для отправки Всем участникам чата'
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

        # ----- Выполнение Кнопка Чтение read_share
        elif call.data == "read_share":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            text = ""
            bot.send_message(call.message.chat.id, f'Список Share - в работе:\n{text}', reply_markup=keyboard)

        # ----- Выполнение Кнопка Чтение read_avail
        elif call.data == "read_avail":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            text = ""
            bot.send_message(call.message.chat.id, f'Список "availibale" - в работе:\n{text}', reply_markup=keyboard)

        # ----- Выполнение кнопка Чтение списка read_Numb
        elif call.data == "read_numb":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            if dic_numb:
                text = ""
                for k_numb, v_numb in dic_numb.items():

                    if k_numb in list_user_id:
                        val_1 = list_user_id[k_numb][0]
                        val_2 = list_user_id[k_numb][1]
                        text = f'{text}{k_numb} @{val_1} дата: {val_2}\n'
                    else:
                        text = f'{text}{k_numb} - нет в списке пользователей USER_ID\n'

                    text = f'{text}Список: {v_numb}\n'
                bot.send_message(call.message.chat.id, f'Список "Numb" всех пользователей:\n{text}',
                                 reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, f'Список "Numb" пуст', reply_markup=keyboard)

        # ----- Выполнение Кнопка Чтение read_shop
        elif call.data == "read_shop":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            if dic_list:
                text = ""
                for k_shop, v_shop in dic_list.items():

                    if k_shop in list_user_id:
                        val_1 = list_user_id[k_shop][0]
                        val_2 = list_user_id[k_shop][1]
                        text = f'{text}{k_shop} @{val_1} дата: {val_2}\n'
                    else:
                        text = f'{text}{k_shop} - нет в списке пользователей USER_ID\n'

                    text = f'{text}Список: {v_shop}\n'
                bot.send_message(call.message.chat.id, f'Список "Shop" всех пользователей:\n{text}',
                                 reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, f'Список "Shop" пуст', reply_markup=keyboard)

        # ----- Выполнение Кнопка Чтение read_userid
        elif call.data == "read_userid":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            text = ""
            for key in list_user_id.keys():
                val_1 = list_user_id[key][0]
                val_2 = list_user_id[key][1]
                text = f'{text}{key} @{val_1} дата: {val_2} \n'
            bot.send_message(call.message.chat.id, f'Список участников чата:\n{text}', reply_markup=keyboard)

        # ----- Выполнение Кнопка Чтение данных - вывод всех доступных списков
        elif call.data == "read":
            drop_id_marker[user_id] = 0
            sms_marker[user_id] = 0
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Shop', callback_data='read_shop'),
                types.InlineKeyboardButton('Share', callback_data='read_share'),
                types.InlineKeyboardButton('Availibale', callback_data='read_avail'),
                types.InlineKeyboardButton('Numb', callback_data='read_numb'),
                types.InlineKeyboardButton('User ID', callback_data='read_userid'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, 'Вывод списка из словарей:', reply_markup=keyboard)

        # -----Выполнение кнопка Удалить по ID из БД
        elif call.data == "drop_id":
            drop_id_marker[user_id] = "drop_id"
            buttons = [
                types.InlineKeyboardButton('Отмена', callback_data='cancel'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv'),
                types.InlineKeyboardButton('Показать user_id', callback_data='user_id')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Для удаления пользователя из БД - введите ID:', reply_markup=keyboard)

        # -----Выполнение кнопка Меню = Удалить ВСЕ из БД
        elif call.data == 'drop_all':
            buttons = [
                types.InlineKeyboardButton('Удалить Все из БД', callback_data='drop_all_bd'),
                types.InlineKeyboardButton('Удалить Name', callback_data='drop_name_bd'),
                types.InlineKeyboardButton('Удалить Shop', callback_data='drop_shop_bd'),
                types.InlineKeyboardButton('Удалить Availibale', callback_data='drop_avail_bd'),
                types.InlineKeyboardButton('Удалить Share', callback_data='drop_share_bd'),
                types.InlineKeyboardButton('Удалить Numb', callback_data='drop_numb_bd'),
                types.InlineKeyboardButton('Чтение данных', callback_data='read'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Удалить весь список из БД:', reply_markup=keyboard)

        # ---- Кнопка удаление Все из БД
        elif call.data == "drop_all_bd":
            drop_id_marker[user_id] = 0
            sms_marker[user_id] = 0
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            # ---- удаление из БД Repl IT
            # for key in db.keys():
            #    del db[key]
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Все данные из БД удалены:', reply_markup=keyboard)

        # ---- Кнопка удаление список Numb из БД - отмеченные позиции списка
        elif call.data == "drop_numb_bd":

            marker = "numb"
            #  --- Удалить из БД список
            # base.del_list(marker)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Cписок "{marker}" из БД удален', reply_markup=keyboard)

        # ---- Кнопка удаление список Share из БД - расшарить мой список покупок
        elif call.data == "drop_share_bd":

            marker = "share"
            #  --- Удалить из БД список
            # base.del_list(marker)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Cписок "{marker}" из БД удален', reply_markup=keyboard)

        # ---- Кнопка удаление список Availibale из БД - доступные списки друзей
        elif call.data == "drop_avail_bd":

            marker = "avail"
            #  --- Удалить из БД список
            # base.del_list(marker)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Cписок "{marker}" из БД удален', reply_markup=keyboard)

        # ---- Кнопка удаление список SHOP из БД -
        elif call.data == "drop_shop_bd":

            marker = "shop"
            #  --- Удалить из БД список
            # base.del_list(marker)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Cписок "{marker}" из БД удален', reply_markup=keyboard)

        # ---- Кнопка удаление список Name из БД -
        elif call.data == "drop_name_bd":

            marker = "name"
            #  --- Удалить из БД список
            # base.del_list(marker)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Cписок "{marker}" из БД удален', reply_markup=keyboard)

        # ----- Выполнение кнопка Выбран "Мой список"
        elif call.data == 'my_list':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            alien_marker[user_id] = 0
            activ_list[user_id] = 'Мой'

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Создать список', callback_data='add'),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'🖍️ Отлично!\n Выбран "Мой" список. Начнем заполнять?', reply_markup=keyboard)

        # ----- Выполнение кнопка Select - выбор списка
        elif call.data == 'select':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            alien_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Мой список', callback_data='my_list'),
                types.InlineKeyboardButton('Общий список', callback_data='all_list'),
                types.InlineKeyboardButton('Списки друзей', callback_data='friendly'),
                types.InlineKeyboardButton('Управление списками', callback_data='manage'),
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, 'С каким списком продолжить работу?', reply_markup=keyboard)

        # ----- Выполнение кнопка Friendly - выбор списка друзей
        elif call.data == 'friendly':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            alien_marker[user_id] = 0
            buttons = [
                types.InlineKeyboardButton('Мой список', callback_data='my_list'),
                types.InlineKeyboardButton('Управление списками', callback_data='manage'),
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            if dic_availibale.get(user_id) is not None:
                text = ""
                j = 0  # для счета позиций списка
                for i in dic_availibale[user_id]:
                    j += 1

                    if i in list_user_id.keys():
                        user_name = f'@{list_user_id[i][0]}'
                    else:
                        user_name = f'Список недоступен ID={i}'
                    text = (f'{text}{j} {user_name} \n')

                avail_marker[user_id] = 1  # маркер выбранного чужого списка
                bot.send_message(call.message.chat.id, f'Выберите номер для работы со списком\n'
                                                       f'📗 Доступные дружественные списки:\n{text}',
                                 reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, '📕 Нет доступных дружественных списков', reply_markup=keyboard)

        # ----- Выполнение кнопка поделиться "Мой список" (share_my)
        elif call.data == 'share_my':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            alien_marker[user_id] = 0

            share_marker[user_id] = 1

            if dic_list[user_id].get('Мой') is not None:
                dic_list[user_id]['Общий'] = dic_list[user_id]['Мой'].copy()
            else:
                dic_list[user_id]['Общий'] = []

            if dic_numb[user_id].get('Мой') is not None:
                dic_numb[user_id]['Общий'] = dic_numb[user_id]['Мой'].copy()
            else:
                dic_numb[user_id]['Общий'] = []
            bot.send_message(call.message.chat.id, "Для предоставления доступа к списку, введите ID пользователя:")

        # ----- Выполнение кнопка поделиться "Общий список" (share_all)
        elif call.data == 'share_all':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0
            alien_marker[user_id] = 0

            share_marker[user_id] = 1

            if dic_list[user_id].get('Общий') is None:
                dic_list[user_id]['Общий'] = []

            if dic_numb[user_id].get('Общий') is None:
                dic_numb[user_id]['Общий'] = []
            bot.send_message(call.message.chat.id, "Для предоставления доступа к списку, введите ID пользователя:")

        # ----- Выполнение кнопка Выбран "Общий список"
        elif call.data == 'all_list':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            alien_marker[user_id] = 0
            activ_list[user_id] = 'Общий'

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Создать список', callback_data='add'),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'✒️Классно!\n Составим "общий" список, и поделимся им с друзьями.',
                                  reply_markup=keyboard)

        # ----- Выполнение кнопка Показать User_ID все пользователи приложения
        elif call.data == 'user_id':
            add_marker[user_id] = 0
            tag_marker[user_id] = 0
            edit_marker[user_id] = 0
            union_marker[user_id] = 0
            share_marker[user_id] = 0
            back_marker[user_id] = 0
            sms_marker[user_id] = 0
            drop_id_marker[user_id] = 0
            serv_marker[user_id] = 0

            share_but[user_id] = 0
            friendly_but[user_id] = 0
            alien_but[user_id] = 0
            y_but[user_id] = 0
            n_but[user_id] = 0
            up_but[user_id] = 0

            text = ""
            for key in list_user_id.keys():
                val_1 = list_user_id[key][0]
                val_2 = list_user_id[key][1]
                text = f'{text}{key} @{val_1} дата: {val_2} \n'
            bot.send_message(call.message.chat.id, text)

        bot.answer_callback_query(callback_query_id=call.id)  # обработка данного callback-запроса завершена.
# -----------------------------------------------------------------------------
# = = = Выполнение сценариев = = =
@bot.message_handler(content_types=["text"])
def echo(message):
    # global id_support

    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)  # Log пользователя
    # time_sms = message.date

    word = message.text.capitalize().replace(".", ",")
    if word == "/":
        pass
    else:
        iskl = ":;!_*-+()\/#%&~'^$`{}[]<>|\"[[]]"  # Убираем спец символы
        for n in iskl:
            if n in message.text:
                word = word.capitalize().replace(n, " ")
            else:
                pass
    # нормализация словарей-переменных
    normalization(user_id)

    # ---Сценарий - завершение всех команд
    if word == "/":
        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

    # !!!!!!!!!!!!!
    # --- Сценарий -  выбрана кнопка "Стиль" - показать пример стиля
    elif style_marker[user_id] == 1:

        add_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        #     -----------------------
        # Блок "Отметить"  ✔️ ‼️
        Nomer = message.text
        if Nomer.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)

            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            if Nomer <= len(list_style[user_id]) and Nomer > 0:

                #  выбор изображения стиля
                # img_style_proba =  img_style_proba(Nomer)
                #

                #  название стиля изображения
                name_style = list_style[Nomer][0]
                dic_numb[user_id] = name_style

                text = f'✔️ - выбран стиль: {name_style}'
                bot.send_message(message.chat.id, f'{text}\nЗагрузите свое изображение',  reply_markup=keyboard)

                # --проверка на повтор отмеченного продукта в списке и <> 0
                # if dic_numb[user_id].get(activ) is not None:
                #     if A in dic_numb[user_id][activ]:
                #         bot.send_message(message.chat.id,
                #                          f'{text_1}‼️ {message.text} - уже отмечено в списке. \n Выберите другое наименование.')
                #     else:
                #         dic_numb[user_id][activ].append(A)
                # else:
                #     dic_numb[user_id][activ] = [A]
                # -- если список выполнен, отмечены все элементы списка
                # if len(dic_numb[user_id][activ]) == len(dic_list[user_id][activ]):
                #     text_end = "🎉 - На сегодня все!"
                #     bot.send_message(message.chat.id, text_end)
                #     text_2 = f'{text_1} Куплено по списку:\n'
                # else:
                #     text_2 = f'{text_1} Список покупок на сегодня:\n'
                # вывод списка на экран
                # prod = show_list(user_id, activ)  # функция показать список
                #  запись в Базу номеров
                # base.in_dict_numb(user_id, dic_numb[user_id])
                # buttons = [
                #     types.InlineKeyboardButton('Добавить', callback_data='add'),
                #     types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                #     types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                #     types.InlineKeyboardButton('Обновить', callback_data='up'),
                #     types.InlineKeyboardButton('Удалить', callback_data='del'),
                #     types.InlineKeyboardButton('Вернуть', callback_data='back')
                # ]
                # keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                # keyboard.add(*buttons)
                # bot.send_message(message.chat.id,  text_2 + prod, parse_mode='MarkdownV2', reply_markup=keyboard)
            else:
                # buttons = [
                #     types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                #     types.InlineKeyboardButton('Меню', callback_data='menu')
                # ]
                # keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                # keyboard.add(*buttons)
                bot.send_message(message.chat.id, f'🚫 {Nomer} - такого номера в cписке нет',
                                 reply_markup=keyboard)
        else:
            text_3 = f'⚠️ Введите цифрами номер из списка.'
            # buttons = [
            #     types.InlineKeyboardButton('Завершить', callback_data='cancel'),
            #     types.InlineKeyboardButton('Меню', callback_data='menu')
            # ]
            # keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            # keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'{text_3}\n {text_style}' , reply_markup=keyboard)

    # --- Сценарий - выбор активного дружественного списка - Friendly
    elif avail_marker[user_id] == 1:

        add_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        # Блок "выбор списка"  ✔️ ‼️ ⛔🚫🆔
        A = message.text
        if A.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)
            if Nomer <= len(dic_availibale[user_id]) and Nomer != 0:
                id_alien = str(dic_availibale[user_id][Nomer - 1])
                dic_alien_user[user_id] = [id_alien]  # выбор номера ID по индексу Nomer

                user_name = list_user_id[id_alien][0]
                alien_marker[user_id] = 1  # управление чужим списком
                text_alien = f'🔄 Вы управляете списком пользователя: @{user_name}\n'

                text1 = f'Cписок @{user_name}'
                text2 = 'Меню'
                text3 = 'Выбор списка'  # команда select - показать мой список
                text4 = 'Управление списками'  # Manager
                buttons = [
                    types.InlineKeyboardButton(text1, callback_data='show'),  # чужой список просмотр
                    types.InlineKeyboardButton(text3, callback_data='select'),  # select выбор списка
                    types.InlineKeyboardButton(text4, callback_data='manage'),  # Управление списками
                    types.InlineKeyboardButton(text2, callback_data='menu')  # Меню
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(message.chat.id, text_alien, reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                    types.InlineKeyboardButton('Меню', callback_data='menu')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(message.chat.id, f'🚫 {message.text} - такого номера в cписке нет',
                                 reply_markup=keyboard)
        else:
            _text = f'⚠️ Введите цифрами номер из списка.'
            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, _text, reply_markup=keyboard)
    # avail_marker[user_id] = 1  # маркер выбранного чужого списка

    # --- Сценарий -  выбрана кнопка "Вернуть" - отменить выделение позиции в списке
    elif back_marker[user_id] == 1:

        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        # блок проверка управления чужим списком
        if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
            user_id = dic_alien_user[user_id][0]
            user_name_alien = list_user_id[user_id][0]
            text_1 = "\n "
            # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
            bot.send_message(message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')
            # проверка активного списка мой/ общий
            activ = 'Общий'
        else:
            # проверка активного списка мой/ общий
            activ = list_activ(user_id)
            # text_alien = f'{activ} список:\n'
            text_1 = f'{activ} список:\n'
        # ------
        # Блок "Вернуть"
        A = message.text
        if A.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)
            if Nomer <= len(dic_list[user_id][activ]) and Nomer != 0:
                # --проверка на вхождение числа в список Номеров
                if dic_numb[user_id].get(activ) is not None:
                    if A in dic_numb[user_id][activ]:
                        dic_numb[user_id][activ].remove(A)
                    else:
                        # bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAIp3GQpz-ryRREzFeW7IlMtgV0EDE7CAAIwAANEDc8XDmth2U5XQgABLwQ')
                        bot.send_message(message.chat.id,
                                         f'{text_1} ❌ {message.text} - не отмечено в списке. \n'
                                         f'Выберите другой номер.')
                else:
                    dic_numb[user_id][activ] = {}
                    bot.send_message(message.chat.id,
                                     f'{text_1} ❌️ Нет отмеченных позиций в списке.')
                text_2 = f'{text_1}📝 Список покупок на сегодня: \n'

                # вывод списка на экран
                prod = show_list(user_id, activ)  # функция показать список
                #  запись в Базу номеров
                # base.in_dict_numb(user_id, dic_numb[user_id])
                buttons = [
                    types.InlineKeyboardButton('Добавить', callback_data='add'),
                    types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                    types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                    types.InlineKeyboardButton('Обновить', callback_data='up'),
                    types.InlineKeyboardButton('Удалить', callback_data='del'),
                    types.InlineKeyboardButton('Вернуть', callback_data='back')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                bot.send_message(message.chat.id, text_2 + prod, parse_mode='MarkdownV2',
                                 reply_markup=keyboard)
            else:
                buttons = [
                    types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                    types.InlineKeyboardButton('Меню', callback_data='menu')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                # bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIp3GQpz-ryRREzFeW7IlMtgV0EDE7CAAIwAANEDc8XDmth2U5XQgABLwQ')
                bot.send_message(message.chat.id, f'{text_1} 🚫 {message.text} - такого номера нет в списке.\n'
                                                  f'Введите другой номер', reply_markup=keyboard)
        else:
            text_3 = f'{text_1}⚠️ Введите цифрами номер из списка.'
            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, text_3, reply_markup=keyboard)

    # --- Сценарий - заполнение списка названиями Add
    elif add_marker[user_id] == 1:
        id_log(user_id, user_name, time_sms)

        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        buttons = [
            types.InlineKeyboardButton('Показать список', callback_data='show'),
            types.InlineKeyboardButton('Завершить', callback_data='cancel')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)

        # блок проверка управления чужим списком
        if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
            user_id = dic_alien_user[user_id][0]
            user_name_alien = list_user_id[user_id][0]
            text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'

            # проверка активного списка мой/ общий
            activ = 'Общий'
        else:
            # проверка активного списка мой/ общий
            activ = list_activ(user_id)
            text_alien = f'{activ} список:\n'
        # -----
        if dic_list[user_id].get(activ) is not None:
            if word in dic_list[user_id][activ]:  # проверка на полное соответствие продукта в списке
                bot.send_message(message.chat.id,
                                 f'{text_alien} ⚠️ Наименование "{word}" уже есть в списке. \n Добавьте другой продукт:',
                                 reply_markup=keyboard)
            else:
                dic_list[user_id][activ].append(word)
                # ----- запись списка в базу
                # base.in_dict_list(user_id, dic_list[user_id])
                bot.send_message(message.chat.id, f'{text_alien} Наименование "{word}" добавлено в список покупок. 👌',
                                 reply_markup=keyboard)
        else:
            dic_list[user_id][activ] = [word]
            # ----- запись списка в базу
            # base.in_dict_list(user_id, dic_list[user_id])
            bot.send_message(message.chat.id, f'{text_alien} Наименование "{word}" добавлено в список покупок. 👌',
                             reply_markup=keyboard)

    # ----Сценарий редактировать список edit
    elif edit_marker[user_id] == 1:

        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        # блок проверка управления чужим списком
        if alien_marker.get(user_id) is not None and alien_marker[user_id] == 1:
            user_id = dic_alien_user[user_id][0]
            user_name_alien = list_user_id[user_id][0]
            # text_alien = f'🔄 Вы управляете списком пользователя: @{user_name_alien} \n'
            text_1 = "\n"
            bot.send_message(message.chat.id, f'🔄 Вы управляете списком пользователя: @{user_name_alien}')

            # проверка активного списка мой/ общий
            activ = 'Общий'
        else:
            # проверка активного списка мой/ общий
            activ = list_activ(user_id)
            # text_alien = f'{activ} список:\n'
            text_1 = f'{activ} список:\n'
        #     -----
        # Блок редактировать
        # _text = message.text.split(maxsplit=1)
        _text = word.split(maxsplit=1)
        if len(_text) > 1:  # проверка на разделение списка
            word = _text[1].capitalize()
            nomer = _text[0]
            if nomer.isnumeric() == True:  # провкрка на число
                Znach = int(nomer)
                if Znach <= len(dic_list[user_id][
                                    activ]):  # проверква на вхождение в список List, номер еового продукта не больше элементов списка
                    if dic_numb[user_id].get(activ) is not None:
                        if nomer in dic_numb[user_id][activ]:  # проверка номер не отмечен в списке
                            bot.send_message(message.chat.id,
                                             f'🚫  Позиция №{nomer} уже отмечена в списке.\nПовторите ввод:')
                            text_2 = f'{text_1}📝 Список покупок на сегодня: \n'
                        else:
                            dic_list[user_id][activ][Znach - 1] = word
                            text_2 = f'{text_1}🤘 Список продуктов изменен:\n'
                    else:
                        dic_list[user_id][activ][Znach - 1] = word
                        text_2 = f'{text_1}🤘 Список продуктов изменен:\n'

                    # вывод списка на экран-------------------
                    prod = show_list(user_id, activ)  # функция показать список
                    # ----- запись списка в базу
                    # base.in_dict_list(user_id, dic_list[user_id])
                    buttons = [
                        types.InlineKeyboardButton('Добавить', callback_data='add'),
                        types.InlineKeyboardButton('Отметить', callback_data='Ok'),
                        types.InlineKeyboardButton('Редактировать', callback_data='edit'),
                        types.InlineKeyboardButton('Обновить', callback_data='up'),
                        types.InlineKeyboardButton('Удалить', callback_data='del'),
                        types.InlineKeyboardButton('Вернуть', callback_data='back')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                    keyboard.add(*buttons)
                    bot.send_message(message.chat.id, text_2 + prod, parse_mode='MarkdownV2',
                                     reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, f'🚫  Позиция №{nomer} в списке отсутствует. \n Повторите ввод:')
            else:
                buttons = [
                    types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                    types.InlineKeyboardButton('Меню', callback_data='menu')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                text_3 = ('⚠️ Введите цифрами номер из списка.')
                bot.send_message(message.chat.id, text_3, reply_markup=keyboard)
        else:
            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            text_4 = R' Выберите номер в списке для изменения и укажите новое наименование (пример: "7 карандаш"):'
            bot.send_message(message.chat.id, "⛔ Неверный ввод!" + "\n" + text_4, reply_markup=keyboard)

    # --- Сценарий - добавить новый список
    elif union_marker[user_id] == 1:

        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        dic_list_union[user_id] = word.split("\n")  # новый список из сообщения
        text = (
            "Добавить - добавить позиции из этого списка в мой список покупок или \nЗаменить - заменить мой список новым из сообщения?")
        buttons = [
            types.InlineKeyboardButton('Добавить', callback_data='union_list'),
            types.InlineKeyboardButton(text='Заменить', callback_data='update_list')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

    # --- Сценарий ответ по SMS ID - 1 пользователь
    elif serv_marker[id_support] == 1:
        union_marker[user_id] = 0
        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        serv_marker[id_support] = 0

        # Блок разделение сообщения на ID и Текст
        _text = message.text.split(maxsplit=1)
        if len(_text) > 1:  # проверка на разделение списка
            word = _text[1].capitalize()
            nomer = _text[0]
            if nomer.isnumeric() == True:  # проверка на число
                Znach = int(nomer)

                # 📧✉️🔖

                if nomer in list_user_id:
                    # 🛠️ S_U_P_P_O_R_T:\n📨 Сообщение от тех. поддержки чата:     📩
                    _text = '🛠️ S_U_P_P_O_R_T:\n📩 Сообщение от тех. поддержки чата:' + '\n'
                    name = list_user_id[nomer][0]
                    try:
                        bot.send_message(Znach, f'{_text} {word}')
                        bot.send_message(message.chat.id, f'📤 сообщение для {Znach} @{name} отправлено')
                    except:
                        bot.send_message(message.chat.id, f'❌ 📮 сообщение не доставлено\n{Znach} @{name} недоступен,')
                else:
                    buttons = [
                        types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                        types.InlineKeyboardButton('Отправить SMS', callback_data='sms_id')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                    keyboard.add(*buttons)
                    bot.send_message(message.chat.id, f'🚫 Такой пользователь по ID {Znach} не найден')
            else:
                buttons = [
                    types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                    types.InlineKeyboardButton('Отправить SMS', callback_data='sms_id')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)
                _text = '⚠️ Введите цифрами номер ID.'
                bot.send_message(message.chat.id, _text, reply_markup=keyboard)

    # --- Сценарий ответ по SMS всем пользователям чата
    elif serv_marker[id_support] == 'all':
        serv_marker[id_support] = 0

        union_marker[user_id] = 0
        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0

        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        my_text_ok = ""
        my_text_not = ""
        all_text = f'🛠️ S_U_P_P_O_R_T:\n📨 Сообщение от тех. поддержки чата:'

        if not list_user_id:
            bot.send_message(message.chat.id, f'📌Список ID-контактов чата пуст.\nСообщения не отправлены.')
        else:
            for key in list_user_id.keys():
                if key != id_support:
                    val_1 = list_user_id[key][0]
                    try:
                        my_text_ok = f'{my_text_ok}{key} @{val_1}\n'
                        bot.send_message(key, f'{all_text} {word}')
                    except:
                        my_text_not = f'{my_text_not}{key} @{val_1}\n'
            bot.send_message(message.chat.id, f'📜 Сообщения отправлены пользователям по списку:\n{my_text_ok}')
            if my_text_not != "":
                bot.send_message(message.chat.id, f'❌ Пользователи недоступны:\n{my_text_not}')

    # --- Сценарий Удалить пользователя по ID из БД
    elif drop_id_marker[user_id] == "drop_id":

        drop_id_marker[user_id] = 0
        serv_marker[id_support] = 0
        union_marker[user_id] = 0
        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0
        sms_marker[user_id] = 0
        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        # Проверка ID на вхождение в список
        nomer = message.text
        if nomer in list_user_id.keys():  # проверка на вхождение номера в список ID
            # удаление ID из БД Repl IT
            # base.del_id(nomer)
            # Перезапись всех списков

            del list_user_id[nomer]

            if dic_list.get(nomer) is not None:
                del dic_list[nomer]

            if dic_share.get(nomer) is not None:
                del dic_share[nomer]

            if dic_numb.get(nomer) is not None:
                del dic_numb[nomer]

            if dic_availibale.get(nomer) is not None:
                del dic_availibale[nomer]

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f' Пользователь ID {nomer} удален из БД:')

        else:
            buttons = [
                types.InlineKeyboardButton('Показать user_id', callback_data='user_id'),
                types.InlineKeyboardButton('Удалить ID', callback_data='drop_id'),
                types.InlineKeyboardButton('Удалить  Все', callback_data='drop_all'),
                types.InlineKeyboardButton('Сервисные команды', callback_data='serv')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'🚫 Такого номера нет в списке.', reply_markup=keyboard)

    # --- Сценарий расшарить свой список, предоставление доступа по ID (Share)---------!в РАБОТЕ!
    elif share_marker[user_id] == 1:

        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        sms_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0
        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        # user_name = str(message.from_user.username)  # @Логин
        # user_Fname = message.from_user.first_name  # фамилия(имя) пользователя
        # user_id = str(message.from_user.id)  # Id пользователя

        nomer = message.text
        if nomer == user_id:
            bot.send_message(message.chat.id, f'ID{nomer} - это Ваш ID.\n'
                                              f'Введите номер ID, для предоставления доступа к своему списку:')
        else:
            # проверка на вхождение ID-чужой в общий список ID Бота
            if nomer in list_user_id.keys():
                user_id_alien = f'{list_user_id[nomer][0]}'
                # for val in list_user_id[nomer]:
                #     user_id_alien = f'@{val[0]}'
                # кому я открыл список для просмотра мой ID -> чужие номера ID
                if dic_share.get(user_id) is not None:
                    dic_share[user_id].append(
                        nomer)  # словарь -> Мой ID : {списки iD пользвателя, кто может смотреть мой список}
                else:
                    dic_share[user_id] = [nomer]
                bot.send_message(message.chat.id, f'Доступ к вашему списку предоставлен для @{user_id_alien} ')
                # -------------------------------
                # кто может смотреть мой список ID чужой -> мой номер ID
                if dic_availibale.get(nomer) is not None:
                    dic_availibale[nomer].append(user_id)
                else:
                    dic_availibale[nomer] = [user_id]

                dic_alien_user[nomer] = [user_id]  # активация чужого списка для пользователя nomer

                text1 = f'Cписок @{user_name}'
                text2 = 'Меню'
                text3 = 'Мой список'  # команда Show - показать мой список
                text4 = 'Управление списками'  # Manager

                buttons = [
                    types.InlineKeyboardButton(text1, callback_data='alien'),  # чужой список активация
                    types.InlineKeyboardButton(text3, callback_data='show'),  # мой список
                    types.InlineKeyboardButton(text4, callback_data='manage'),  # Управление списками
                    types.InlineKeyboardButton(text2, callback_data='menu')  # меню
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
                keyboard.add(*buttons)

                bot.send_message(nomer, f' @{user_name} открыл вам доступ к своему списку', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, f'Введенный Id {nomer} отсутствует в списке Чат-Бота.\n'
                                                  f'Попросите пользователя прислать свой ID  - (команда \id)')

    # --- Сценарий команды нет в списке
    else:
        add_marker[user_id] = 0
        tag_marker[user_id] = 0
        edit_marker[user_id] = 0
        union_marker[user_id] = 0
        share_marker[user_id] = 0
        back_marker[user_id] = 0
        drop_id_marker[user_id] = 0
        serv_marker[user_id] = 0
        sms_marker[user_id] = 0
        share_but[user_id] = 0
        friendly_but[user_id] = 0
        alien_but[user_id] = 0
        y_but[user_id] = 0
        n_but[user_id] = 0
        up_but[user_id] = 0

        _text = ('❌ Неизвестная команда.')  # + ' \n' + 'Для вызова списка команд введите - /menu')
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Справка', callback_data='help')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, _text, reply_markup=keyboard)


# keep_alive()  #запускаем flask-сервер
# while True:
#   try:
#     bot.polling(none_stop=True)
#   except Exception as _ex:
#     print(_ex)
#     time.sleep(15)

bot.polling(none_stop=True)