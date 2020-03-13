import tkinter as tk
from PIL import Image, ImageTk
from cv2 import cv2
import threading
from library.LocationFunc import Relocate


class RtspLinkLine():

    __canvas = None
    __lineID = None
    __tagX = None
    __tagY = None

    def __init__(self, canvas):
        # 取出需用到的設定值
        self.__canvas = canvas

    # 繪製連接線
    def DrawLinkLine(self, tagX, tagY, rtspX, rtspY):
        self.__tagX = tagX
        self.__tagY = tagY
        self.__lineID = self.__canvas.create_line(
            tagX, tagY, rtspX, rtspY, fill="red", width=3)

    # 刪除連接線
    def DropLinkLine(self):
        self.__canvas.delete(self.__lineID)
        self.__canvas = None
        self.__lineID = None

    # 移動連接線
    def MoveLinkLine(self, rtspX, rtspY):
        if self.__lineID is not None:
            self.__canvas.coords(
                self.__lineID, self.__tagX, self.__tagY, rtspX, rtspY)