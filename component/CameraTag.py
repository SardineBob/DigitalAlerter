import tkinter as tk
from component.Tag import Tag
from component.RtspWindow import RtspWindow
from PIL import Image, ImageTk
from cv2 import cv2
import time
import threading


class CameraTag(Tag):

    __picPath = './resource/IconCamera.png'
    __rtspUrl = ''
    __rtspWindow = None
    __rtspOpen = False

    def __init__(self, canvas, configItem):
        # 取出需用到的設定值
        pointid = configItem["number"]
        x = configItem["X"]
        y = configItem["Y"]
        self.__rtspUrl = configItem["rtspUrl"]
        # open攝影機標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "cameraIcon") is False:
            canvas.cameraIcon = []
        canvas.cameraIcon.append(picPhoto)
        # 傳入父類別，建立攝影機標籤物件
        super().__init__(canvas, pointid, x, y, picPhoto, 'camera')
        # 綁定Click事件到全部擁有camera這個tags的物件
        canvas.tag_bind(self.tagid, '<Button-1>', self.__CameraClickEvent)

    # 點擊攝影機Tag的事件，會開啟該攝影機的RTSP影像串流
    def __CameraClickEvent(self, event):
        # 判斷是否需建立承載RTSP影像串流的容器物件
        if self.__rtspWindow is None:
            self.__rtspWindow = RtspWindow({'url': self.__rtspUrl})
        # 點擊第一下開啟影像，第二下關閉影像
        if self.__rtspOpen is False:
            self.__rtspOpen = True
            self.__rtspWindow.Start()
        else:
            self.__rtspOpen = False
            self.__rtspWindow.Stop()
            self.__rtspWindow = None

        # 兩個問題
        # 2.視窗放大縮小 重新定位的問題
