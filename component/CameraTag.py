import tkinter as tk
from component.Tag import Tag
from component.RtspBox import RtspBox
from PIL import Image, ImageTk
from cv2 import cv2
import time
import threading


class CameraTag(Tag):

    __picPath = './resource/IconCamera.png'
    __rtspWindow = None
    __rtspIsOpen = False

    def __init__(self, canvas, relocate, configItem):
        # 取出需用到的設定值
        pointid = configItem["number"]
        name = configItem["name"]
        x = configItem["X"]
        y = configItem["Y"]
        # open攝影機標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "cameraIcon") is False:
            canvas.cameraIcon = []
        canvas.cameraIcon.append(picPhoto)
        # 傳入父類別，建立攝影機標籤物件
        super().__init__(canvas, relocate, pointid, name, x, y, picPhoto, 'camera')
        # 綁定Click事件到全部擁有camera這個tags的物件
        canvas.tag_bind(self.tagid, '<Button-1>', self.__CameraClickEvent)
        # 攝影機點暫時不用狀態環，先行移除
        canvas.delete(self.ringid)

    # 點擊攝影機Tag的事件，會開啟該攝影機的RTSP影像串流
    def __CameraClickEvent(self, event):
        if self.__rtspIsOpen is False:
            self.__openRtspBox()
        else:
            self.__closeRtspBox()

    # 開啟RtspBox動作
    def __openRtspBox(self):
        self.__rtspWindow.OpenRtspBox(self.pointid)
        self.__rtspIsOpen = True
        # 變化CameraTag背景顏色，說明攝影機畫面啟動中(目前採用藍色)
        self.canvas.itemconfig(self.bgid, fill='#0000ff')

    # 關閉RtspBox動作
    def __closeRtspBox(self):
        self.__rtspWindow.CloseRtspBox(self.pointid)
        self.setRtspIsClose()

    # 提供外部呼叫，通知tag已關閉RTSP Box
    def setRtspIsClose(self):
        self.__rtspIsOpen = False
        # 變化CameraTag背景顏色，說明攝影機畫面未啟動(目前採用綠色)
        self.canvas.itemconfig(self.bgid, fill='#00ff00')

    # 連結RTSP Window視窗開啟與關閉事件，實作點擊這個camera tag，根據狀態開啟或關閉
    def linkRtspWindow(self, rtspWindow):
        self.__rtspWindow = rtspWindow
