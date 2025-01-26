import requests

from setting import *
from file_img import *
# from model_cnn import *
# from setting import TG_TOKEN

import os
import telebot
from telebot import types
from datetime import datetime
from telebot import TeleBot
import time

from PIL import Image


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

# --- Маркеры событий
style_marker = {}  # маркер стиля изображения
show_marker = {}   # маркер для просмотра стиля
image_marker = {} # маркер загруженного изображения

# --- словари для Style
dic_style = {}  # название (номер) изображения для стиля dic_style[user_id]
dic_img = {}   # название загруженного файла и имходный размер
# ---------------

# = = = Описание команд и функций
# --- вызов справки
HELP = """
Приветствую!✌️ 
Я Чат-Бот! Помогу преобразовать твое изображение под один из известных стилей.
Просто загрузи свое изображение!
Нажми на кнопку ниже, что бы узнать функционал доступных команд и их описание:
©️
"""
#  ---- описание вызываемых команд
TEAM = """✏️ Команды доступные в приложении:
/menu - (Menu, Меню) - Меню - список доступных команд приложения.
/help - (Нelp, Справка, ? ) - вызов справки о программе, знакомство с приложением.
/info - (Info, Описание) - описание действия команд и кнопок приложения.
/sample - (Sample, Пример) - показать пример изображения стиля.
/style - (Style, Стиль) - выбор изображение стиля.
/end - (End, Отмена, /) - отмена, завершение команды.
"""

# ---- описания действия кнопок
Info = """
🖼️ Просто загрузи свое изображение, и я помогу его преобразовать под один из известных стилей.

✏️ Описание действия кнопок приложения: 
1. Меню - список доступных команд приложения.
2. Справка - вызов справки о программе, знакомство с приложением.
3. Описание - описание действия команд и кнопок приложения.
4. Пример стиля - показать пример изображения стиля.
5. Новое изображение - загрузить новое изображение, для стилизации.
6. Завершить - завершение всех команд.
"""


#  = = = Общие функции приложения
# ----- Отмена всех команд
# def cancel_id(user_id):
#     # add_marker[user_id] = 0
#     # tag_marker[user_id] = 0
#     # edit_marker[user_id] = 0
#     # union_marker[user_id] = 0
#     # share_marker[user_id] = 0
#     # back_marker[user_id] = 0
#     # sms_marker[user_id] = 0
#     # share_but[user_id] = 0
#     # friendly_but[user_id] = 0
#     # alien_but[user_id] = 0
#     # y_but[user_id] = 0
#     # n_but[user_id] = 0
#     # up_but[user_id] = 0
#     # drop_id_marker[user_id] = 0
#     # serv_marker[user_id] = 0
#     _text = f'❌ Неизвестная команда.'
#     return _text

# ----- Нормализация всех словарей - проверка на существование
def normalization(user_id):

    if dic_img.get(user_id) is not None:
        # удалить файл изображения
        os.remove( dic_img[user_id] [0])
        del dic_img[user_id]
    if dic_style.get(user_id) is not None:
        del dic_style[user_id]

    style_marker[user_id] = 0
    show_marker[user_id] = 0

# ------------------------------------------------------------
# = = = Команды для управления приложением
# -----  Справка
@bot.message_handler(
    commands=["Справка", "СПРАВКА", "справка", "help", "Help", "HELP", "hElp", "heLp", "helP", "HElp", "HElP", "HELp",
              "hELp", "hELP", "heLp", "heLP", "?", "start"])
def help(message):
    user_id = str(message.from_user.id)  # id пользователя

    # обнуляем маркеры
    style_marker[user_id] = 0
    show_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
        types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, HELP, reply_markup=keyboard)

# ----- Меню
@bot.message_handler(commands=["menu", "MENU", "Menu", "меню", "Меню", "МЕНЮ", "мЕНЮ", "меНЮ", "менЮ"])
def menu(message):
    user_id = str(message.from_user.id)  # id пользователя

    # обнуляем маркеры
    style_marker[user_id] = 0
    show_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
        types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, TEAM, reply_markup=keyboard)

# ----- Инфо - описание команд и кнопок
@bot.message_handler(commands=["info", "INFO", "Info", "iNfo", "Описание", "описание", "ОПИСАНИЕ"])
def info(message):
    user_id = str(message.from_user.id)  # id пользователя

    # обнуляем маркеры
    style_marker[user_id] = 0
    show_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
        types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, Info, reply_markup=keyboard)

#  ----- выбор стиля для переноса
@bot.message_handler(commands=["style", "STYLE", "Style", "Стиль", "стиль", "СТИЛЬ"])
def style_img(message):
    user_id = str(message.from_user.id)  # id пользователя

    style_marker[user_id] = 1
    show_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'🖍️Выберите изображение стиля для переноса:\n{text_style}', reply_markup=keyboard)

# ----- Отмена всех команд /end
@bot.message_handler(commands=["Отмена", "ОТМЕНА", "отмена", "end", "END", "End", "/"])
def end(message):
    user_id = str(message.from_user.id)

    #  обнуляем словари и маркеры
    normalization(user_id)

    buttons = [
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
        types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

# -----Показ изображения стиля
@bot.message_handler(commands=["sample", "SAMPLE", "Sample", "пример", "Пример", "ПРИМЕР"])
def show(message):
    user_id = str(message.from_user.id)

    show_marker[user_id]  = 1
    style_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'🖍️Выберите категорию стиля изображения и я покажу пример:\n {text_style}',
                     reply_markup=keyboard)

# ----- получение изображения
# @bot.message_handler(content_types=['photo'])
@bot.message_handler(content_types=['document', 'audio', 'video', 'photo'])
def photo(message):
    user_id = str(message.from_user.id)  # id пользователя

    style_marker[user_id] = 0
    show_marker[user_id] = 0

    fileID = message.document.file_id if message.content_type == 'document' else \
         message.audio.file_id if message.content_type == 'audio' else \
             message.video.file_id if message.content_type == 'video' else \
                 message.photo[-1].file_id if message.content_type == 'photo' else None
    file_info = bot.get_file(fileID)
    file_extension = os.path.splitext(file_info.file_path)[-1].lower()

    # определение формата файла
    if file_extension in ['.jpg', '.jpeg', '.png']:

        downloaded_file = bot.download_file(file_info.file_path)
        img_photo = message.photo[len(message.photo) - 1].file_id

        # path = bot.get_file(fileID)
        # extn = '.' + str(path.file_path).split('.')[-1]
        # print(extn)
        # print(path)
        # chat_id = message.chat.id
        # url = r'https://api.telegram.org/bot'
        #     # r'https://api.telegram.org'
        # fl = requests.get(f'{url}{TG_TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_photo}').text
        # print(  img_photo )
        # ph = Image.open(f'{url}{TG_TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_photo}')
        # nm = f'{url}{TG_TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_photo}'
        # print(f'{url}{TG_TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_photo}')
        # print( downloaded_file)
        # ph = Image.open( nm)
        # print( ph)
        # print('---------------------------')
        # bot.send_photo(message.chat.id, fl, caption='Ваш текст')

        # bot.send_message(message.chat.id, f' изображения:\n {fl}')
        # print('---------------------------')
        #  загрузка изображения

        text = f'temp_image/img_{user_id}.jpg'

        with open( text , 'wb' ) as new_file:
            new_img = new_file.write(downloaded_file)

        # размер исходного изображения
        in_img_size = img_size(text)
        #  название исходного файла и исходный размер в словарь
        dic_img[user_id] = [text, in_img_size ]

        # print( dic_img[user_id] )

        #  проверка на выбор изображения стиля
        if dic_style.get(user_id) is not None:

           bot.send_message(message.chat.id, f'[ ■_■_□_□_□ ] ...выполняю перенос стиля...\n'
                                             f'⏰... это займет несколько минут...')
           # #  начальный размер файла
           # in_size = dic_img[user_id][1]
           # #  изображение стиля
           # img_style =dic_style[user_id][1]
           # # изображение контент
           # img_content = image_loader (text)
           # #  изображение для модели
           # img_input = img_content.clone()
           # # запуск модели CNN
           # output_model, score_style, score_content = run_style_transfer(model_vgg, cnn_normalization_mean,
           #                                                         cnn_normalization_std, img_content,
           #                                                         img_style, img_input,
           #                                                         num_steps=N_Step,
           #                                                         style_weight=1000000,
           #                                                         content_weight=1)
           #
           # # преобразование изображение в исходный размер
           # img_resize = resize_loader(output_model, in_size)
           # print( dic_img[user_id], dic_style[user_id] )

           output_img = style_apply( dic_img[user_id], dic_style[user_id] )

           buttons = [
               types.InlineKeyboardButton('Меню', callback_data='menu'),
               types.InlineKeyboardButton('Завершить', callback_data='cancel'),
               types.InlineKeyboardButton('Выбрать новый стиль', callback_data='new_style'),
               types.InlineKeyboardButton('Загрузить новое изображение', callback_data='new_image')
           ]
           keyboard = types.InlineKeyboardMarkup(row_width=2)
           keyboard.add(*buttons)

           bot.send_photo(message.chat.id, output_img)
           bot.send_message(message.chat.id, f'✨ Новое изображение', reply_markup=keyboard )
           # bot.send_photo(message.chat.id, img_resize, caption='Новое изображение', reply_markup=keyboard )
        else:
            # изображения стиля не выбрано. предложить варианты стиля
            style_marker[user_id] = 1
            show_marker[user_id] = 0
            image_marker [user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'🖍️Выберите изображение стиля для переноса:\n{text_style}',
                             reply_markup=keyboard)

    else:
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Завершить', callback_data='cancel'),
            types.InlineKeyboardButton('Описание команд', callback_data='info')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f'⚠️ Неудалось распознать файл.\n'
                                          f'Пришлите изображение в фармате "jpеg" или "png" ',
                         reply_markup=keyboard)

# ---------------------------------------------
# = = = Реагирование на кнопки = = =
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    user_id = str(call.from_user.id)
    # message_id = call.message.message_id
    # chat_id = call.message.chat.id
    # print(user_id)

    if call.message:
        # ----- Выполнение кнопки новое изобажение
        if call.data == "new_image":

            show_marker[user_id]  = 0
            style_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, f'📥 Загрузите свое изображение для применения стиля',
                             reply_markup=keyboard)

        #  Выбор стиля для изображения
        elif call.data == "new_style":

            style_marker[user_id] = 1
            show_marker[user_id]  = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, f'🖍️Выберите изображение стиля для переноса:\n {text_style}',
                             reply_markup=keyboard)

        #  Показ примера стиля
        elif call.data == "show_style":

            style_marker[user_id] = 0
            show_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, f'🖍️Выберите категорию стиля изображения и я покажу пример:\n {text_style}',
                             reply_markup=keyboard)

        # ----- Кнопка Справка
        elif call.data == "help":

            style_marker[user_id] = 0
            show_marker[user_id]  = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=HELP, reply_markup=keyboard)

           # -----Выполнение Кнопка "Отмена" - завершение всех команд
        elif call.data == "cancel":

            #  обнуляем словари и маркеры
            normalization(user_id)

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

        # ----- Выполнение кнопка "Меню"
        elif call.data == 'menu':

            style_marker[user_id] = 0
            show_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Справка', callback_data='help'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=TEAM,
                                  reply_markup=keyboard)
            # bot.send_message(call.message.chat.id, TEAM,  reply_markup=keyboard)

        # ----- Выполнение кнопка "Info" Описание команд
        elif call.data == 'info':

            #  обнуляем словари и маркеры
            style_marker[user_id] = 0
            show_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Справка', callback_data='help'),
                types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=Info, reply_markup=keyboard)

        # ----- Применить стиль, к уже загруженному изображению
        elif call.data == 'apply':

            style_marker[user_id] = 0
            show_marker[user_id] = 0

            # print(user_id, dic_img[user_id], dic_style[user_id])

            bot.send_message(call.message.chat.id, f'[ ■_■_□_□_□ ] ...выполняю перенос стиля...\n'
                                              f'⏰... это займет не более 1 мин.')
            output_img = style_apply(dic_img[user_id], dic_style[user_id] )

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Выбрать новый стиль', callback_data='new_style'),
                types.InlineKeyboardButton('Загрузить новое изображение', callback_data='new_image')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_photo(call.message.chat.id, output_img)
            bot.send_message(call.message.chat.id, f'✨ Новое изображение', reply_markup=keyboard)


        # обработка данного callback-запроса завершена
        bot.answer_callback_query(callback_query_id=call.id)
# -----------------------------------------------------------------------------
# = = = Выполнение сценариев
@bot.message_handler(content_types=["text"])
def echo(message):

    user_id = str(message.from_user.id)
    # user_name = str(message.from_user.username)  # Log пользователя
    # time_sms = message.date

    word = message.text.capitalize().replace(".", ",")
    if word == "/":
        pass
    else:
        iskl = ":;!_*-+()\/#%&~'^$`{}[]<>|\"[[]]"  # Убираем спец. символы
        for n in iskl:
            if n in message.text:
                word = word.capitalize().replace(n, " ")
            else:
                pass

    # ---Сценарий - завершение всех команд
    if word == "/":

        #  обнуляем словари и маркеры
        normalization(user_id)

        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
            types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
            types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

    # --- Сценарий -  показ примера стиля изображения
    elif show_marker[user_id] == 1:

        style_marker[user_id] = 0

        Nomer = message.text
        if Nomer.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)

            buttons = [
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style'),
                types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Отмена', callback_data='cancel')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            if Nomer <= len(list_style) and Nomer > 0:

                show_marker[user_id] = 0
                #  название стиля изображения
                name_style = list_style[Nomer][0]
                dic_style[user_id] = [name_style, random_image(name_style) ]
                #  вывод изображения стиля
                img_sample = img_show( random_image (name_style) )

                text = f'✔️ - выбран стиль: {list_style[Nomer][1]}'
                bot.send_photo(message.chat.id, img_sample )
                bot.send_message(message.chat.id, f'{text}', reply_markup=keyboard)

            else:
                bot.send_message(message.chat.id, f'🚫 {Nomer} - такого номера в cписке нет'
                                                  f'🖍️Выберите изображение стиля:\n {text_style}',
                                 reply_markup=keyboard)
        else:
            text_3 = f'‼️ Введите цифрами номер из списка.'
            bot.send_message(message.chat.id, f'{text_3}\n {text_style}', reply_markup=keyboard)

    # --- Сценарий -  выбор стиля
    elif style_marker[user_id] == 1:

        # style_marker[user_id] = 0
        show_marker[user_id] = 0

        Nomer = message.text
        if Nomer.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)

            if Nomer <= len(list_style) and Nomer > 0:

                style_marker[user_id] = 0
                #  название стиля изображения
                name_style = list_style[Nomer][0]
                dic_style[user_id] = [name_style, random_image(name_style)]

                buttons = [
                    types.InlineKeyboardButton('Пример стиля', callback_data='show_style'),
                    types.InlineKeyboardButton('Добавить изображение', callback_data='new_image'),
                    types.InlineKeyboardButton('Меню', callback_data='menu'),
                    types.InlineKeyboardButton('Отмена', callback_data='cancel')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)

                if dic_img.get(user_id) is not None:

                    text_1 = f'✔️ - выбран стиль: {list_style[Nomer][1]}'

                    buttons = [
                        types.InlineKeyboardButton('Применить', callback_data='apply'),
                        types.InlineKeyboardButton('Новое изображение', callback_data='new_image'),
                        types.InlineKeyboardButton('Меню', callback_data='menu'),
                        types.InlineKeyboardButton('Отмена', callback_data='cancel')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)

                    if image_marker[user_id] == 1:

                       image_marker[user_id] = 0
                       bot.send_message(message.chat.id, f'[ ■_■_□_□_□ ] ...выполняю перенос стиля...\n'
                                                         f'⏰... это займет не более 1 мин.')

                       output_img = style_apply(dic_img[user_id], dic_style[user_id])

                       buttons = [
                           types.InlineKeyboardButton('Меню', callback_data='menu'),
                           types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                           types.InlineKeyboardButton('Выбрать новый стиль', callback_data='new_style'),
                           types.InlineKeyboardButton('Загрузить новое изображение', callback_data='new_image')
                       ]
                       keyboard = types.InlineKeyboardMarkup(row_width=2)
                       keyboard.add(*buttons)

                       bot.send_photo(message.chat.id, output_img)
                       bot.send_message(message.chat.id, f'✨ Новое изображение', reply_markup=keyboard)

                    else:
                        bot.send_message(message.chat.id, f'{text_1}\nПрименить стиль к изображению или загрузить новое?'
                                     , reply_markup=keyboard)
                else:
                    #  название стиля изображения
                    name_style = list_style[Nomer][0]
                    dic_style[user_id] = [name_style, random_image(name_style)]

                    text_2 = f'✔️ - выбран стиль: {list_style[Nomer][1]}'
                    buttons = [
                        types.InlineKeyboardButton('Пример стиля', callback_data='show_style'),
                        types.InlineKeyboardButton('Описание команд', callback_data='info'),
                        types.InlineKeyboardButton('Меню', callback_data='menu'),
                        types.InlineKeyboardButton('Отмена', callback_data='cancel')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)
                    bot.send_message(message.chat.id, f'{text_2}\nЗагрузите изображение',  reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, f'🚫 {Nomer} - такого номера в cписке нет'
                                                  f'🖍️Выберите изображение стиля:\n {text_style}',
                                 reply_markup=keyboard)
        else:
            text_3 = f'‼️ Введите цифрами номер из списка.'
            bot.send_message(message.chat.id, f'{text_3}\n {text_style}', reply_markup=keyboard)


    # --- Сценарий команды нет в списке
    else:

        style_marker[user_id] = 0
        show_marker[user_id] = 0

        text_3 = ('❌ Неизвестная команда.')
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text_3, reply_markup=keyboard)

# ----------------------------------

bot.polling(none_stop=True)