import tkinter as tk
from component.Abnormal.QueryBar import QueryBar
from component.Abnormal.AbnormalTable import AbnormalTable
from component.Abnormal.VideoList import VideoList
from component.RtspBox import RtspBox
from component.RtspBoxLayout import RtspBoxLayout


class RtspWindow():

    __window = None
    __width = 640  # 目前視窗寬度
    __height = 480  # 目前視窗高度
    __padx = 5  # 每格影像間，X軸間格pixel
    __pady = 5  # 每格影像間，Y軸間格pixel
    __rtspBox = []  # 目前開啟中RTSP影像物件
    __cameraTags = []  # 目前存在的所有Camera Point資料

    # 開啟RTSP影像串流視窗
    def __OpenRtspWindow(self):
        # 開始建立一個子視窗
        self.__window = tk.Toplevel()
        self.__window.geometry(
            "{}x{}+50+50".format(self.__width, self.__height))
        # 註冊視窗關閉事件，使用者點擊視窗的X，會觸發
        self.__window.protocol("WM_DELETE_WINDOW", self.__WindowClose)
        # 設定Grid版面配置比例(最外層主要容器)
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=1)
        self.__window.grid_columnconfigure(2, weight=1)
        self.__window.grid_columnconfigure(3, weight=1)
        self.__window.grid_rowconfigure(0, weight=1)
        self.__window.grid_rowconfigure(1, weight=1)
        # 註冊視窗Resize觸發的事件(同時修正RTSP影像大小)
        self.__window.bind("<Configure>", self.__WindowResize)

    # 開啟指定的攝影機RTSP影像串流
    def OpenRtspBox(self, cameraTagID):
        # 若開啟第一格RTSP影像，則觸發開啟視窗
        if len(self.__rtspBox) <= 0:
            self.__OpenRtspWindow()
        # 開啟RTSP影像串流
        self.__rtspBox.append(RtspBox({
            'root': self.__window,
            'cameraTagID': cameraTagID,
            'closeMethod': self.CloseRtspBox
        }))
        # 重新配置版面
        self.__ResetPanel()

    # 關閉指定攝影機RTSP影像串流
    def CloseRtspBox(self, cameraTagID):
        # 執行關閉程序
        self.__CloseRtspBox(cameraTagID)
        # 判斷若關閉RTSP Box一格不剩，則關閉整個視窗
        if len(self.__rtspBox) <= 0:
            self.__WindowClose()

    # 關閉指定RTSP影像串流，包含Tag狀態旗標重置、RTSP串流執行序銷毀以及移除RTSP Box陣列
    def __CloseRtspBox(self, cameraTagID):
        # 先找到這個cameraTagID的item，停止RTSP串流執行序後移除
        for item in self.__rtspBox:
            if item.tagID is cameraTagID:
                item.Stop()
                self.__rtspBox.remove(item)
                # 重新配置版面
                self.__ResetPanel()
        # 找到CameraTag本體，執行將開啟RTSP的旗標重製動作
        for item in self.__cameraTags:
            if item.pointid is cameraTagID:
                item.setRtspIsClose()

    # 根據開啟或關閉的Rtsp Box數量，重新配置版面
    def __ResetPanel(self):
        for item in self.__rtspBox:
            idx = self.__rtspBox.index(item)
            (seat, size) = self.__getBoxLayoutGrid(idx)
            self.__rtspBox[idx].setBoxGrid(seat, size)

    # 視窗關閉，用於外部呼叫
    def __WindowClose(self):
        # 關閉視窗時，清除所有開啟中的RtspBox
        rtspBoxs = self.__rtspBox.copy()
        for item in rtspBoxs:
            self.__CloseRtspBox(item.tagID)
        # 銷毀視窗物件
        if self.__window is not None:
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

    # 提供外部設定所有存在的CameraTag資料
    def SetCameraTag(self, cameraTags):
        self.__cameraTags = cameraTags
