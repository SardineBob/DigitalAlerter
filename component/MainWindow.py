import tkinter as tk
from component.ConfigUtil import ConfigUtil
from component.Map import Map
from component.WindowRelocate import WindowRelocate
from component.AlertTag import AlertTag
from component.CameraTag import CameraTag


class MainWindow():
    __configUtil = None
    __originWidth = 640
    __originHeight = 480
    __curWidth = __originWidth
    __curHeight = __originHeight
    __mainWindow = None
    __canvas = None
    __map = None
    __windowRelocate = None
    __alertTags = []
    __cameraTags = []

    # 測試用
    __window = None
    __window1 = None
    __window2 = None
    __window3 = None

    def __init__(self):
        # 準備主要視窗設定
        self.__mainWindow = tk.Tk()
        self.__mainWindow.title("Digital Alerter(ver.0.0.2)")
        self.__mainWindow.geometry("%dx%d" % (
            self.__originWidth, self.__originHeight))
        # 註冊視窗事件
        self.__mainWindow.bind('<Configure>', self.__windowResize)
        # 讀取保全器材位置設定檔
        self.__configUtil = ConfigUtil()
        # 產生繪圖物件
        self.__canvas = tk.Canvas(
            width=self.__curWidth, height=self.__curHeight, bg="black")
        self.__canvas.pack(fill='both', expand=True)
        # 產生地圖物件
        self.__map = Map(self.__canvas)
        self.__map.Draw(self.__originWidth, self.__originHeight)
        # 產生視窗重新定位的物件
        self.__windowRelocate = WindowRelocate({
            'oriWindowWidth': self.__originWidth,
            'oriWindowHeight': self.__originHeight,
            'oriMapWidth': self.__map.mapOriginWidth,
            'oriMapHeight': self.__map.mapOriginHeight
        })
        # 產生保全器材(警報點)標籤位置
        for item in self.__configUtil.AlertPoints:
            self.__alertTags.append(
                AlertTag(self.__canvas, self.__windowRelocate, item))
        # 產生攝影機標籤位置
        for item in self.__configUtil.cameraPoints:
            self.__cameraTags.append(
                CameraTag(self.__canvas, self.__windowRelocate, item))

        # 給兩個按鈕來測試閃爍
        def click1():
            self.__alertTags[2].TriggerAlert()

        def click2():
            self.__alertTags[2].TriggerStop()
            for item in self.__cameraTags:
                item.RtspStop()

        # def click3():
            # self.__window = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 100, 100)
            # self.__window1 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 100, 270)
            # self.__window2 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 350, 100)
            # self.__window3 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 350, 270)
            # self.__window.Start()
            # self.__window1.Start()
            # self.__window2.Start()
            # self.__window3.Start()

        button1 = tk.Button(text='啟動', command=click1)
        button1.place(x=10, y=10)
        button2 = tk.Button(text='停止', command=click2)
        button2.place(x=50, y=10)
        #button3 = tk.Button(text='播放', command=click3)
        #button3.place(x=90, y=10)

        # 開啟視窗
        self.__mainWindow.mainloop()

    def __windowResize(self, event):
        # 判斷事件是主要視窗所觸發
        if str(event.widget) == '.':
            # 判斷變動主要視窗寬高的操作
            if self.__curWidth != event.width or self.__curHeight != event.height:
                # 觸發執行Map Resize動作
                self.__map.Draw(event.width, event.height)
                # 設定目前Window Resize後的寬高大小
                self.__windowRelocate.SetCurrentSize(event.width, event.height)
                # 重新定位保全器材標籤位置
                for item in self.__alertTags:
                    item.Relocate()
                for item in self.__cameraTags:
                    item.Relocate()
                # 更新目前視窗寬高
                self.__curWidth = event.width
                self.__curHeight = event.height
