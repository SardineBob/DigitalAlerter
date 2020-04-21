from utilset.SqlLiteUtil import SqlLiteUtil

# 處理異常紀錄寫DB的Util


class AbnormalUtil:

    # 新增一筆異常紀錄
    def InsertAbnormalRecord(self, para):
        # 取出相關資訊，準備Insert資料
        AlertTime = para["alertTime"]
        AlertID = para["alertID"]
        CameraInfos = para["cameraInfo"]  # this is array
        # 準備Insert INTO指令，並執行
        commands = []
        # insert into AbnormalList
        commands.append({
            'command': " INSERT INTO AbnormalList VALUES (:alerttime, :alertid, '') ",
            'parameter': {
                'alerttime': AlertTime,
                'alertid': AlertID
            }
        })
        # insert into RecordList
        for camera in CameraInfos:
            commands.append({
                'command': " INSERT INTO RecordList VALUES (:alerttime, :alertid, :cameraid, '', :recordfilename) ",
                'parameter': {
                    'alerttime': AlertTime,
                    'alertid': AlertID,
                    'cameraid': camera['cameraID'],
                    'recordfilename': camera['recordFileName'],
                }
            })
        for command in commands:
            SqlLiteUtil().Execute(command['command'], command['parameter'])

    # 根據條件搜尋需要的異常紀錄
    def FindAbnormalRecord(self, AlertTime=None, AlertID=None):
        abnormalRecordList = []
        # 先取得異常紀錄清單，即保全器材的觸發時間點
        command = " SELECT AlertTime, AlertID FROM AbnormalList WHERE 1=1 "
        parameter = {}
        # 開始根據條件搜尋
        if AlertTime is not None:
            command += " AND AlertTime=:alerttime "
            parameter["alerttime"] = AlertTime
        if AlertID is not None:
            command += " AND AlertID=:alertid "
            parameter["alertid"] = AlertID
        abnormalList = SqlLiteUtil().Execute(command, parameter)
        # 逐一取得觸發時間點，對應各攝影機的錄影檔名資訊
        for abnormalItem in abnormalList:
            alertTime, alertID = abnormalItem
            # 取得這個觸發時間點，攝影機錄影檔名
            command = " SELECT CameraID, RecordFileName FROM RecordList WHERE AlertTime=:alerttime AND AlertID=:alertid "
            parameter = {
                'alerttime': alertTime,
                'alertid': alertID
            }
            recordList = SqlLiteUtil().Execute(command, parameter)
            # 將錄影檔名，整理成List<Object>放進異常紀錄清單
            cameraList = []
            for recordItem in recordList:
                cameraID, recordFileName = recordItem
                cameraList.append({
                    'cameraID': cameraID,
                    'recordFileName': recordFileName
                })

            # 加工與結合查詢結果，轉為List<Object>形式回傳
            abnormalRecordList.append({
                'alertTime': alertTime,
                'alertID': alertID,
                'cameraInfo': cameraList
            })

        return abnormalRecordList
