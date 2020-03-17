from websocket import enableTrace, WebSocketApp
import threading


class RaspberryPiSignal:

    __wsUrl = "ws://localhost:9453"
    __ws = None
    __task = None
    __alertTagCollection = None

    def __init__(self, alertTagCollection):
        # enableTrace(True)  # 啟動偵錯模式
        self.__alertTagCollection = alertTagCollection
        self.__createTask()

    # 將接收websocket訊號的方法，使用執行序背景執行
    def __createTask(self):
        if self.__task is None:
            self.__task = threading.Thread(target=self.__createWebsocket)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__task.start()

    # 關閉執行序
    def closeTask(self):
        self.__ws.close()
        self.__ws = None
        self.__task = None
        self.__alertTagCollection = None

    # 產生WebSocket連線
    def __createWebsocket(self):
        if self.__ws is not None:
            return
        self.__ws = WebSocketApp(
            self.__wsUrl,
            on_open=self.__onOpen,
            on_message=self.__onMessage,
            on_error=self.__onError,
            on_close=self.__onClose
        )
        self.__ws.run_forever()

    def __onMessage(self, message):
        if self.__alertTagCollection is None:
            return
        # 根據收到的Websocket哪一個Alert設備，去執行這一個AlertTag觸發警報事件
        self.__alertTagCollection[int(message)].TriggerAlert()
        print("收到的Alert Tag號碼" + message)

    def __onError(self, error):
        print("###WebSocket-Error###")
        print(error)
        self.closeTask()

    def __onClose(self):
        print("###WebSocket-Close###")
        self.closeTask()

    def __onOpen(self):
        print("###WebSocket-Open###")
