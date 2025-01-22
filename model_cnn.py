import requests

import os
import time
import glob
import cv2
import copy
import random

# from tqdm.notebook import tqdm
# from collections import defaultdict

import numpy as np

import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim

# from torchsummary import summary
# from IPython.display import clear_output
# import seaborn as sns

import torch
import torchvision
from torchvision import transforms
import torchvision.models as models

import matplotlib.pyplot as plt
from PIL import Image

# контроль предупреждений
import warnings
warnings.simplefilter("ignore")

from setting import *

# from file_img import *
#
# #  вывод изображения стиля
# name_style = 'cubism'
# print( img_style_proba (name_style) )
#  # img_show(style_img['cubism'][1][0] )
# plt.show()


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# print(device)

# = = =
# вспомогаьельные функйии для CNN

# - подсчет loss для исходного изображения

class ContentLoss(nn.Module):

    def __init__(self, target,):
        super(ContentLoss, self).__init__()

        self.target = target.detach()

    def forward(self, input):
        self.loss = F.mse_loss(input, self.target)
        return input

# - функция потерь для стиля
# матрица Грама
def gram_matrix( input):

    a, b, c, d = input.size()
    # a - размер батча size=1
    # b - кол-в карт
    # c,d - размер

    features = input.view(a * b, c * d)

    G = torch.mm(features, features.t())
    # произведение по Граму
    #  нормализуем значения матрицы грамма
    # деления на количество элементов в каждой карте объектов.

    return G.div(a * b * c * d)

#  - подсчет loss для изображения стиля
class StyleLoss(nn.Module):

    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input

# - нормализация тензора изображений для обучения модели

cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()

        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):

        return (img - self.mean) / self.std

# - функция рассчета признаков стиля и контента

def get_style_model_and_losses(cnn, normalization_mean, normalization_std,
                               style_img, content_img,
                               content_layers=Content_Layers,
                               style_layers=Style_Layers):
    cnn = copy.deepcopy(cnn)

    normalization = Normalization(normalization_mean, normalization_std).to(device)

    content_losses = []
    style_losses = []

    model = nn.Sequential(normalization)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = 'bn_{}'.format(i)
        else:
            raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

        model.add_module(name, layer)

        if name in content_layers:

            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module("content_loss_{}".format(i), content_loss)
            content_losses.append(content_loss)

        if name in style_layers:

            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module("style_loss_{}".format(i), style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]

    return model, style_losses, content_losses

# - оптимизатор

def get_input_optimizer(input_img):
    optimizer = optim.Adam([input_img.requires_grad_()])
    return optimizer

# - обучение модели (процесс переноса стиля)

def run_style_transfer(cnn, normalization_mean, normalization_std,
                       content_img, style_img, input_img, num_steps=100,
                       style_weight=1000000, content_weight=1):

# получение представлений признаков стиля и контента (из промежуточных слоёв)
    model, style_losses, content_losses = get_style_model_and_losses(cnn,
        normalization_mean, normalization_std, style_img, content_img)

# вызов оптимизатора
    optimizer = get_input_optimizer(input_img)

    run = [0]
    while run[0] <= num_steps:

        def closure():

            global sc_style, sc_content

            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)

            style_score = 0
            content_score = 0

#  подсчет Loss для слоев стиля
            for sl in style_losses:
                style_score += sl.loss

#  подсчет Loss для слоев контента
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            sc_style, sc_content =  style_score.item(), content_score.item()

            return  style_score + content_score

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)

    return (input_img, sc_style, sc_content )

# загрузка модели vgg19

model_vgg = models.vgg19(pretrained=True).features.to(device).eval()

# print(model_vgg)