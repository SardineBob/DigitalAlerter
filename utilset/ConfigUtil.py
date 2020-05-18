import os
from tkinter import messagebox
import configparser
import json


class ConfigUtil():

    __filePath = 'config.ini'
    AlertPoints = None
    cameraPoints = None
    RaspberryPis = None

    def __init__(self):
        # 判斷設定檔是否存在
        if os.path.exists(self.__filePath) is False:
            messagebox.showinfo("error", "設定檔不存在。")
            exit()
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取警報器材位置
        self.AlertPoints = json.loads(config["AlertPoint"]["point"])
        # 讀取攝影機位置
        self.cameraPoints = json.loads(config["CameraPoint"]["point"])
        # 讀取樹梅派Websocket位址
        self.RaspberryPis = json.loads(config["RaspberryPiWebsocket"]["device"])
