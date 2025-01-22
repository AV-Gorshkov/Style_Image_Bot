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
from model_cnn import *

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

    return ( width, height)

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
      out_image.to(device, torch.float)
      out_image = img_show (out_image)

      return out_image

#  - - - пример случайного изображения стиля
def img_style_sample (name_style):

    rnd_img = random_image (name_style)
    img_sample = img_show(rnd_img)

    return img_sample

#  выбор случайного изображения стиля из колекции
def random_image (name_style):
    num = random.randint(0, 2)
    return tensor_style_img [name_style] [num]

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
tensor_style_img = {}

for key, val in dict_image.items():
  for el in val:
   tensor_img =image_loader ( Data_Dir + key + '/' + el)
   if tensor_style_img.get( key ) is None:
      tensor_style_img[ key ] = [ tensor_img]
   else:
      tensor_style_img[ key ]. append( tensor_img )


 #  перенос стиля на изображение

def style_apply(lst_img, lst_style ):

    #  начальный размер файла
    in_size = lst_img[1]
    #  изображение стиля
    img_style = lst_style[1]
    # изображение контент
    img_content = image_loader ( lst_img[0])
    #  изображение для модели
    img_input = img_content.clone()
    # запуск модели CNN
    output_model, score_style, score_content = run_style_transfer(model_vgg, cnn_normalization_mean,
                                                                   cnn_normalization_std, img_content,
                                                                   img_style, img_input,
                                                                   num_steps=N_Step,
                                                                   style_weight=1000000,
                                                                   content_weight=1)

    # преобразование изображение в исходный размер
    output_img = resize_loader(output_model, in_size)

    return output_img


# пример тензора
# print(dict_image)
# print(Img_Size)
# print(style_img['cubism'][1])
# print(tensor_style_img['cubism'][1].shape)

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

