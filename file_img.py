# загрузка стилей для изображений
# вспомогательные функции по обработке изображений

import os
import sys
import glob

import random
import matplotlib.pyplot as plt

import torch
import torchvision
from torchvision import transforms

from PIL import Image

# from setting import Data_Dir, Img_Size, device
import requests
from setting import *

# img7 = Image.open("file_0.jpg")

# print('7--', img7.size      )

#  = = = Поворот!
# from PIL import Image
#
# img = Image.open("forest.jpg")
# # поворот на 90 градусов
# img2 = img.rotate(90)
# # сохраняем новое изображение
# img2.save("forest_new.jpg")

# '⚠️

# = = =

def img_size (in_img):

    in_img = Image.open(in_img)
    height, width = in_img.size

    return (height, width)

# --- преобразования изображения в тензор

def image_loader(image_name):

    loader = transforms.Compose([
      transforms.Resize(Img_Size),
      transforms.ToTensor()])

    image = Image.open(image_name)
    image = loader(image).unsqueeze(0)

    return image.to(device, torch.float)

# ---  преобразование тензора в изображение
# рисование картинки
def img_show(tensor):

    unloader = transforms.ToPILImage()
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    # plt.imshow(image)

    return  image



# --- возврат изображения в исходный размер из тензоза
# in_size - исходный размер входящего изображения
def resize_loader(in_image, in_size):

      out_loader = transforms.Compose([
              transforms.Resize(in_size)
              ])
      out_image = out_loader(in_image)

      return out_image.to(device, torch.float)

#  - - - пример случайного изображения стиля
def img_style_proba (name_style):

    num = random.randint(0, 2)
    # key = list_style[Nomer][0]
    img_proba = img_show(style_img[name_style][num])

    return img_proba

# = = =
# загрузка данных стилей из папки

data_image_paths = glob.glob(f"{Data_Dir}/*/*.jpg")

# - названия стилей помещены в словарь
dict_image = {}

for path in data_image_paths:
  if dict_image.get( path.split('\\')[-2] ) is None:
    dict_image[ path.split('\\')[-2] ] = [ path.split('\\')[-1] ]
  else:
    dict_image[ path.split('\\')[-2] ]. append(path.split('\\')[-1])

# - преобразуем изображения стилей в тензоры и упакуем их в словарь
style_img = {}

for key, val in dict_image.items():
  for el in val:
   tensor_img =image_loader ( Data_Dir + key + '/' + el)
   if style_img.get( key ) is None:
      style_img[ key ] = [ tensor_img]
   else:
      style_img[ key ]. append( tensor_img )

# пример тензора
# print(dict_image)
# print(Img_Size)
# print(style_img['cubism'][1][0])


#  вывод изображения стиля
# tx = 'cubism'
#
# im = img_style_proba (tx)
# print(im)
#
# print(im.format, im.size, im.mode)
#
# ph = im.show()
#
# print(ph)


# img_show(style_img['cubism'][1][0] )
# plt.show()
# ph = Image.open (im)

# ph = open( img_style_proba (tx), 'rb')

#     new_img = new_file.write(downloaded_file)

# print('123')


# name1 = 'file_0.jpg'
# img = Image.open(name1)
# plt.imshow(img)
# print(Image.open(name1) )
# plt.show()

# удалить файл
# os.remove(name1)

