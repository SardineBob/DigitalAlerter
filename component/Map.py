import tkinter as tk
from PIL import Image, ImageTk


class Map():
    __mapPath = './resource/map.jpg'
    __mapLoad = None
    __mapWidth = None
    __mapHeight = None
    __mapContainer = None

    def __init__(self):
        self.__mapLoad = Image.open(self.__mapPath)
        self.__mapWidth = self.__mapLoad.width
        self.__mapHeight = self.__mapLoad.height
        # 設定地圖的容器，用一個Label物件來裝
        self.__mapContainer = tk.Label(bg='black')
        self.__mapContainer.pack(fill='both', expand=True)  # 全面展開

    def Create(self, width=640, height=480):
        # 視窗寬度(高度)小於Map圖片原寬(高)，resize成視窗寬度(高度)，否則維持圖片原寬(高)
        width = width if width <= self.__mapWidth else self.__mapWidth
        height = height if height <= self.__mapHeight else self.__mapHeight
        # Map異動為指定的大小
        mapImage = self.__mapLoad.resize((width, height))
        # 讀入放Image的容器(Label)
        photoImg = ImageTk.PhotoImage(mapImage)
        self.__mapContainer.configure(image=photoImg)
        # ↓avoid garbage collection(避免資源被回收)
        self.__mapContainer.image = photoImg
