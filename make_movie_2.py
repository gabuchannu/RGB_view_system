from ctypes import alignment
import sys
import time
import cv2
import os
import threading
import movie_to_frame
import system_screen
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors
from xml.etree.ElementTree import QName
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont
import system_screen as sc


class movie_maker:
    def __init__(self, folder_pass):
#        super(self).__init__()
        #---------------------------------------
        #RGB画像を使って画像の比率を取得しておく
        #---------------------------------------
        with open(folder_pass + str("1_rgb") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)
            self.rgb_image = Image.fromarray(data) #darrayを画像に変換
        self.height, self.weight, self.channel = data.shape
        self.frame_counter = 2



    def make_space(self, main_widget, folder_pass, frame):
                # FigureCanvasに表示するグラフ
        self.fig = Figure(facecolor="#f0f0f0", dpi=100, figsize=(self.weight/300, self.height/300), tight_layout="True") #FIgureとして枠を作る
#        self.fig.patch.set_facecolor("#f0f0f0")
        # グラフを表示するFigureCanvasを作成
        self.fc = FigureCanvas(self.fig) #キャンバスにfigを入れる
        self.fc.setParent(main_widget) #main_widgetの子にする
        FigureCanvas.setSizePolicy(self.fc,
                                QSizePolicy.Fixed,
                                QSizePolicy.Fixed,
                                )
        FigureCanvas.updateGeometry(self.fc)
        # グラフの設定
        self.fc.axes = self.fig.add_subplot(1, 1, 1)
#        self.fc.axes.set_axis_off() #軸要らないから消す
        #self.fc.setContentsMargins(0,0,0,0) #四隅の余白0にする
#        first_frame = self.frame_rgb(folder_pass, frame)
#        return first_frame


    def frame_rgb(self, folder_pass, frame):
        #self.fc.axes = self.fig.add_subplot(1, 1, 1)

        with open(folder_pass + str(frame) + str("_rgb") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)
            image = Image.fromarray(data) #darrayを画像に変換

#        fc.axes.plot([1, 2, 3], [2, 3, 4])
#        new_image = Image.fromarray(cv2.resize(data, dsize= None, fx=0.5, fy=0.5))

        self.fc.axes.imshow(image)
        self.fc.axes.set_axis_off() #軸要らないから消す
        # 描画設定
        #self.fc.setParent(main_widget)
#        FigureCanvas.setFixedSize(self.weight*0.5, self.height*0.5)
#         FigureCanvas.setSizePolicy(self.fc,
#                                 QSizePolicy.Fixed,
#                                 QSizePolicy.Fixed,
# #                                 QtWidgets.QSizePolicy.Expanding
#                                 )
#         FigureCanvas.updateGeometry(self.fc)
#        self.fig.tight_layout() #Canvasと画像の間の余白を狭くする
        #self.fig.patch.set_alpha(0)
#        p = self.fc.palette()
#        p.setColor(self.fc.backgroundRole(), QColor(0, 0, 0, 128)) # 背景色
#        self.fc.setPalette(p)
        return self.fc



    def frame_rb(self, main_widget, folder_pass):
        # FigureCanvasに表示するグラフ
        self.fig_rb = Figure(facecolor="#f0f0f0", dpi=100, figsize=(self.weight/350, self.height/350), tight_layout="True")
#        self.fig_sub.patch.set_facecolor("#f0f0f0")
        # グラフを表示するFigureCanvasを作成
        self.fc_rb = FigureCanvas(self.fig_rb)
        # グラフの設定
        self.fc_rb.axes = self.fig_rb.add_subplot()

        with open(folder_pass + str("1_rb") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)

#        fc.axes.plot([1, 2, 3], [2, 3, 4])
#        new_image = Image.fromarray(cv2.resize(data, dsize= None, fx=0.5, fy=0.5))

        self.image_rb = data #ndarrayをセットする
        self.axis_image_rb = sns.heatmap(self.image_rb, ax = self.fc_rb.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar=False, square=True, vmin=0,vmax=255)
        #self.axis_image_sub = sns.heatmap(self.image_sub, ax = self.fc_sub.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
        # self.FigureCanvas_rb.draw() #表示する

#        self.fc.axes.imshow(new_image)
        self.fc_rb.axes.set_axis_off() #軸要らないから消す
        # 描画設定
        self.fc_rb.setParent(main_widget)
#        FigureCanvas.setFixedSize(self.weight*0.5, self.height*0.5)
        FigureCanvas.setSizePolicy(self.fc_rb,
                                QSizePolicy.Fixed,
                                QSizePolicy.Fixed,
#                                 QtWidgets.QSizePolicy.Expanding
                                )
        FigureCanvas.updateGeometry(self.fc_rb)
#        self.fig_sub.tight_layout() #Canvasと画像の間の余白を狭くする
#        self.fc_sub.setContentsMargins(0,0,0,0) #四隅の余白0にする
        return self.fc_rb
        

    def frame_rg(self, main_widget, folder_pass):
        # FigureCanvasに表示するグラフ
        self.fig_rg = Figure(facecolor="#f0f0f0", dpi=100, figsize=(self.weight/350, self.height/350), tight_layout="True")
#        self.fig_sub.patch.set_facecolor("#f0f0f0")
        # グラフを表示するFigureCanvasを作成
        self.fc_rg = FigureCanvas(self.fig_rg)
        # グラフの設定
        self.fc_rg.axes = self.fig_rg.add_subplot()

        with open(folder_pass + str("1_rg") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)

#        fc.axes.plot([1, 2, 3], [2, 3, 4])
#        new_image = Image.fromarray(cv2.resize(data, dsize= None, fx=0.5, fy=0.5))

        self.image_rg = data #ndarrayをセットする
        self.axis_image_rg = sns.heatmap(self.image_rg, ax = self.fc_rg.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar=False, square=True, vmin=0,vmax=255)
        #self.axis_image_sub = sns.heatmap(self.image_sub, ax = self.fc_sub.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
        # self.FigureCanvas_rb.draw() #表示する

#        self.fc.axes.imshow(new_image)
        self.fc_rg.axes.set_axis_off() #軸要らないから消す
        # 描画設定
        self.fc_rg.setParent(main_widget)
#        FigureCanvas.setFixedSize(self.weight*0.5, self.height*0.5)
        FigureCanvas.setSizePolicy(self.fc_rg,
                                QSizePolicy.Fixed,
                                QSizePolicy.Fixed,
#                                 QtWidgets.QSizePolicy.Expanding
                                )
        FigureCanvas.updateGeometry(self.fc_rg)
#        self.fig_sub.tight_layout() #Canvasと画像の間の余白を狭くする
#        self.fc_sub.setContentsMargins(0,0,0,0) #四隅の余白0にする
        return self.fc_rg


    def frame_gb(self, main_widget, folder_pass):
        # FigureCanvasに表示するグラフ
        self.fig_gb = Figure(facecolor="#f0f0f0", dpi=100, figsize=(self.weight/350, self.height/350), tight_layout="True")
#        self.fig_sub.patch.set_facecolor("#f0f0f0")
        # グラフを表示するFigureCanvasを作成
        self.fc_gb = FigureCanvas(self.fig_gb)
        # グラフの設定
        self.fc_gb.axes = self.fig_gb.add_subplot()

        with open(folder_pass + str("1_gb") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)

#        fc.axes.plot([1, 2, 3], [2, 3, 4])
#        new_image = Image.fromarray(cv2.resize(data, dsize= None, fx=0.5, fy=0.5))

        self.image_gb = data #ndarrayをセットする
        self.axis_image_gb = sns.heatmap(self.image_gb, ax = self.fc_gb.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar=False, square=True, vmin=0,vmax=255)
        #self.axis_image_sub = sns.heatmap(self.image_sub, ax = self.fc_sub.axes, cmap="rainbow", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
        # self.FigureCanvas_rb.draw() #表示する

#        self.fc.axes.imshow(new_image)
        self.fc_gb.axes.set_axis_off() #軸要らないから消す
        # 描画設定
        self.fc_gb.setParent(main_widget)
#        FigureCanvas.setFixedSize(self.weight*0.5, self.height*0.5)
        FigureCanvas.setSizePolicy(self.fc_gb,
                                QSizePolicy.Fixed,
                                QSizePolicy.Fixed,
#                                 QtWidgets.QSizePolicy.Expanding
                                )
        FigureCanvas.updateGeometry(self.fc_gb)
#        self.fig_sub.tight_layout() #Canvasと画像の間の余白を狭くする
#        self.fc_sub.setContentsMargins(0,0,0,0) #四隅の余白0にする
        return self.fc_gb


    def make_colorbar(self, main_widget):
        cm = plt.cm.get_cmap("rainbow")
        norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
#        colorbar_fig = Figure(facecolor="azure")
        colorbar_fig = Figure(facecolor="#f0f0f0", dpi=100, figsize=(10,1), tight_layout="True") #tight_layoutで自動調整を入れることで目盛り消えずに済む
        cax = colorbar_fig.add_subplot(1, 1, 1) 
#        colorbar_fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
        colorbar_fig_cv = FigureCanvas(colorbar_fig)
#        cax = colorbar_fig.add_axes([0, 0, 0.5, 0.2]) 
        #cax.axis("off") #軸要らないから消す
        colorbar_fig.colorbar(plt.cm.ScalarMappable(norm, cm), orientation="horizontal", cax=cax)
        colorbar_fig_cv.setParent(main_widget)
        FigureCanvas.setSizePolicy(colorbar_fig_cv,
                                QSizePolicy.Fixed,
                                QSizePolicy.Fixed,
                                )
        return colorbar_fig_cv


    def update_figure(self, folder_pass):
#        self.fc.axes = self.fig.add_subplot(1, 1, 1)

        with open(folder_pass + str(self.frame_counter) + str("_rgb") + ".dat", "rb") as f: #ファイルを開く
            data = np.load(f, allow_pickle=True)
            image = Image.fromarray(data) #darrayを画像に変換

#        fc.axes.plot([1, 2, 3], [2, 3, 4])
#        new_image = Image.fromarray(cv2.resize(data, dsize= None, fx=0.5, fy=0.5))
        #self.fc.axes.cla()
        sc.FigureWidget_rgb.axes.cla()
        self.fc.axes.imshow(image)
        self.fc.axes.set_axis_off() #軸要らないから消す
        self.frame_counter += 1

        sc.FigureWidget_rgb = self.fc
#        FigureCanvas.updateGeometry(self.fc)
#        self.fc.draw()
