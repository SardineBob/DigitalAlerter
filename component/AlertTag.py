from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime
from utilset.AbnormalUtil import AbnormalUtil


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'
    __task = None
    __flickerStatus = False  # 控制Tag閃爍的開關
    __cameraMappingID = None  # 這個警報點對應的攝影機ID
    __cameraMappingTag = None  # 這個警報點對應的攝影機實體物件

    def __init__(self, canvas, relocate, configItem):
        # 取出需用到的設定值
        pointid = configItem["number"]
        x = configItem["X"]
        y = configItem["Y"]
        self.__cameraMappingID = configItem["cameraLink"]
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "alertIcon") is False:
            canvas.alertIcon = []
        canvas.alertIcon.append(picPhoto)
        # 傳入父類別，建立警報點標籤物件
        super().__init__(canvas, relocate, pointid, x, y, picPhoto, 'alert')

    # 標籤觸發警報動作，閃爍背景(紅色)來達到視覺注目效果(使用執行序來跑，以免畫面lock)
    def TriggerAlert(self):
        if self.__task is None:
            # 建立執行序實體
            self.__task = threading.Thread(target=self.__TagFlicker)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__flickerStatus = True  # 開啟背景閃爍
            self.__task.start()
            # 產生觸發時間與錄影檔名
            nowTime = datetime.now()
            cameraInfo = []
            # 觸發啟動攝影機動作
            for camera in self.__cameraMappingTag:
                filename = nowTime.strftime('%Y%m%d%H%M%S') + \
                    "-Alert" + str(self.pointid) + \
                    "-Camera" + str(camera.pointid) + ".avi"
                camera.SetRecordFileName(filename)
                camera.openRtsp()
                # 蒐集錄影檔名，準備寫入DB
                cameraInfo.append({
                    'cameraID': camera.pointid,
                    'recordFileName': filename
                })
            # 警示觸發時，記錄一筆異常紀錄
            triggerTime = nowTime.strftime('%Y/%m/%d %H:%M:%S')
            AbnormalUtil().InsertAbnormalRecord({
                'alertTime': triggerTime,
                'alertID': self.pointid,
                'cameraInfo': cameraInfo
            })

    # 停止警報觸發動作，停止背景閃爍
    def TriggerStop(self):
        self.__flickerStatus = False
        self.__task = None  # 停止閃爍，執行序清掉(等待python程序GC)，以利下一次觸發
        # 觸發關閉攝影機動作
        for camera in self.__cameraMappingTag:
            camera.closeRtsp()

    # 執行背景閃爍的特效(紅綠背景互換)
    def __TagFlicker(self):
        while self.__flickerStatus is True:
            self.canvas.itemconfig(self.bgid, fill='#ff0000')
            time.sleep(0.25)
            self.canvas.itemconfig(self.bgid, fill='#00ff00')
            time.sleep(0.25)

    # 連結攝影機，根據設定檔中這個警報點連接的攝影機ID，去取出攝影機實體物件中，觸發開啟RTSP影像的事件
    def linkCamera(self, cameraTagCollection):
        self.__cameraMappingTag = []
        for id in self.__cameraMappingID:
            self.__cameraMappingTag.append(cameraTagCollection[id-1])
