import tkinter as tk
from component.Tag import Tag
from PIL import Image, ImageTk
from cv2 import cv2
import time
import threading


class RtspWindow():

    __window = None
    __url = None
    __x = 200
    __y = 200
    __width = 10
    __height = 5
    __task = None
    __active = False

    def __init__(self, parameter):
        # 取出需用到的設定值
        self.__url = parameter["url"]
        # 建立承載RTSP影像串流的容器物件
        self.__window = tk.Label(
            bg="black", width=self.__width, height=self.__height)
        # 放置在畫面上
        self.__window.place(x=self.__x, y=self.__y, anchor='nw')

    # 開始播放RTSP影像串流(建立一個執行序來跑，以免畫面Lock)
    def Start(self):
        if self.__task is None:
            self.__task = threading.Thread(target=self.__Play)
            self.__task.setDaemon(True)
            self.__active = True
            self.__task.start()

    # 停止播放RTSP串流，並銷毀執行序(需等待python程序GC)
    def Stop(self):
        self.__active = False
        self.__task = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__window.destroy()  # 銷毀
        self.__window = None

    # 執行RTSP影像串流播放的動作
    def __Play(self):
        video = cv2.VideoCapture(self.__url)
        (status, frame) = video.read()
        while self.__active and status:
            (status, frame) = video.read()
            imgArray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(imgArray)
            photo = ImageTk.PhotoImage(image=image)
            if hasattr(self.__window, 'configure') is True:
                self.__window.configure(
                    image=photo, width=photo.width(), height=photo.height())
                self.__window.rtspImage = photo
        video.release()
