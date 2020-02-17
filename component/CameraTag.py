import tkinter as tk
from component.Tag import Tag
from PIL import Image, ImageTk
from cv2 import cv2
import time
import threading


class CameraTag(Tag):

    __picPath = './resource/IconCamera.png'
    __rtspUrl = None
    __rtspTask = None
    __rtspActive = False
    __rtspWindow = None
    __rtspX = 100
    __rtspY = 100
    __rtspWidth = 10
    __rtspHeight = 5

    def __init__(self, canvas, configItem):
        # 取出需用到的設定值
        pointid = configItem["number"]
        x = configItem["X"]
        y = configItem["Y"]
        rtspUrl = configItem["rtspUrl"]
        # open攝影機標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "cameraIcon") is False:
            canvas.cameraIcon = []
        canvas.cameraIcon.append(picPhoto)
        # 傳入父類別，建立攝影機標籤物件
        super().__init__(canvas, pointid, x, y, picPhoto, 'camera')
        # 初始化RTSP串流來源位址
        self.__rtspUrl = rtspUrl
        # 綁定Click事件到全部擁有camera這個tags的物件
        canvas.tag_bind(self.tagid, '<Button-1>', self.__CameraClickEvent)

    # 點擊攝影機Tag的事件，會開啟該攝影機的RTSP影像串流
    def __CameraClickEvent(self, event):
        # 判斷是否需建立承載RTSP影像串流的容器物件
        if self.__rtspWindow is None:
            self.__rtspWindow = tk.Label(
                bg="black", width=self.__rtspWidth, height=self.__rtspHeight)
            self.__rtspWindow.place(
                x=self.__rtspX, y=self.__rtspY, anchor='nw')
        # 點擊第一下開啟影像，第二下關閉影像
        if self.__rtspActive is False:
            self.__RtspStart()
        else:
            self.__RtspStop()

    # 開始播放RTSP影像串流(建立一個執行序來跑，以免畫面Lock)
    def __RtspStart(self):
        if self.__rtspTask is None:
            self.__rtspTask = threading.Thread(target=self.__RtspPlay)
            self.__rtspTask.setDaemon(True)
            self.__rtspActive = True
            self.__rtspTask.start()

    # 停止播放RTSP串流，並銷毀執行序(需等待python程序GC)
    def __RtspStop(self):
        self.__rtspActive = False
        self.__rtspTask = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__rtspWindow.destroy()  # 銷毀
        self.__rtspWindow = None

    # 執行RTSP影像串流播放的動作
    def __RtspPlay(self):
        video = cv2.VideoCapture(self.__rtspUrl)
        (status, frame) = video.read()
        while self.__rtspActive and status:
            (status, frame) = video.read()
            imgArray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(imgArray)
            photo = ImageTk.PhotoImage(image=image)
            if hasattr(self.__rtspWindow, 'configure') is True:
                self.__rtspWindow.configure(
                    image=photo, width=photo.width(), height=photo.height())
                self.__rtspWindow.rtspImage = photo
        video.release()

        # 兩個問題
        # 2.視窗放大縮小 重新定位的問題
