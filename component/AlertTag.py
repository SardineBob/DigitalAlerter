from component.Tag import Tag
from PIL import Image, ImageTk


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'

    def __init__(self, canvas, x=0, y=0):
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        canvas.alertIcon = picPhoto
        # 傳入父類別，建立警報點標籤物件
        super().__init__(canvas, x, y, picPhoto, 'alert')
