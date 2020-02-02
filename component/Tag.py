import tkinter as tk


class Tag():

    __tag = None
    __x = 0
    __y = 0

    def __init__(self):
        self.__tag = tk.Label(text="this is label", bg="green")
        self.__x = 39
        self.__y = 67
        self.__tag.place(x=self.__x, y=self.__y)
        #self.__tag.bind('<Button-1>', self.click)

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
        # 重新定位tag的位置
        self.__tag.place(x=self.__x * ratioWidth + offsetX,
                         y=self.__y * ratioHeight + offsetY)

    # def click(self,event):
    #    print('OKOKOKOK')
