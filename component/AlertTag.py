from component.Tag import Tag
from PIL import Image, ImageTk


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'

    def __init__(self, x=0, y=0):
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # 傳入父類別，建立警報點標籤物件
        super().__init__(x, y, picPhoto)
