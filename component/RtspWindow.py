import tkinter as tk
from PIL import Image, ImageTk
from cv2 import cv2
import threading
from library.LocationFunc import Relocate


class RtspWindow():

    __window = None
    __url = None
    __x = 0
    __y = 0
    __width = 10
    __height = 5
    __task = None
    __active = False
    __relocatePara = None  # 視窗resize時，所傳入的參數，記錄下來，移動RTSP Window時，需要將座標根據縮放比例重新計算

    def __init__(self, para):
        # 取出需用到的設定值
        self.__url = para["url"]
        self.__x = para["x"]
        self.__y = para["y"]
        # 建立承載RTSP影像串流的容器物件
        self.__window = tk.Label(
            bg="black", width=self.__width, height=self.__height)
        # 放置在畫面上
        self.__window.place(x=self.__x, y=self.__y, anchor='nw')
        # 註冊RTSP視窗拖移事件
        self.__window.bind('<B1-Motion>', self.__DragEvent)

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

    # 因應視窗縮放，根據縮放比例重新定位視窗位置
    def Relocate(self, para):
        if self.__window is None:
            return
        # 放置目前的XY座標
        para["oriX"] = self.__x
        para["oriY"] = self.__y
        # 取得因為視窗縮放產生的新座標
        result = Relocate(para)
        newX = result["newX"]
        newY = result["newY"]
        # 重新定位RTSP Window的位置
        self.__window.place(x=newX, y=newY, anchor='nw')
        # 紀錄這次的參數
        self.__relocatePara = para

    def __DragEvent(self, event):
        print(event.x, event.y)
        self.__x = event.x
        self.__y = 100
        # 若曾經縮放過，則這個新座標要根據比例縮放
        if self.__relocatePara is None:
            self.__window.place(x=self.__x, y=self.__y, anchor='nw')
        else:
            self.Relocate(self.__relocatePara)
