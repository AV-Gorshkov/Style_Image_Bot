import requests

from setting import *
from file_img import *
from model_cnn import *
# from setting import TG_TOKEN

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
# id_support = '5170069430'

# --- Маркеры
# add_marker = {}  # маркер добавления продукта

# !!!!!!!!!!!!!!!!!!!!!
style_marker = {}  # маркер стиля изображения
show_marker = {}
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# edit_marker = {}  # маркер кнопка Edit
# alien_marker = {}  # маркер управление чужим списком
# union_marker = {}  # маркер добавить целый список
# share_marker = {}  # маркер расшаривания списка (изменение ID на список для просмотра)
# back_marker = {}  # маркер вернуть позицию обратно в список
# sms_marker = {}  # маркер написания СМС в поддержку от User
# drop_id_marker = {}  # маркер удаления из Базы Данных по ID
# serv_marker = {}  # маркер сервесный
# avail_marker = {}  # маркер выбранного чужого списка
#
# activ_list = {}  # маркер активного списка мой / общий  my/all

# ---Кнопки
# share_but = {}  # кнопка расшарить свой список
# friendly_but = {}  # кнопка доступные списки моих друзей
# alien_but = {}  # кнопка ID кто имеет доступ к моим спискам
# y_but = {}  # кнопка да
# n_but = {}  # кнопка нет
# up_but = {}  # кнопка обновить

# --- Словари


# if not dic_list:
#     dic_list = dict(base.out_dict_list())
# else:
#    pass
# ---------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  словари для Style

dic_style = {}  # название (номер) изображения для стиля dic_style[user_id]
dic_img = {}   # название загруженного файла и размер



# !!!!!!!!!!!!!!!!!!!!!!!!!!
# if not dic_numb:
#     dic_numb = dict(base.out_dict_numb())
# else:
#    pass
# -----
#
# dic_list_union = {}  # новый список из сообщения
# dic_list_clear = {}  # список для удаления названий основного списка при "Заменить"
# dic_alien_user = {}  # ID активного чужого списка (только одна пара Ключ(мой ID)=Значение(ID чужого списка))
#
# dic_share = {}  # список ID-мой и ID-кому открыт доступ к списку
# dic_availibale = {}  # список ID доступных списков для просмотра -> ID(кому открыт доступ): [ID кто предоставил]
#
# list_user_id = {}  # список всех iD и логинов участников бота
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
/sample - (Sample, Пример) - показать пример изображения стиля.
/style - (Style, Стиль) - выбор изображение стиля.
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
    # add_marker[user_id] = 0
    # tag_marker[user_id] = 0
    # edit_marker[user_id] = 0
    # union_marker[user_id] = 0
    # share_marker[user_id] = 0
    # back_marker[user_id] = 0
    # sms_marker[user_id] = 0
    # share_but[user_id] = 0
    # friendly_but[user_id] = 0
    # alien_but[user_id] = 0
    # y_but[user_id] = 0
    # n_but[user_id] = 0
    # up_but[user_id] = 0
    # drop_id_marker[user_id] = 0
    # serv_marker[user_id] = 0
    _text = f'❌ Неизвестная команда.'
    return _text

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

#     # ----- Запись всех ID и Логинов в список Чат-Бота
# def id_log(user_id, user_name, time_sms):
#     time_sms = str(datetime.fromtimestamp(time_sms).strftime('%d.%m.%Y'))
#     list_user_id[user_id] = [user_name, time_sms]
#     # base.in_user_id(user_id, list_user_id[user_id])  # запись в БД Repl.it


# ----- подмена  user_id для чужого списка -возможно функция не нужна ===!!!!!!!!!

# def alien_user(user_id):
#     user_id = dic_alien_user[user_id][0]  # - подмена  user_id
#     user_name_alien = list_user_id[user_id][0]
#     return [user_id, user_name_alien]
#
#
# # ----- Показать список
# def show_list(user_id, activ):
#     prod = ""
#     j = 0  # для счета позиций списка
#     for i in dic_list[user_id][activ]:
#         j += 1
#         Z = str(j)
#         if dic_numb[user_id].get(activ) is not None:
#             if Z in dic_numb[user_id][activ]:
#                 text2 = '~' + str(i) + '~'  # ✅  ✔️
#                 # text2 = '~' + str(j) + " " + str(i) + '~'  # ✅  ✔️
#                 prod = (f'{prod}✅ {j} {text2} \n')
#             else:
#                 prod = (f'{prod} {j}  {i} \n')
#         else:
#             prod = (f'{prod} {j}  {i} \n')
#     return prod
#
# # ----- Проверка активного списка мой/ общий
# def list_activ(user_id):
#     if activ_list.get(user_id) is None:
#         activ_list[user_id] = 'Мой'
#     activ = activ_list[user_id]
#
#     if dic_list.get(user_id) is None:
#         dic_list[user_id] = {}
#     if dic_numb.get(user_id) is None:
#         dic_numb[user_id] = {}
#     return activ

# --------------------------------------------------------------
# = = =  Сервисные команды

# my_id='5170069430'

# user_name = str(message.from_user.username) # имя
# user_Fname = message.from_user.first_name
# user_surname = message.from_user.last_name   # фио пользователя message.chat.id
# /ch=str("586115676")
# bot.send_message(ch, f'{user_id} , @{user_name} - { user_Fname} ') #сообщение уходит в чат другого пользователя -----!!!!!!!!!!!!!!!!!!
# bot.send_message(ch, "123") #сообщение уходит в чат другого пользователя



# ------------------------------------------------------------
# = = = Команды для управления приложением
# -----  Справка
@bot.message_handler(
    commands=["Справка", "СПРАВКА", "справка", "help", "Help", "HELP", "hElp", "heLp", "helP", "HElp", "HElP", "HELp",
              "hELp", "hELP", "heLp", "heLP", "?", "start"])  # регистрация фун-ции на сервере телеграмм
def help(message):
    user_id = str(message.from_user.id)  # id пользователя

    #  обнуляем словари и маркеры
    normalization(user_id)

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

    #  обнуляем словари и маркеры
    normalization(user_id)

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

    #  обнуляем словари и маркеры
    normalization(user_id)

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Справка', callback_data='help'),
        types.InlineKeyboardButton('Новый список', callback_data='add')
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
        types.InlineKeyboardButton('Завершить', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'Выберите изображение стиля для переноса:\n {text_style}', reply_markup=keyboard)

# ----- Отмена всех команд /end
@bot.message_handler(commands=["Отмена", "ОТМЕНА", "отмена", "end", "END", "End", "/"])
def end(message):
    user_id = str(message.from_user.id)

    #  обнуляем словари и маркеры
    normalization(user_id)

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Новый список', callback_data='add'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

# -----Показ стилей для изображения /sample - (Sample, Пример)
@bot.message_handler(commands=["sample", "SAMPLE", "Sample", "пример", "Пример", "ПРИМЕР"])
def show(message):
    user_id = str(message.from_user.id)

    show_marker[user_id]  = 1
    style_marker[user_id] = 0

    # ------
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Завершить', callback_data='cancel'),
        types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'Выберите категорию стиля изображения:\n {text_style}',
                     reply_markup=keyboard)

# ----- получение фото
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

    # тип файла # bot.send_message(message.chat.id, f' 🟢 {file_extension}')
    if file_extension in ['.jpg', '.jpeg', '.png']:

        downloaded_file = bot.download_file(file_info.file_path)
        # img_photo = message.photo[len(message.photo) - 1].file_id

        #  загрузка изображения
        text = f'img_{user_id}.jpg'
        with open( text , 'wb' ) as new_file:
            new_img = new_file.write(downloaded_file)

        #     размер исходного изображения
        in_img_size = img_size(text)
        #  название исходного файла и размер  в словарь
        dic_img[user_id] = [text, in_img_size ]

        #  проверка на выбор изображения стиля
        if dic_style.get(user_id) is not None:

           bot.send_message(message.chat.id, f'[ ■_■_■_□_□_□_□ ]\n'
                                             f'... выполняю перенос стиля...\n'
                                             f'... это займет не более 1 мин.')

           # изображение контент
           img_content = image_loader (text)
           #  изображение для модели
           img_input = img_content.clone()

           output_model, score_style, score_content = run_style_transfer(model_vgg, cnn_normalization_mean,
                                                                   cnn_normalization_std, img_content,
                                                                   img_style, img_input,
                                                                   num_steps=N_Step,
                                                                   style_weight=1000000,
                                                                   content_weight=1)

           # преобразование изображение в исходный размер
           img_resize = resize_loader(output)
           # imshow(img_resize)

           buttons = [
               types.InlineKeyboardButton('Меню', callback_data='menu'),
               types.InlineKeyboardButton('Завершить', callback_data='cancel'),
               types.InlineKeyboardButton('Новый стиль', callback_data='new_style'),
               types.InlineKeyboardButton('Новое изображение', callback_data='new_image')
           ]
           keyboard = types.InlineKeyboardMarkup(row_width=2)
           keyboard.add(*buttons)

           bot.send_photo(message.chat.id, img_resize, caption='Новое изображение', reply_markup=keyboard )


           # bot.send_message(message.chat.id, f' получено размер🟢 {in_img_size}')
        else:
            # изображения стиля не выбрано
            # предложить варианты стиля
            style_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'Выберите изображение для переноса стиля:\n {text_style}',
                             reply_markup=keyboard)

        # bot.send_message(message.chat.id, f' получено размер🟢 {in_img_size}' )
    else:
        bot.send_message(message.chat.id, f' Неудалось распознать файл.\n'
                                          f'Пришлите изображение в фармате "jpеg" или "png" ')

     #    отправить фото в ответ
    # img_photo = message.photo[len(message.photo) - 1].file_id
    # bot.send_photo(message.chat.id, img_photo, caption='Ваш текст')


# ---------------------------------------------
# = = = Реагирование на кнопки = = =
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = str(call.from_user.id)
    message_id = call.message.message_id
    chat_id = call.message.chat.id

    if call.message:
        # ----- Выполнение кнопки новое изобажение
        if call.data == "new_image":

            show_marker[user_id]   = 0
            style_marker[user_id] = 0

            bot.send_message(call.message.chat.id, f'🟢 Загрузите свое изображение для применения стиля', reply_markup=keyboard)

        #  Выбор стиля для изображения
        elif call.data == "new_style":

            style_marker[user_id] = 1
            show_marker[user_id]  = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'Выберите изображение стиля для переноса:\n {text_style}',
                             reply_markup=keyboard)

        #  Показ примера стиля
        elif call.data == "show_style":

            style_marker[user_id] = 0
            show_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Пример стиля', callback_data='show_style')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'Выберите категорию стиля изображения:\n {text_style}',
                             reply_markup=keyboard)

        # ----- Кнопка Справка
        elif call.data == "help":

            style_marker[user_id] = 0
            show_marker[user_id]  = 0

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

           # -----Выполнение Кнопка "Отмена" - завершение всех команд
        elif call.data == "cancel":

            style_marker[user_id] = 0
            show_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

        # ----- Выполнение кнопка "Меню"
        elif call.data == 'menu':

            style_marker[user_id] = 0
            show_marker[user_id] = 0

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

            style_marker[user_id] = 0
            show_marker[user_id] = 0

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

        bot.answer_callback_query(callback_query_id=call.id)  # обработка данного callback-запроса завершена.
# -----------------------------------------------------------------------------
# = = = Выполнение сценариев = = =
@bot.message_handler(content_types=["text"])
def echo(message):
    # global id_support

    user_id = str(message.from_user.id)
    # user_name = str(message.from_user.username)  # Log пользователя
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
    # normalization(user_id)

    # ---Сценарий - завершение всех команд
    if word == "/":

        style_marker[user_id] = 0
        show_marker[user_id] = 0

        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)


    # --- Сценарий -  показ примера стиля изображения
    elif show_marker[user_id] == 1:

        style_marker[user_id] = 0
        show_marker[user_id] = 0

        #     -----------------------
        #  ✔️ ‼️
        Nomer = message.text
        if Nomer.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)

            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            # bot.send_message(message.chat.id, f'{list_style}')
            if Nomer <= len(list_style) and Nomer > 0:

                #  название стиля изображения
                name_style = list_style[Nomer][0]
                dic_style[user_id] = name_style

                img_proba = img_style_proba( dic_style[user_id]  )

                text = f'✔️ - выбран стиль: {name_style}'

                bot.send_photo(message.chat.id, img_proba )
                bot.send_message(message.chat.id, f'{text}', reply_markup=keyboard)

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
            bot.send_message(message.chat.id, f'{text_3}\n {text_style}', reply_markup=keyboard)


    # --- Сценарий -  выбор стиля
    elif style_marker[user_id] == 1:

        style_marker[user_id] = 0
        show_marker[user_id] = 0

        Nomer = message.text
        if Nomer.isnumeric() == True:  # провкрка на число
            Nomer = int(message.text)

            buttons = [
                types.InlineKeyboardButton('Завершить', callback_data='cancel'),
                types.InlineKeyboardButton('Меню', callback_data='menu')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            if Nomer <= len(list_style) and Nomer > 0:

                #  название стиля изображения
                name_style = list_style[Nomer][0]
                dic_style[user_id] = name_style

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



    # --- Сценарий команды нет в списке
    else:

        style_marker[user_id] = 0
        show_marker[user_id] = 0

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