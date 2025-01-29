# загрузка стилей для изображений
# вспомогательные функции по обработке изображений

import requests
import os
import sys
import glob

import random
import matplotlib.pyplot as plt

import torch
import torchvision
from torchvision import transforms

from PIL import Image

from setting import *
from model_cnn import *


# === Вспомогательные функции по предобработке изображений
#  --- размер изображения
def img_size (in_img):

    in_img = Image.open(in_img)
    width, height = in_img.size

    # если изображение вертикалбно, то повернуть
    if height > width :
       image_size = ( width, height)
       marker_rotate = 1
    else:
        image_size = (height, width)
        marker_rotate = 0

    return [ image_size, marker_rotate]

# --- преобразования изображения в тензор
def image_loader(image_name, rotate=0):

    loader = transforms.Compose([
      transforms.Resize(Img_Size),
      transforms.ToTensor()])

    image = Image.open(image_name)

    if rotate == 1:
        image = image.rotate(90, expand=True)

    image = loader(image).unsqueeze(0)

    return image.to(device, torch.float)

# ---  преобразование тензора в изображение
def img_show(tensor, rotate=0):

    unloader = transforms.ToPILImage()
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)

    if rotate == 1:
        image = image.rotate(-90, expand=True)
    # plt.imshow(image)

    return  image

# --- возврат изображения в исходный размер из тензоза
# in_size - исходный размер входящего изображения
def resize_loader(in_image, in_size, rotate=0):

      out_loader = transforms.Compose([
              transforms.Resize(in_size)
              ])
      out_image = out_loader(in_image)
      out_image.to(device, torch.float)
      out_image = img_show (out_image, rotate)

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


 #  перенос стиля на изображение
def style_apply(lst_img, lst_style, lst_step ):

    #  начальный размер файла
    in_size = lst_img[1]
    # поворот изображения
    rotate = lst_img[2]
    #  изображение стиля
    img_style = lst_style[1]
    # глубина стилизации
    N_Step = lst_step
    # изображение контент
    img_content = image_loader ( lst_img[0], rotate)
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
    output_img = resize_loader(output_model, in_size, rotate)

    return output_img
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

