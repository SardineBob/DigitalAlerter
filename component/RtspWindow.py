import tkinter as tk
from component.Abnormal.QueryBar import QueryBar
from component.Abnormal.AbnormalTable import AbnormalTable
from component.Abnormal.VideoList import VideoList
from component.RtspBox import RtspBox
from component.RtspBoxLayout import RtspBoxLayout


class RtspWindow():

    __window = None
    __closeMethod = None  # 呼叫端關閉本視窗的方法，通常包含呼叫本class的close event，以及呼叫端管理class關閉的實作方法
    __width = 640  # 目前視窗寬度
    __height = 480  # 目前視窗高度
    __padx = 5  # 每格影像間，X軸間格pixel
    __pady = 5  # 每格影像間，Y軸間格pixel
    __rtspBox = []  # 目前開啟中RTSP影像物件
    #test = None

    def __init__(self, para):
        # 取出需使用的設定值
        self.__closeMethod = para["closeMethod"]
        # 開始建立一個子視窗
        self.__window = tk.Toplevel()
        self.__window.geometry(
            "{}x{}+50+50".format(self.__width, self.__height))
        # 註冊視窗關閉事件，使用者點擊視窗的X，會觸發
        self.__window.protocol("WM_DELETE_WINDOW", self.__closeMethod)
        # 產生版面
        self.__CreatePanel()
        # 註冊視窗Resize觸發的事件(同時修正RTSP影像大小)
        self.__window.bind("<Configure>", self.__WindowResize)

    # 產生版面(固定8格320*240的影像畫面視窗)
    def __CreatePanel(self):
        # 設定Grid版面配置比例(最外層主要容器)
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=1)
        self.__window.grid_columnconfigure(2, weight=1)
        self.__window.grid_columnconfigure(3, weight=1)
        self.__window.grid_rowconfigure(0, weight=1)
        self.__window.grid_rowconfigure(1, weight=1)

        self.__rtspBox.append(RtspBox({
            'root': self.__window,
            'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
            'closeMethod': self.WindowClose,
            'cameraTagID': 1,
            'recordFileName': 'test.avi'}))

        # self.__rtspBox.append(RtspBox({
        #     'root': self.__window,
        #     'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #     'closeMethod': self.WindowClose,
        #     'cameraTagID': 2,
        #     'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 3,
        #    'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 4,
        #    'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 5,
        #    'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 6,
        #    'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 7,
        #    'recordFileName': 'test.avi'}))
        # self.__rtspBox.append(RtspBox({
        #    'root': self.__window,
        #    'url': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov',
        #    'closeMethod': self.WindowClose,
        #    'cameraTagID': 8,
        #    'recordFileName': 'test.avi'}))
        for item in self.__rtspBox:
            idx = self.__rtspBox.index(item)
            (seat, size) = self.__getBoxLayoutGrid(idx)
            self.__rtspBox[idx].setBoxGrid(seat, size)


    # 視窗關閉，用於外部呼叫
    def WindowClose(self):
        self.__window.destroy()
        self.__window = None

    # 視窗縮放大小時，觸發事件處理包含RTSP影像大小異動等動作
    def __WindowResize(self, event):
        # 判斷事件是主要視窗所觸發
        if str(event.widget) == '.!toplevel':
            # 判斷變動主要視窗寬高的操作
            if self.__width != event.width or self.__height != event.height:
                # 更新目前視窗寬高
                self.__width = event.width
                self.__height = event.height
                # 更新所有開啟的影像大小
                for item in self.__rtspBox:
                    idx = self.__rtspBox.index(item)
                    item.setBoxSize(self.__getBoxSize(idx))

    # 根據目前開啟的影像數量，計算該格的Grid版面配置的參數以及計算影像長寬(最多8格)
    def __getBoxLayoutGrid(self, whichGrid):
        # 根據目前已開啟的影像數量，來做版面上的排列
        openBoxCnt = len(self.__rtspBox)
        # 根據目前開啟的影像數量，指定格數，取出對應的配置參數
        seat = RtspBoxLayout[openBoxCnt-1][whichGrid]
        # 加入一些固定的參數
        seat['sticky'] = 'EWNS'
        seat['padx'] = self.__padx
        seat['pady'] = self.__pady
        # 計算這格影像大小
        boxSize = self.__getBoxSize(whichGrid)
        # 回傳配置參數
        return (seat, boxSize)

    # 根據目前視窗大小，計算每個影像大小(根據開啟影像數量與格子位置為了版面配置有不同大小)
    def __getBoxSize(self, whichGrid):
        # 取得每格影像的設定參數
        seat = RtspBoxLayout[len(self.__rtspBox)-1][whichGrid]
        # 計算影像大小
        boxWidth = int((self.__width / 4) * seat['columnspan'] - self.__padx)
        boxHeight = int((self.__height / 2) * seat['rowspan'] - self.__pady)
        return (boxWidth, boxHeight)
