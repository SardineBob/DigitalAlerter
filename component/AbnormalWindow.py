import tkinter as tk
from tkinter import ttk
from utilset.AbnormalUtil import AbnormalUtil


class AbnormalWindow():

    __window = None
    __treeView = None
    __closeMethod = None  # 呼叫端關閉本視窗的方法，通常包含呼叫本class的close event，以及呼叫端管理class關閉的實作方法

    def __init__(self, para):
        # 取出需使用的設定值
        self.__closeMethod = para["closeMethod"]
        # 開始建立一個子視窗
        self.__window = tk.Toplevel()
        self.__window.geometry("640x480+50+50")
        # 註冊視窗關閉事件，使用者點擊視窗的X，會觸發
        self.__window.protocol("WM_DELETE_WINDOW", self.__closeMethod)
        # 建立異常紀錄清單本體
        self.__CreateAbnormalTable()

    # 建立異常紀錄清單表格本體
    def __CreateAbnormalTable(self):
        # 創建treeview widget (show="headings"可隱藏自動產生的第一列)
        self.__treeView = ttk.Treeview(self.__window, show="headings")
        # 定義欄位
        self.__treeView["columns"] = ("TriggerTime", "TagID")
        self.__treeView.column("TriggerTime", minwidth=170, anchor=tk.CENTER)
        self.__treeView.column("TagID", minwidth=100, anchor=tk.CENTER)
        # 定義標題
        self.__treeView.heading("TriggerTime", text="異常觸發時間")
        self.__treeView.heading("TagID", text="警報點ID")
        # 展開至整個視窗
        self.__treeView.pack(fill="both", expand=True)
        # 設定treeview的樣式
        style = ttk.Style()
        style.configure("Treeview", font=("微軟正黑體", 12))
        style.configure("Treeview.Heading", font=("微軟正黑體", 14, "bold"))
        self.__treeView.tag_configure("odd", background="#FFFFFF")
        self.__treeView.tag_configure("even", background="#DDDDDD")
        # 載入資料
        self.__LoadAbnormalTable()

    # 讀取異常清單表格
    def __LoadAbnormalTable(self):
        # 撈取異常紀錄清單資料
        data = AbnormalUtil().FindAbnormalRecord()
        # 逐筆呈現在表格內
        for item in data:
            itemFormat = "even" if data.index(item) % 2 == 0 else "odd"
            self.__treeView.insert(
                "", 0, text="", value=(item), tags=(itemFormat))

    # 視窗關閉，用於外部呼叫
    def WindowClose(self):
        self.__window.destroy()
        self.__window = None
