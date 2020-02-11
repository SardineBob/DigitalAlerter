from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'
    __task = None
    __flickerStatus = False  # 控制Tag閃爍的開關

    def __init__(self, canvas, pointid, x=0, y=0):
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "alertIcon") is False:
            canvas.alertIcon = []
        canvas.alertIcon.append(picPhoto)
        # 傳入父類別，建立警報點標籤物件
        super().__init__(canvas, pointid, x, y, picPhoto, 'alert')

    # 標籤觸發警報動作，閃爍背景(紅色)來達到視覺注目效果(使用執行序來跑，以免畫面lock)
    def TriggerAlert(self):
        if self.__task is None:
            # 建立執行序實體
            self.__task = threading.Thread(target=self.__TagFlicker)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__flickerStatus = True  # 開啟背景閃爍
            self.__task.start()

    # 停止警報觸發動作，停止背景閃爍
    def TriggerStop(self):
        self.__flickerStatus = False
        self.__task = None  # 停止閃爍，執行序清掉(等待python程序GC)，以利下一次觸發

    # 執行背景閃爍的特效(紅綠背景互換)
    def __TagFlicker(self):
        while self.__flickerStatus is True:
            self.canvas.itemconfig(self.bgid, fill='#ff0000')
            time.sleep(0.25)
            self.canvas.itemconfig(self.bgid, fill='#00ff00')
            time.sleep(0.25)
