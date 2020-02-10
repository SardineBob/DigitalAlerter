import tkinter as tk


class Tag():

    __canvas = None
    __tagid = None
    __bgid = None
    __pointid = None
    __tagX = 0
    __tagY = 0
    __tagW = 0
    __tagH = 0

    def __init__(self, canvas, pointid, x, y, picPhoto, tagName):
        self.__canvas = canvas
        self.__pointid = pointid
        self.__tagX = x
        self.__tagY = y
        self.__tagW = picPhoto.width()
        self.__tagH = picPhoto.height()
        # 先繪製Tag背景圓型，並預設為綠色(警報時為紅色)(__getBGCoords=>計算微調背景圓型在tag的位置)
        self.__bgid = canvas.create_oval(
            self.__getBGCoords(self.__tagX, self.__tagY),
            fill='#00ff00',
            tags=tagName
        )
        # 繪製Tag圖示
        self.__tagid = canvas.create_image(
            x, y, image=picPhoto, anchor=tk.NW, tags=tagName)

    def Relocate(self, para):
        # 取出KV結構內資料待處理
        curWindowWidth = para['curWindowWidth'] if 'curWindowWidth' in para else 640
        curWindowHeight = para['curWindowHeight'] if 'curWindowHeight' in para else 480
        oriWindowWidth = para['oriWindowWidth'] if 'oriWindowWidth' in para else 640
        oriWindowHeight = para['oriWindowHeight'] if 'oriWindowHeight' in para else 480
        oriMapWidth = para['oriMapWidth'] if 'oriMapWidth' in para else 640
        oriMapHeight = para['oriMapHeight'] if 'oriMapHeight' in para else 480
        # 計算目前視窗寬高與原寬高異動比率(ex.據比例調整保全器材位置)
        ratioWidth = curWindowWidth / oriWindowWidth if curWindowWidth <= oriMapWidth \
            else oriMapWidth / oriWindowWidth
        ratioHeight = curWindowHeight / oriWindowHeight if curWindowHeight <= oriMapHeight \
            else oriMapHeight / oriWindowHeight
        # 判斷視窗放大超過原始地圖寬高，則增加空白偏移量(因地圖在視窗置中，故(視窗寬高-地圖寬高) / 2)
        offsetX = 0 if curWindowWidth <= oriMapWidth \
            else (curWindowWidth - oriMapWidth) / 2
        offsetY = 0 if curWindowHeight <= oriMapHeight \
            else (curWindowHeight - oriMapHeight) / 2
        # 重新定位tag(包含背景)的位置
        newX = self.__tagX * ratioWidth + offsetX
        newY = self.__tagY * ratioHeight + offsetY
        self.__canvas.coords(self.__tagid, newX, newY)
        self.__canvas.coords(
            self.__bgid,
            self.__getBGCoords(newX, newY)
        )

    # 計算Tag背景的圓型位置，這邊只是微調一下，讓畫面好看
    def __getBGCoords(self, tagX, tagY):
        return (
            tagX - 1,
            tagY + 1,
            tagX + self.__tagW,
            tagY + 1 + self.__tagH
        )