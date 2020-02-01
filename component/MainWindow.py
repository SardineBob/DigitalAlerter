import tkinter as tk
from component.Map import Map


class MainWindow():
    __mainWindowWidth = 640
    __mainWindowHeight = 480
    __mainWindow = None
    __map = None

    def __init__(self):
        # 準備主要視窗設定
        self.__mainWindow = tk.Tk()
        self.__mainWindow.title("Digital Alerter(ver.0.0.1)")
        self.__mainWindow.geometry("%dx%d" % (
            self.__mainWindowWidth, self.__mainWindowHeight))
        # 註冊視窗事件
        self.__mainWindow.bind('<Configure>', self.__windowResize)
        # 產生地圖物件
        self.__map = Map()
        self.__map.Create(self.__mainWindowWidth, self.__mainWindowHeight)
        # 開啟視窗
        self.__mainWindow.mainloop()

    def __windowResize(self, event):
        # 判斷事件是主要視窗所觸發
        if str(event.widget) == '.':
            # 判斷變動主要視窗寬高的操作
            if self.__mainWindowWidth != event.width or self.__mainWindowHeight != event.height:
                # 觸發執行Map Resize動作
                self.__map.Create(event.width, event.height)
                # 更新目前視窗寬高
                self.__mainWindowWidth = event.width
                self.__mainWindowHeight = event.height
