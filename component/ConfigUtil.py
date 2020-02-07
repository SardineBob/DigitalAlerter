import os
from tkinter import messagebox
import configparser
import json


class ConfigUtil():

    __filePath = 'config.ini'
    AlertPoints = None

    def __init__(self):
        # 判斷設定檔是否存在
        if os.path.exists(self.__filePath) is False:
            messagebox.showinfo("error", "設定檔不存在。")
            exit()
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath)
        # 讀取警報器材位置
        self.AlertPoints = json.loads(config["AlertPoint"]["point"])