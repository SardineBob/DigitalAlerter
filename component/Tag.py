import tkinter as tk
from library.LocationFunc import Relocate


class Tag():

    canvas = None
    tagid = None
    bgid = None
    pointid = None
    tagX = 0
    tagY = 0
    tagW = 0
    tagH = 0

    def __init__(self, canvas, pointid, x, y, picPhoto, tagName):
        self.canvas = canvas
        self.pointid = pointid
        self.tagX = x
        self.tagY = y
        self.tagW = picPhoto.width()
        self.tagH = picPhoto.height()
        # 先繪製Tag背景圓型，並預設為綠色(警報時為紅色)(__getBGCoords=>計算微調背景圓型在tag的位置)
        self.bgid = canvas.create_oval(
            self.getBGCoords(self.tagX, self.tagY),
            fill='#00ff00',
            tags=tagName
        )
        # 繪製Tag圖示
        self.tagid = canvas.create_image(
            x, y, image=picPhoto, anchor=tk.NW, tags=tagName)

    def Relocate(self, para):
        # 放置目前的XY座標
        para["oriX"] = self.tagX
        para["oriY"] = self.tagY
        # 取得因為視窗縮放產生的新座標
        result = Relocate(para)
        newX = result["newX"]
        newY = result["newY"]
        # 重新定位tag(包含背景)的位置
        self.canvas.coords(self.tagid, newX, newY)
        self.canvas.coords(self.bgid, self.getBGCoords(newX, newY))

    # 計算Tag背景的圓型位置，這邊只是微調一下，讓畫面好看
    def getBGCoords(self, tagX, tagY):
        return (
            tagX - 1,
            tagY + 1,
            tagX + self.tagW,
            tagY + 1 + self.tagH
        )
