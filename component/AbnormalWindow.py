import tkinter as tk
from tkinter import ttk
from utilset.AbnormalUtil import AbnormalUtil


class AbnormalWindow():

    __window = None
    __treeView = None
    __listBox = None
    __closeMethod = None  # 呼叫端關閉本視窗的方法，通常包含呼叫本class的close event，以及呼叫端管理class關閉的實作方法

    def __init__(self, para):
        # 取出需使用的設定值
        self.__closeMethod = para["closeMethod"]
        # 開始建立一個子視窗
        self.__window = tk.Toplevel()
        self.__window.geometry("480x480+50+50")
        # 註冊視窗關閉事件，使用者點擊視窗的X，會觸發
        self.__window.protocol("WM_DELETE_WINDOW", self.__closeMethod)
        # 產生版面
        self.__CreatePanel()

    # 產生版面(左版面：異常紀錄清單，右版面：選取異常紀錄之對應的錄影檔)
    def __CreatePanel(self):
        # 設定Grid版面配置比例
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=1)
        self.__window.grid_rowconfigure(1, weight=1)
        # 建立異常紀錄清單
        self.__CreateAbnormalTable()
        # 左邊滿版，擺入異常紀錄清單
        self.__treeView.grid(row=0, column=0, sticky='EWNS', rowspan=2)
        # 右邊版面標題
        title = tk.Label(self.__window, text="錄影片段", font=(
            "微軟正黑體", 12, "bold"), background="#DDDDDD")
        title.grid(row=0, column=1, sticky='EWNS')
        # 右邊版面內容，擺入選取之異常紀錄的錄影檔選單
        self.__CreateVideoList()
        self.__listBox.grid(row=1, column=1, sticky="EWNS")

    # 建立異常紀錄清單表格本體
    def __CreateAbnormalTable(self):
        # 創建treeview widget (show="headings"可隱藏自動產生的第一列)
        self.__treeView = ttk.Treeview(self.__window, show="headings")
        # 定義欄位
        self.__treeView["columns"] = ("TriggerTime", "AlertID")
        self.__treeView.column("TriggerTime", minwidth=170,
                               width=170, anchor=tk.CENTER)
        self.__treeView.column("AlertID", minwidth=100,
                               width=100, anchor=tk.CENTER)
        # 定義標題
        self.__treeView.heading("TriggerTime", text="異常觸發時間")
        self.__treeView.heading("AlertID", text="警報點ID")
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
            # 取出各欄位資料
            alertTime = item['alertTime']
            alertID = item['alertID']
            # 透過treeview呈現
            self.__treeView.insert("", "end", value=(
                alertTime, alertID), tags=(itemFormat))

    # 建立錄影片段清單本體
    def __CreateVideoList(self):
        self.__listBox = tk.Listbox(self.__window)
        self.__listBox.configure(
            font=("微軟正黑體", 12), justify="center", highlightthickness=0)
        self.__listBox.insert(0, '0001')
        self.__listBox.insert(1, '0002')
        self.__listBox.insert(2, '0003')
        self.__listBox.insert(3, '0004')
        self.__listBox.insert(4, '0005')
        self.__listBox.insert(5, '0006')

    # 視窗關閉，用於外部呼叫
    def WindowClose(self):
        self.__window.destroy()
        self.__window = None
