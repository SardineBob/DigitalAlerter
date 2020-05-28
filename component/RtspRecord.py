import tkinter as tk
from cv2 import cv2
import threading
import time
from utilset.ConfigUtil import ConfigUtil


class RtspRecord():

    __taskRecord = None
    __taskTimeout = None
    __active = False
    __tagID = None  # Camera Tag ID Number
    __url = None
    __recordFileName = None  # 從外界傳入的錄影檔名，該參數None時，系統自動預設

    def __init__(self, para):
        # 取出需用到的設定值
        self.__tagID = para["cameraTagID"]
        self.__url = ConfigUtil().getCameraPoint(self.__tagID)['rtspUrl']
        self.__recordFileName = para["recordFileName"]
        # 建立執行序並開始錄影
        self.Start()

    # 啟動RTSP錄影
    def Start(self):
        if self.__taskRecord is None:
            self.__taskRecord = threading.Thread(target=self.__Record)
            self.__taskRecord.setDaemon(True)
            self.__active = True
            self.__taskRecord.start()

    # 停止播放RTSP串流，並銷毀執行序(需等待python程序GC)
    def Stop(self):
        self.__active = False
        self.__taskRecord = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__taskTimeout = None  # 停止，執行序清掉(等待python程序GC)，以利下一次觸發

    # 執行RTSP影像串流錄影的動作
    def __Record(self):
        # 連接RTSP串流
        video = cv2.VideoCapture(self.__url)
        # 計算錄影片段尺寸，目前採縮小1/4
        recordSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH) / 4),
                      int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) / 4))
        # 準備錄影路徑與檔名
        filename = self.__recordFileName
        if self.__recordFileName is None:
            nowTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = "Camera" + str(self.__tagID) + "-" + nowTime + ".avi"
        filepath = "CameraRecord/" + filename
        # 準備錄影的相關參數
        recordForucc = cv2.VideoWriter_fourcc(*self.getSourceFourcc(video))
        recordFPS = int(video.get(cv2.CAP_PROP_FPS))
        # 建立錄影實體物件
        record = cv2.VideoWriter(filepath, recordForucc, recordFPS, recordSize)
        # 讀取RTSP串流，準備錄影
        (status, frame) = video.read()
        # 計數frame數量，根據FPS錄到符合設定值秒數，就停止錄影
        maxFrameCnt = recordFPS * ConfigUtil().SystemConfig.VideoTime
        frameCnt = 0
        # 開始錄影
        while self.__active and status:
            (status, frame) = video.read()
            # resize frame
            frame = cv2.resize(frame, recordSize)
            record.write(frame)  # 錄製影片到檔案
            frameCnt = frameCnt+1
            # 錄到指定的frame數量，就停止
            if frameCnt >= maxFrameCnt:
                self.Stop()
        # 釋放資源
        video.release()
        record.release()

    # 取得來源RTSP影像的編碼
    def getSourceFourcc(self, sourceVideo):
        code = sourceVideo.get(cv2.CAP_PROP_FOURCC)
        code = "".join([chr((int(code) >> 8 * i) & 0xFF) for i in range(4)])
        return code
