import tkinter as tk
from PIL import Image, ImageTk
from cv2 import cv2
import threading


class RtspLinkLine():

    __canvas = None
    __lineID = None

    def __init__(self, canvas):
        # 取出需用到的設定值
        self.__canvas = canvas

    # 繪製連接線
    def DrawLinkLine(self, tagX, tagY, rtspX, rtspY):
        self.__lineID = self.__canvas.create_line(
            tagX, tagY, rtspX, rtspY, fill="red", width=3)

    # 刪除連接線
    def DropLinkLine(self):
        self.__canvas.delete(self.__lineID)
        self.__canvas = None
        self.__lineID = None

    # 移動連接線
    def MoveLinkLine(self, tagX, tagY, rtspX, rtspY):
        if self.__lineID is not None:
            self.Relocate(tagX, tagY, rtspX, rtspY)

    # 因應視窗縮放，根據縮放比例重新定位連接線位置
    def Relocate(self, tagX, tagY, rtspX, rtspY):
        if self.__lineID is None:
            return
        # 重新定位連接線的位置
        self.__canvas.coords(self.__lineID, tagX, tagY, rtspX, rtspY)
