import tkinter as tk
from PIL import Image, ImageTk
from cv2 import cv2
import threading
from utilset.ConfigUtil import ConfigUtil


class RtspBox():

    __root = None
    __box = None
    __url = None
    __width = 10
    __height = 5
    __task = None
    __active = False
    __closeMethod = None  # 當關閉這個RtspBox的時候，外部也有在Close時需要執行的動作
    tagID = None  # Camera Tag ID Number
    __boxSize = (320, 240)  # 定義一個RtspBox尺寸，通常由父容器計算視窗寬高與格數後給予
    __recordSize = (320, 240)  # 定義一個錄影片段尺寸，目前採計算原尺寸的1/4

    def __init__(self, para):
        # 取出需用到的設定值
        self.__root = para["root"]
        self.tagID = para["cameraTagID"]
        self.__closeMethod = para["closeMethod"]
        self.__url = ConfigUtil().getCameraPoint(self.tagID)['rtspUrl']
        # 建立承載RTSP影像串流的容器物件
        self.__box = tk.Label(
            self.__root, bg="black", width=self.__width, height=self.__height)
        # 註冊RTSP視窗雙擊事件(關閉視窗)
        self.__box.bind('<Double-Button-1>', self.__DoubleClickEvent)
        # 開始撥放RTSP影像串流
        self.__Start()

    # 開始播放RTSP影像串流(建立一個執行序來跑，以免畫面Lock)
    def __Start(self):
        if self.__task is None:
            self.__task = threading.Thread(target=self.__Play)
            self.__task.setDaemon(True)
            self.__active = True
            self.__task.start()

    # 停止播放RTSP串流，並銷毀執行序(需等待python程序GC)
    def Stop(self):
        if self.__box is not None:
            self.__box.destroy()  # 銷毀
        self.__active = False
        self.__task = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__box = None

    # 執行RTSP影像串流播放的動作
    def __Play(self):
        # 連接RTSP串流
        video = cv2.VideoCapture(self.__url)
        # 讀取RTSP串流，並撥放與錄影
        (status, frame) = video.read()
        while self.__active and status:
            (status, frame) = video.read()
            # resize frame
            frame = cv2.resize(frame, self.__boxSize)
            # 呈現影像畫面
            imgArray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(imgArray)
            photo = ImageTk.PhotoImage(image=image)
            if hasattr(self.__box, 'configure') is True:
                self.__box.configure(
                    image=photo, width=photo.width(), height=photo.height())
                self.__box.rtspImage = photo
        video.release()

    # RTSP視窗雙擊事件
    def __DoubleClickEvent(self, event):
        self.Stop()
        # 執行外部傳進來的Close事件
        self.__closeMethod(self.tagID)

    # 提供父容器設定這格RTSP影像尺寸
    def setBoxSize(self, size):
        self.__boxSize = size

    # 提供父容器設定這格RTSP影像在Grid的layout分布是哪一個位置，以及這格RTSP影像大小
    def setBoxGrid(self, seat, size):
        self.__box.grid(seat)
        self.__boxSize = size
