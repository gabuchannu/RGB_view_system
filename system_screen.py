from copyreg import pickle
from ctypes import alignment
import sys
import matplotlib.pyplot as plt
import time
import cv2
import os
import seaborn as sns
import threading
import numpy as np
from xml.etree.ElementTree import QName
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image
import movie_to_frame
import make_movie_2
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets


class AppScreen(QWidget):

    def __init__(self):
        super(AppScreen, self).__init__()

        self.movie_class = movie_to_frame.movie_task() #別ファイルを呼びだす

        #self.main_widget = QWidget(self)

        #外側のキャンパスの初期サイズを指定
        self.setGeometry(0, 0, 1920, 1080)
        #ウィンドウタイトルを指定
        self.setWindowTitle("R-B成分・R-G成分・G-B成分 視覚化システム")

        self.first_ui() #uiを実行
        self.show() #表示する


    #------------------------
    #最初の画面のUIの実行関数
    #------------------------
    def first_ui(self):
        self.first_design_parts()
        self.make_first_layout()


    #-----------------------------------
    # main初期画面の使用パーツを定義
    #-----------------------------------
    def first_design_parts(self):
        self.title = QLabel("RGB成分値 視覚化 システム")
        self.title.setStyleSheet("font-size: 24pt")

        #from_layoutで使用するウィジェット
        self.url_name = QLabel("動画パス:") #"動画パス"っていうテキスト
        self.url_name.setStyleSheet("font-size: 20pt")

        self.url = QLineEdit() #入力する画面
        self.url.setText("C:\\Users\\Miku\\Downloads\\system_test.mp4") #初期で入っているパス
        #self.url.setText("C:\\Users\\Miku\\Downloads\\00000.png") #初期で入っているパス
        self.url.setStyleSheet("font-size: 30px")
        self.url.setFixedSize(1000, 50) #サイズを固定

        #ボタンウィジェット
        self.start_button = QPushButton("読み込み開始")
        self.start_button.setStyleSheet("font-size: 30px ; height: 35px ; width: 220px") #ボタンのスタイルを指定

        #ボタンがクリックされたらstart_progress関数を実行
        self.start_button.clicked.connect(self.button_click)

        #進行状況バーのウィジェット
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0) #0%スタート
        self.progressBar.setMaximum(100) #100%終わり
        self.progressBar.setFixedSize(1500, 60) #サイズを固定


    #----------------------------------
    #スタート画面のレイアウト作成
    #----------------------------------
    def make_first_layout(self):
        self.main_layout = QVBoxLayout() #1番外枠の全体の骨組みのレイアウト
        self.form_layout = QHBoxLayout() #フォーム全体に使う骨組みのレイアウト    

        #中央ぞろえでフォーム全体のウィジェットを作成
        self.form_layout.addStretch() #余白
        self.form_layout.addWidget(self.url_name) #form_layoutにウィジェットを追加
        self.form_layout.addWidget(self.url) #form_layoutにウィジェットを追加
        self.form_layout.addStretch() #余白

        self.main_layout.addStretch() #余白
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter) #main_layoutにタイトルウィジェットを追加 

        self.main_layout.addStretch() #余白
        self.main_layout.addLayout(self.form_layout) #main_layoutにform_layoutを追加

        self.main_layout.addStretch() #余白
        self.main_layout.addWidget(self.start_button, alignment=Qt.AlignHCenter) #main_layoutにボタンウィジェットを追加

        self.main_layout.addStretch() #余白
        self.main_layout.addWidget(self.progressBar, alignment=Qt.AlignHCenter) #main_layoutに進捗状況バーウィジェットを追加

        self.main_layout.addStretch() #余白

        self.setLayout(self.main_layout) #main_layoutをキャンパスにセットする


    #--------------------------------------
    #動画をダウンロードして画像処理を行う関数
    #--------------------------------------
    def download_movie(self):
#        self.movie_class.openfile(self.url.text()) #静止画のパスを引数に渡す
        self.frame_count = self.movie_class.openmovie(self.url.text()) #動画のパスを引数に渡す


    #------------------------------
    #ボタンを押したら実行される関数
    #------------------------------
    def button_click(self):
        th = threading.Thread(target=self.download_movie, daemon=True) #別スレッドで動画処理関数を実行
        th.start() #マルチスレッド開始

        count = 0
        while th.is_alive(): #別スレッド内の動画処理が行われている間は回り続ける
            if count == 80: #79%まで
                break
            else: #進捗状況バーを進める
                QTest.qWait(1)
                self.progressBar.setValue(count)
                count = count + 1
                QApplication.processEvents()
            
        th.join() #動画処理関数が終わるまで待つ

        while count != 101: #マルチスレッドが終わったら100%まで持ってく
            QTest.qWait(1)
            self.progressBar.setValue(count)
            count = count + 1
            QApplication.processEvents()

        self.clearLayout(self.main_layout) #最初のスクリーンからWidgetを全て消す
        self.second_ui() #消したスクリーンを使って2つめのスクリーンを作る
        #最初の画面を入れる
        self.show() #表示する

    #--------------------------
    #2つ目の画面のUIを作る関数
    #--------------------------
    def second_ui(self):
        self.second_design_parts()
        self.make_second_layout()

#-----------------------------------
# 動画再生画面で使用するパーツを定義
#-----------------------------------
    def second_design_parts(self):

        #レイアウト上に表示するシステムのタイトル
        self.second_title = QLabel("RGB成分値 視覚化 システム")
        self.second_title.setStyleSheet("font-size: 24pt")

        #RGB_layoutで使用するウィジェット
        self.rgb_name = QLabel("元画像") #"元画像"っていうテキスト
        self.rgb_name.setStyleSheet("font-size: 20pt")

        #RB_layoutで使用するウィジェット
        self.rb_name = QLabel("R-B成分値") #"R-B成分値"っていうテキスト
        self.rb_name.setStyleSheet("font-size: 20pt")

        #RG_layoutで使用するウィジェット
        self.rg_name = QLabel("R-G成分値") #"R-G成分値"っていうテキスト
        self.rg_name.setStyleSheet("font-size: 20pt")

        #GB_layoutで使用するウィジェット
        self.gb_name = QLabel("G-B成分値") #"G-B成分値"っていうテキスト
        self.gb_name.setStyleSheet("font-size: 20pt")

        #ボタンウィジェット
        self.play_button = QPushButton("再生開始")
        self.play_button.setStyleSheet("font-size: 30px ; height: 35px ; width: 220px") #ボタンのスタイルを指定

        #ボタンがクリックされたらstart_play関数を実行
        self.play_button.clicked.connect(self.start_play)

        #画像のデータファイルを取得する
        number = self.url.text().rfind(".") #ファイルの種類名を取得
        self.folder_pass = self.url.text()[:number] #.aviより前を持ってくる

        self.make_frame = make_movie_2.movie_maker(self.folder_pass)

        #動画再生画面のウィジット(元画像)
        #self.FigureCanvas = make_frame_class.before_start(folder_pass, "rgb")
        # with open(folder_pass + str("1_rgb") + ".dat", "rb") as f: #ファイルを開く
        #     data = np.load(f, allow_pickle=True)
        #     self.image = Image.fromarray(data) #darrayを画像に変換
        
        #height, weight, channel = data.shape #画像を埋め込むサイズを決める

        #height, weight = self.pick_frame.pick_size(folder_pass) #画像を埋め込むサイズを決める
        self.FigureWidget_rgb = self.make_frame.make_rgb_space(self, self.folder_pass, 1)
    
        #self.FigureWidget = QWidget(self) #動画埋め込みのためのウィジェット
        # self.FigureWidget.setFixedSize(weight*0.2, height*0.2) #サイズを固定
        # self.FigureLayout = QVBoxLayout(self.FigureWidget) #ウィジェットにFigureLayoutを追加する
        #self.FigureLayout.setContentsMargins(0,0,0,0) #四隅の余白0にする
        #self.Figure = plt.figure() #self.Figureという描画領域を作成する
        #self.FigureCanvas = FigureCanvas(self.Figure) #self.Figureを表示するキャンバスを作成
        # self.FigureLayout.addWidget(self.FigureCanvas) #キャンバスをFigureLayoutに入れる

#         self.axis = self.Figure.add_subplot(1,1,1) #画像表示のために軸作る
#         self.axis.set_axis_off() #軸要らないから消す
#         self.Figure.tight_layout() #Canvasと画像の間の余白を狭くする

#         self.axis_image = self.axis.imshow(self.image) #軸と画像を合わせる
#  #        self.axis_image.set_data(self.image) #画像をセットする
#         self.FigureCanvas.draw() #表示する

        #動画再生画面のウィジット(R-B成分値)
        self.FigureWidget_rb = self.make_frame.frame_rb(self, self.folder_pass)  
        # with open(folder_pass + str("1_rb") + ".dat", "rb") as f: #ファイルを開く
        #     data_rb = np.load(f, allow_pickle=True) #ndarrayで読み込み

        # self.FigureWidget_rb = QWidget(self) #動画埋め込みのためのウィジェット
        # self.FigureWidget_rb.setFixedSize(weight*0.25, height*0.25) #サイズを固定
        
        # self.FigureLayout_rb = QVBoxLayout(self.FigureWidget_rb) #ウィジェットにFigureLayout_rbを追加する
        # self.FigureLayout_rb.setContentsMargins(0,0,0,0) #四隅の余白0にする

        # self.Figure_rb = plt.figure() #self.Figure_rbという描画領域を作成する
        # self.FigureCanvas_rb = FigureCanvas(self.Figure_rb) #self.Figure_rbを表示するキャンバスを作成
        # self.FigureLayout_rb.addWidget(self.FigureCanvas_rb) #キャンバスをFigureLayout_rbに入れる

        # self.axis_rb = self.Figure_rb.add_subplot() #画像表示のために軸作る
        # self.Figure_rb.tight_layout() #Canvasと画像の間の余白を狭くする

        # self.image_rb = data_rb #ndarrayをセットする
        # self.axis_image_rb = sns.heatmap(self.image_rb, cmap="rainbow", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
        # self.FigureCanvas_rb.draw() #表示する

        #動画再生画面のウィジット(R-G成分値)
        key = "rg"    
        self.FigureWidget_rg = self.make_frame.frame_rg(self, self.folder_pass)
        # with open(folder_pass + str("1_rg") + ".dat", "rb") as f: #ファイルを開く
        #     data_rg = np.load(f, allow_pickle=True)

        # self.FigureWidget_rg = QWidget(self) #動画埋め込みのためのウィジェット
        # self.FigureWidget_rg.setFixedSize(weight*0.25, height*0.25) #サイズを固定
        
        # self.FigureLayout_rg = QVBoxLayout(self.FigureWidget_rg) #ウィジェットにFigureLayout_rgを追加する
        # self.FigureLayout_rg.setContentsMargins(0,0,0,0) #四隅の余白0にする

        # self.Figure_rg = plt.figure() #self.Figure_rgという描画領域を作成する
        # self.FigureCanvas_rg = FigureCanvas(self.Figure_rg) #self.Figure_rgを表示するキャンバスを作成
        # self.FigureLayout_rg.addWidget(self.FigureCanvas_rg) #キャンバスをFigureLayout_rgに入れる

        # self.axis_rg = self.Figure_rg.add_subplot() #画像表示のために軸作る
        # self.Figure_rg.tight_layout() #Canvasと画像の間の余白を狭くする

        # self.image_rg = data_rg
        # self.axis_image_rg = sns.heatmap(self.image_rg, cmap="gray", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
        # self.FigureCanvas_rg.draw() #表示する

        #動画再生画面のウィジット(G-B成分値)  
        self.FigureWidget_gb = self.make_frame.frame_gb(self, self.folder_pass)  
        # with open(folder_pass + str("1_gb") + ".dat", "rb") as f: #ファイルを開く
        #     data_gb = np.load(f, allow_pickle=True)

        # self.FigureWidget_gb = QWidget(self) #動画埋め込みのためのウィジェット
        # self.FigureWidget_gb.setFixedSize(weight*0.25, height*0.25) #サイズを固定
        
        # self.FigureLayout_gb = QVBoxLayout(self.FigureWidget_gb) #ウィジェットにFigureLayout_gbを追加する
        # self.FigureLayout_gb.setContentsMargins(0,0,0,0) #四隅の余白0にする

        # self.Figure_gb = plt.figure() #self.Figure_gbという描画領域を作成する
        # self.FigureCanvas_gb = FigureCanvas(self.Figure_gb) #self.Figure_gbを表示するキャンバスを作成
        # self.FigureLayout_gb.addWidget(self.FigureCanvas_gb) #キャンバスをFigureLayout_gbに入れる

#        self.axis_gb = self.Figure_gb.add_subplot() #画像表示のために軸作る
#        self.Figure_gb.tight_layout() #Canvasと画像の間の余白を狭くする

#        self.image_gb = data_gb
#        self.axis_image_gb = sns.heatmap(self.image_gb, cmap="RdBu", xticklabels=False, yticklabels=False, cbar_kws={"orientation": "horizontal"}, square=True, vmin=0,vmax=255)
#        self.FigureCanvas_gb.draw() #表示する

        self.color_bar = self.make_frame.make_colorbar(self)


    #----------------------------------
    #動画再生画面のレイアウト作成
    #----------------------------------
    def make_second_layout(self):
        
        self.rgb_layout = QHBoxLayout() #レイアウト上部に使う骨組みのレイアウト
        self.sub_layout = QHBoxLayout() #レイアウト下部に使う骨組みのレイアウト


        self.main_layout.addStretch() #余白
        self.main_layout.addWidget(self.second_title, alignment=Qt.AlignHCenter) #main_layoutにタイトルウィジェットを追加

        #上半分の骨組みのレイアウトの中身
        self.rgb_layout.addStretch() #余白
        self.rgb_layout.addWidget(self.rgb_name) #元画像っていう文字
        self.rgb_layout.addWidget(self.FigureWidget_rgb) #元画像の動画のウィジェット
        self.rgb_layout.addStretch() #余白
        self.rgb_layout.addWidget(self.play_button) #再生開始のボタン
        self.rgb_layout.addStretch() #余白

        self.main_layout.addStretch(0) #余白
        self.main_layout.addLayout(self.rgb_layout) #上半分のレイアウトをmain_layoutに追加する
        #self.main_layout.addStretch(0) #余白をなしにする

        #下半分の骨組みのレイアウトの中身
        self.sub_layout.addStretch() #余白
        self.sub_layout.addWidget(self.rb_name) #R-B成分っていう文字
        self.sub_layout.addWidget(self.FigureWidget_rb) #R-Bの動画のウィジェット

        self.sub_layout.addWidget(self.rg_name) #R-G成分っていう文字
        self.sub_layout.addWidget(self.FigureWidget_rg) #R-Gの動画のウィジェット

        self.sub_layout.addWidget(self.gb_name) #G-B成分っていう文字
        self.sub_layout.addWidget(self.FigureWidget_gb) #G-Bの動画のウィジェット
        self.sub_layout.addStretch() #余白

        self.main_layout.addStretch(0) #余白
        self.main_layout.addLayout(self.sub_layout) #下半分のレイアウトを追加する
        self.main_layout.addWidget(self.color_bar, alignment=Qt.AlignHCenter)
        self.main_layout.addStretch(0) #余白なしにする


    #----------------------------------
    #再生開始が押されたら実行される関数
    #----------------------------------
    def start_play(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.make_frame.update_figure(self.folder_pass))
        self.timer.start(1000)
        self.timer.singleShot(110000, self.timer_stop)

    def timer_stop(self):
        self.timer.stop()
        print("here")

    #-------------------------------------------
    #レイアウト内のウィジェットを全て削除する関数
    #-------------------------------------------
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = AppScreen()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")