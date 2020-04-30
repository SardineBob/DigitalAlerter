import os
import subprocess
import tkinter as tk
from tkinter import ttk
from utilset.AbnormalUtil import AbnormalUtil
from utilset.ConfigUtil import ConfigUtil


class AbnormalWindow():

    __window = None
    __treeView = None
    __listBox = None
    __closeMethod = None  # 呼叫端關閉本視窗的方法，通常包含呼叫本class的close event，以及呼叫端管理class關閉的實作方法
    __videoList = None  # 目前載入的錄影片段清單
    __PanelLayout = None  # 定義各元件部屬在Grid的位置
    __queryDate = None  # 存放輸入之查詢日期
    __queryAlert = None  # 存放選取之警報點位置

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
        # 設定Grid版面配置比例(最外層主要容器)
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=1)
        self.__window.grid_rowconfigure(2, weight=1)
        # 定義外層主要容器的版面配置定位點
        self.__PanelLayout = {
            'queryBar': {'row': 0, 'column': 0, 'sticky': 'EWNS', 'columnspan': 2},
            'queryBar.dateLabel': {'row': 0, 'column': 0, 'sticky': 'EWNS'},
            'queryBar.dateBox': {'row': 0, 'column': 1, 'sticky': 'EWNS'},
            'queryBar.alertLabel': {'row': 1, 'column': 0, 'sticky': 'EWNS'},
            'queryBar.alertSelect': {'row': 1, 'column': 1, 'sticky': 'EWNS'},
            'treeView': {'row': 1, 'column': 0, 'sticky': 'EWNS', 'rowspan': 2},
            'title': {'row': 1, 'column': 1, 'sticky': 'EWNS'},
            'listBox': {'row': 2, 'column': 1, 'sticky': 'EWNS'}
        }
        # 建立查詢區塊
        self.__CreateQueryBar()
        # 建立異常紀錄清單
        self.__CreateAbnormalTable()
        # 右邊版面標題
        title = tk.Label(self.__window, text="錄影片段", font=(
            "微軟正黑體", 12, "bold"), background="#DDDDDD")
        title.grid(self.__PanelLayout['title'])
        # 產生錄影片段選單
        self.__CreateVideoList()

    # 建立查詢區塊本體
    def __CreateQueryBar(self):
        # 建立一個查詢區塊容器，並建構在主容器中
        QueryBar = tk.Frame(self.__window)
        # 設定查詢區塊容器的版面配置比例
        QueryBar.grid_columnconfigure(0, weight=1)
        QueryBar.grid_columnconfigure(1, weight=4)
        QueryBar.grid(self.__PanelLayout['queryBar'])
        # 建立異常日期查詢功能列
        dateLabel = tk.Label(QueryBar, text="異常日期(yyyy/mm/dd)", font=(
            "微軟正黑體", 12, "bold"), background="#DDDDDD")
        dateLabel.grid(self.__PanelLayout['queryBar.dateLabel'])
        dateBox = tk.Entry(QueryBar, font=("微軟正黑體", 12, "bold"))
        dateBox.grid(self.__PanelLayout['queryBar.dateBox'])

        # 日期查詢輸入事件
        def dateBoxInput(event):
            # 值沒有變不需執行
            if self.__queryDate == dateBox.get():
                return
            # 強制把輸入空值轉為None
            self.__queryDate = None if dateBox.get() == '' else dateBox.get()
            # 更新異常紀錄清單
            self.__LoadAbnormalTable(self.__queryDate, self.__queryAlert)
        # 綁定loass focus跟按enter的事件
        dateBox.bind('<FocusOut>', dateBoxInput)
        dateBox.bind('<Return>', dateBoxInput)

        # 建立警報點查詢功能列
        alertLabel = tk.Label(QueryBar, text="警報位置", font=(
            "微軟正黑體", 12, "bold"), background="#DDDDDD")
        alertLabel.grid(self.__PanelLayout['queryBar.alertLabel'])
        alertSelect = ttk.Combobox(QueryBar, font=(
            "微軟正黑體", 12, "bold"), state="readonly", values=self.__getAlertNameList())
        alertSelect.grid(self.__PanelLayout['queryBar.alertSelect'])

        # 警報位置查詢選取事件
        def alertBoxSelect(event):
            # 值沒有變不需執行
            if self.__queryAlert == alertSelect.get():
                return
            # 強制把輸入空值轉為None
            self.__queryAlert = None if alertSelect.get() == '' else alertSelect.get()
            # 更新異常紀錄清單
            self.__LoadAbnormalTable(self.__queryDate, self.__queryAlert)
        # 綁定選取下拉選單事件
        alertSelect.bind("<<ComboboxSelected>>", alertBoxSelect)

    # 讀取警報點位置選取清單
    def __getAlertNameList(self):
        list = []
        for point in ConfigUtil().AlertPoints:
            list.append(point['number'])
        return list

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
        self.__treeView.heading("AlertID", text="警報位置")
        # 設定treeview的樣式
        style = ttk.Style()
        style.configure("Treeview", font=("微軟正黑體", 12))
        style.configure("Treeview.Heading", font=("微軟正黑體", 14, "bold"))
        self.__treeView.tag_configure("odd", background="#FFFFFF")
        self.__treeView.tag_configure("even", background="#DDDDDD")
        # 載入資料
        self.__LoadAbnormalTable()
        # 左邊滿版，擺入異常紀錄清單
        self.__treeView.grid(self.__PanelLayout['treeView'])

    # 讀取異常清單表格
    def __LoadAbnormalTable(self, AlertTime=None, AlertID=None):
        # 清空treeview(星號(*)，類似視為Tuple)
        self.__treeView.delete(*self.__treeView.get_children())
        # 撈取異常紀錄清單資料
        data = AbnormalUtil().FindAbnormalRecord(AlertTime, AlertID)
        # 逐筆呈現在表格內
        for item in data:
            itemFormat = "even" if data.index(item) % 2 == 0 else "odd"
            # 取出各欄位資料
            alertTime = item['AlertTime']
            alertID = item['AlertID']
            # 透過treeview呈現
            self.__treeView.insert("", "end", value=(
                alertTime, alertID), tags=(itemFormat))
        # 綁定選取的事件
        self.__treeView.bind('<Button-1>', self.__TreeViewSelected)

    # 選取異常清單項目事件，建立該異常時間發生之攝影機錄影片段
    def __TreeViewSelected(self, event):
        # 擷取選取的警示時間與警示點為何
        selectedItem = self.__treeView.identify('item', event.x, event.y)
        selectedData = self.__treeView.item(selectedItem, 'values')
        selectedAlertTime = selectedData[0]
        selectedAlertID = selectedData[1]
        # 觸發更新錄影片段清單
        self.__LoadVideoList(selectedAlertTime, selectedAlertID)

    # 建立錄影片段清單本體
    def __CreateVideoList(self):
        if self.__listBox is not None:
            return
        # ListBox初始設定
        self.__listBox = tk.Listbox(self.__window)
        self.__listBox.configure(
            font=("微軟正黑體", 12), justify="center", highlightthickness=0)
        # 右邊版面內容，擺入選取之異常紀錄的錄影檔選單
        self.__listBox.grid(self.__PanelLayout['listBox'])

    # 讀取錄影片段清單
    def __LoadVideoList(self, AlertTime, AlertID):
        # 清空預備載入資料
        if self.__listBox is not None:
            self.__listBox.delete(0, tk.END)
        # 根據警示時間與警示器材代碼，取得錄影片段清單
        self.__videoList = AbnormalUtil().FindRecordList(AlertTime, AlertID)
        # 逐筆呈現於ListBox
        for item in self.__videoList:
            index = self.__videoList.index(item)
            cameraID = item['CameraID']
            self.__listBox.insert(index, cameraID)
        # 綁定選取事件
        self.__listBox.bind('<Double-1>', self.__ListBoxSelected)

    # 點選錄影片事件，開啟該錄影片段影片檔案
    def __ListBoxSelected(self, event):
        # 擷取選取的錄影片段在ListBox的Index
        widget = event.widget
        index = widget.curselection()[0]
        # 根據index到List取得錄影片段檔名
        videoFileName = self.__videoList[index]['RecordFileName']
        # 透過Window Media Plyer播放影片
        playerPath = "C:/Program Files/Windows Media Player/wmplayer.exe"
        videoPath = os.path.join(
            os.path.abspath('.'), 'CameraRecord', videoFileName)
        subprocess.Popen(playerPath + ' ' + videoPath)

    # 視窗關閉，用於外部呼叫
    def WindowClose(self):
        self.__window.destroy()
        self.__window = None
