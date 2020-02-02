import tkinter as tk
from component.Map import Map
from component.Tag import Tag


class MainWindow():
    __originWidth = 640
    __originHeight = 480
    __curWidth = __originWidth
    __curHeight = __originHeight
    __mainWindow = None
    __map = None
    __tag = None

    def __init__(self):
        # 準備主要視窗設定
        self.__mainWindow = tk.Tk()
        self.__mainWindow.title("Digital Alerter(ver.0.0.1)")
        self.__mainWindow.geometry("%dx%d" % (
            self.__originWidth, self.__originHeight))
        # 註冊視窗事件
        self.__mainWindow.bind('<Configure>', self.__windowResize)
        # 產生地圖物件
        self.__map = Map()
        self.__map.Create(self.__originWidth, self.__originHeight)
        # 產生保全器材標籤位置
        self.__tag = Tag()
        # 開啟視窗
        self.__mainWindow.mainloop()

    def __windowResize(self, event):
        # 判斷事件是主要視窗所觸發
        if str(event.widget) == '.':
            # 判斷變動主要視窗寬高的操作
            if self.__curWidth != event.width or self.__curHeight != event.height:
                # 觸發執行Map Resize動作
                self.__map.Create(event.width, event.height)
                # 重新定位保全器材標籤位置
                self.__tag.Relocate({
                    'curWindowWidth': event.width,
                    'curWindowHeight': event.height,
                    'oriWindowWidth': self.__originWidth,
                    'oriWindowHeight': self.__originHeight,
                    'oriMapWidth': self.__map.mapOriginWidth,
                    'oriMapHeight': self.__map.mapOriginHeight
                })
                # 更新目前視窗寬高
                self.__curWidth = event.width
                self.__curHeight = event.height
