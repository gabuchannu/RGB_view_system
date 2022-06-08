from re import S, sub
import dlib
import cv2
from PIL import Image
#import imutile import face_utils
import numpy as np
#import detetime
import pandas as pd
import csv
import copy
import statistics

class movie_task:
    def __init__(self):
        self.movie_pass = "" #動画のパス
        self.rgb_list = [] #RGB成分値を格納するリスト
        self.rb_list = [] #R-BとR-GとG-B成分の値を格納するリスト
        self.rg_list = []
        self.gb_list = []
        self.count = 0 #フレーム数がいくつあるかカウントに使うカウンター


    #---------------
    #動画を読み込む
    #---------------
    def openmovie(self, movie):

        time_counter = 1 #何フレーム進めたかを見るためのカウンター

        self.movie_pass = movie #引数として渡された動画のパス
        cap = cv2.VideoCapture(self.movie_pass) #動画を読み込む
        
        while True:
            ret, img = cap.read() #動画を1フレームごとに見ていく
            if ret == False: #動画要素がなくなってたら
                break #ループから抜ける

            if time_counter == 30: #1秒経過してたら
                time_counter = 1 #カウントをリセット
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.pixel_info(img_rgb) #pixel_info関数を実行
            else: #まだ1秒経過してなかったら
                time_counter = time_counter + 1 #カウントを増やす


    #---------------
    #静止画を読み込む
    #---------------
    def openfile(self, photo):

        self.photo_pass = photo #引数として渡された動画のパス
#        img = cv2.imread(self.photo_pass) #画像の読み込み
        img = np.array(Image.open(self.photo_pass))
            
        self.pixel_info(img) #frame_taskを実行

        return self.count


    #-------------------------------
    #各ピクセルに対して処理をする関数
    #-------------------------------
    def pixel_info(self, img):

        self.count += 1 #何フレーム目かをカウントする
        height_img, weight_img, channel_img = img.shape #画像サイズの取得
        #img2 = copy.copy(img) #元が書き換えられないコピーを創る

        rb_line = []
        rg_line = []
        gb_line = []

        for i in range(0, height_img): #全ピクセルに対して処理
            for j in range(0, weight_img):
                rb_value = int(img[i, j, :][0]) - int(img[i, j, :][2])
                rg_value = int(img[i, j, :][0]) - int(img[i, j, :][1])
                gb_value = int(img[i, j, :][1]) - int(img[i, j, :][2])
                if rb_value <= 0: #0以下だったら
                    rb_value = 0
                if rg_value <= 0:
                    rg_value = 0
                if gb_value <= 0:
                    gb_value = 0
                rb_line.append(rb_value)
                rg_line.append(rg_value)
                gb_line.append(gb_value)

                if j == (weight_img - 1): #1列分やりきったら結合                   
                    self.rb_list.append(rb_line)
                    self.rg_list.append(rg_line)
                    self.gb_list.append(gb_line)
                    rb_line = [] #中身空にする
                    rg_line = [] #中身空にする
                    gb_line = [] #中身空にする

                # #self.sub_value.append([rb_value, rg_value, gb_value]) #差分成分のピクセル情報
                # img2[i, j, :][0] = rb_value #差分成分のピクセル情報に書き換える
                # img2[i, j, :][1] = rg_value
                # img2[i, j, :][2] = gb_value
        
        self.rgb_list = img #元画像の各ピクセル情報

        self.array_to_text() #ピクセル情報をtxtファイルで保存する関数


    #-------------------------------------
    #ピクセル情報の配列をテキストに保存する
    #-------------------------------------
    def array_to_text(self):

#        number = self.photo_pass.rfind(".") #静止画のパス名を取得
        number = self.movie_pass.rfind(".") #動画のパス名を取得
#        folder_pass = self.photo_pass[:number] #.aviより前を持ってくる
        folder_pass = self.movie_pass[:number] #.aviより前を持ってくる

        save_folder_pass_rb = folder_pass + str(self.count) + "_rb.dat" #差分のピクセル情報を保存するtxtファイルのパス
        save_folder_pass_rg = folder_pass + str(self.count) + "_rg.dat"
        save_folder_pass_gb = folder_pass + str(self.count) + "_gb.dat"       
        save_folder_pass_rgb = folder_pass + str(self.count) + "_rgb.dat" #元画像のピクセル情報を保存するtxtファイルのパス
        
        self.rgb_list.dump(save_folder_pass_rgb)
        self.rb_list = np.array(self.rb_list)
        self.rb_list.dump(save_folder_pass_rb)
        self.rg_list = np.array(self.rg_list)
        self.rg_list.dump(save_folder_pass_rg)
        self.gb_list = np.array(self.gb_list)
        self.gb_list.dump(save_folder_pass_gb)

        self.rgb_list = []
        self.rb_list = []
        self.rg_list = []
        self.gb_list = []