from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading


class CameraTag(Tag):

    __picPath = './resource/IconCamera.png'

    def __init__(self, canvas, pointid, x=0, y=0):
        # open攝影機標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "cameraIcon") is False:
            canvas.cameraIcon = []
        canvas.cameraIcon.append(picPhoto)
        # 傳入父類別，建立攝影機標籤物件
        super().__init__(canvas, pointid, x, y, picPhoto, 'camera')