import tkinter as tk


class Tag():

    canvas = None
    relocate = None
    tagid = None
    bgid = None
    pointid = None
    name = None
    tagX = 0  # 目前tag的座標位置
    tagY = 0
    tagW = 0
    tagH = 0
    oriTagX = 0  # 初始化時tag的座標位置，作為計算視窗縮放後新座標基準
    oriTagY = 0

    def __init__(self, canvas, relocate, pointid, name, x, y, picPhoto, tagName):
        self.canvas = canvas
        self.relocate = relocate
        self.pointid = pointid
        self.name = name
        self.tagX = self.oriTagX = x
        self.tagY = self.oriTagY = y
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

    def Relocate(self):
        # 取得因為視窗縮放產生的新座標
        result = self.relocate.Relocate(self.oriTagX, self.oriTagY)
        self.tagX = result["newX"]
        self.tagY = result["newY"]
        # 重新定位tag(包含背景)的位置
        self.canvas.coords(self.tagid, self.tagX, self.tagY)
        self.canvas.coords(self.bgid, self.getBGCoords(self.tagX, self.tagY))

    # 計算Tag背景的圓型位置，這邊只是微調一下，讓畫面好看
    def getBGCoords(self, tagX, tagY):
        return (
            tagX - 1,
            tagY + 1,
            tagX + self.tagW,
            tagY + 1 + self.tagH
        )
