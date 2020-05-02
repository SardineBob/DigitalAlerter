import tkinter as tk
from PIL import Image, ImageTk
from cv2 import cv2
import threading
import time
from component.RtspLinkLine import RtspLinkLine


class RtspWindow():

    __window = None
    __url = None
    __coordX = 0  # 視窗在frame容器中的座標
    __coordY = 0
    __width = 10
    __height = 5
    __task = None
    __active = False
    # __relocatePara = None  # 視窗resize時，所傳入的參數，記錄下來，移動RTSP Window時，需要將座標根據縮放比例重新計算
    __preMoveCoordX = 0  # 紀錄RTSP視窗拖移時，前一次的XY座標(計算拖移量用)
    __preMoveCoordY = 0
    __closeMethod = None  # RTSP視窗關閉的方法，包含tag的開關狀態控制異動
    __canvas = None  # 繪製連接線的畫布物件
    __relocate = None  # 視窗異動而座標重新定位的物件
    __tagID = None  # Camera Tag ID Number
    __tagX = None  # tag的座標位置，繪製連接線使用
    __tagY = None
    __linkLine = None  # Tag與RTSP視窗的連接線
    __recordFileName = None  # 從外界傳入的錄影檔名，該參數None時，系統自動預設

    def __init__(self, para):
        # 取出需用到的設定值
        self.__url = para["url"]
        self.__coordX = para["x"]
        self.__coordY = para["y"]
        self.__closeMethod = para["closeMethod"]
        self.__canvas = para["canvas"]
        self.__relocate = para["relocate"]
        self.__tagID = para["cameraTagID"]
        self.__tagX = para["cameraTagX"]
        self.__tagY = para["cameraTagY"]
        self.__recordFileName = para["recordFileName"]
        # 建立承載RTSP影像串流的容器物件
        self.__window = tk.Label(
            bg="black", width=self.__width, height=self.__height)
        # 放置在畫面上
        self.__window.place(
            x=self.__coordX, y=self.__coordY, anchor='nw')
        # 註冊RTSP視窗點擊事件
        self.__window.bind('<Button-1>', self.__ClickEvent)
        # 註冊RTSP視窗拖移事件
        self.__window.bind('<B1-Motion>', self.__DragEvent)
        # 註冊RTSP視窗雙擊事件(關閉視窗)
        self.__window.bind('<Double-Button-1>', self.__DoubleClickEvent)
        # 產生一條連接線物件
        self.__linkLine = RtspLinkLine(self.__canvas)
        self.__linkLine.DrawLinkLine(
            self.__tagX, self.__tagY, self.__coordX, self.__coordY)

    # 開始播放RTSP影像串流(建立一個執行序來跑，以免畫面Lock)
    def Start(self):
        if self.__task is None:
            self.__task = threading.Thread(target=self.__Play)
            self.__task.setDaemon(True)
            self.__active = True
            self.__task.start()

    # 停止播放RTSP串流，並銷毀執行序(需等待python程序GC)
    def Stop(self):
        self.__active = False
        self.__task = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__window.destroy()  # 銷毀
        self.__window = None
        self.__linkLine.DropLinkLine()  # 移除連接線
        self.__linkLine = None

    # 執行RTSP影像串流播放的動作
    def __Play(self):
        # 連接RTSP串流
        video = cv2.VideoCapture(self.__url)
        # resize RTSP串流影像
        video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        # 準備錄影路徑與檔名
        filepath = "CameraRecord"
        filename = self.__recordFileName
        if self.__recordFileName is None:
            nowTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = "Camera" + str(self.__tagID) + "-" + nowTime + ".avi"
        # 準備錄影的相關參數
        recordForucc = cv2.VideoWriter_fourcc(*self.getSourceFourcc(video))
        recordFPS = int(video.get(cv2.CAP_PROP_FPS))
        recordWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        recordHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 建立錄影實體物件
        record = cv2.VideoWriter(
            filepath + "/" + filename, recordForucc, recordFPS, (recordWidth, recordHeight))
        # 讀取RTSP串流，並撥放與錄影
        (status, frame) = video.read()
        while self.__active and status:
            (status, frame) = video.read()
            record.write(frame)  # 錄製影片到檔案
            imgArray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(imgArray)
            image.thumbnail((320,240)) # 縮小尺寸為320*240
            photo = ImageTk.PhotoImage(image=image)
            if hasattr(self.__window, 'configure') is True:
                self.__window.configure(
                    image=photo, width=photo.width(), height=photo.height())
                self.__window.rtspImage = photo
        video.release()
        record.release()

    # 因應視窗縮放，根據縮放比例重新定位視窗位置
    def Relocate(self):
        if self.__window is None:
            return
        # 取得因為視窗縮放產生的新座標
        result = self.__relocate.Relocate(self.__coordX, self.__coordY)
        newX = result["newX"]
        newY = result["newY"]
        # 重新定位RTSP Window的位置
        self.__window.place(x=newX, y=newY, anchor='nw')
        # 同步relocate連接線的位置
        self.__linkLine.Relocate(
            self.__tagX, self.__tagY, newX, newY)

    # RTSP視窗點擊事件
    def __ClickEvent(self, event):
        self.__preMoveCoordX = event.x
        self.__preMoveCoordY = event.y

    # RTSP視窗拖移事件
    def __DragEvent(self, event):
        # 這個移動的座標是window內部的，基準點也就是window左上角為(0,0)
        moveInWindowX = event.x
        moveInWindowY = event.y
        # 這個座標是RTSP視窗在frame容器中的座標位置
        newX = self.__coordX + (moveInWindowX - self.__preMoveCoordX)
        newY = self.__coordY + (moveInWindowY - self.__preMoveCoordY)
        # 更新RTSP視窗目前座標
        self.__coordX = newX
        self.__coordY = newY
        # 重新定位要移動的新座標
        self.Relocate()

    # RTSP視窗雙擊事件
    def __DoubleClickEvent(self, event):
        self.__closeMethod()

    # 設定與該RTSP Window對應的Camera Tag座標位置
    def SetCameraTagCoords(self, X, Y):
        self.__tagX = X
        self.__tagY = Y

    # 取得來源RTSP影像的編碼
    def getSourceFourcc(self, sourceVideo):
        code = sourceVideo.get(cv2.CAP_PROP_FOURCC)
        code = "".join([chr((int(code) >> 8 * i) & 0xFF) for i in range(4)])
        return code
