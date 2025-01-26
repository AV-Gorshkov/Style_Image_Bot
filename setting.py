# исходные данные, константы

import os
import sys
import torch
from PIL import Image

# путь к файлам стиля
Data_Dir = os.path.join( sys.path[0], 'style\\')

# --- определение размера для сжатия картинок
path_ = os.path.join(sys.path[0], 'style\\grisaille\\1.jpg')
img_style = Image.open(path_)
height, width = img_style.size
img_nrows = min(200, height)
img_ncols = int(width * img_nrows / height)

Img_Size = (img_nrows, img_ncols)
# print( Img_Size )

# --- Список стилей
text_style = """
1. Абстракционизм
2. Кубизм
3. Графити
4. Гризайль
5. Импрессионизм
6. Постимпрессионизм
7. Поп-Арт
"""

list_style = {
    1 : ['abstractionism', 'Абстракционизм'],
    2 : ['cubism', 'Кубизм'],
    3 : ['graffiti', 'Граффити'],
    4 : ['grisaille', 'Гризайль'],
    5 : ['impressionism', 'Импрессионизм'],
    6 : ['post-impressionism', 'Постимпрессионизм'],
    7: ['pop-art', 'Поп-Арт' ]
    }

# ---- токен_бот
TG_TOKEN = "7514605007:AAGkbIAMYqF91eJHopgt9MfaG3SCaYryRwk"

# --- определение девайса
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#  --- слои для маодели
#  слой контент
Content_Layers = ['conv_5']
# слой стиля
Style_Layers = ['conv_1',
                'conv_2',
                'conv_3',
                'conv_4',
                'conv_5'
               ]

# ---  кол-во итерций переноса стиля

dic_n_step = {'min': 200,
              'med': 600,
              'max': 1000
             }