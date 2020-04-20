from utilset.SqlLiteUtil import SqlLiteUtil

# 處理異常紀錄寫DB的Util


class AbnormalUtil:

    # 新增一筆異常紀錄
    def InsertAbnormalRecord(self, para):
        # 取出相關資訊，準備Insert資料
        TriggerTime = para["triggerTime"]
        AlertID = para["alertID"]
        CameraInfos = para["cameraInfo"]  # this is array
        # 準備Insert INTO指令，並執行
        commands = []
        # insert into AbnormalList
        commands.append({
            'command': " INSERT INTO AbnormalList VALUES (:triggertime, :alertid, '') ",
            'parameter': {
                'triggertime': TriggerTime,
                'alertid': AlertID
            }
        })
        # insert into RecordList
        for camera in CameraInfos:
            commands.append({
                'command': " INSERT INTO RecordList VALUES (:triggertime, :alertid, :cameraid, '', :recordfilename) ",
                'parameter': {
                    'triggertime': TriggerTime,
                    'alertid': AlertID,
                    'cameraid': camera['cameraID'],
                    'recordfilename': camera['recordFileName'],
                }
            })
        for command in commands:
            SqlLiteUtil().Execute(command['command'], command['parameter'])

    # 根據條件搜尋需要的異常紀錄
    def FindAbnormalRecord(self, TriggerTime=None, TagID=None):
        command = " SELECT * FROM AbnormalRecord WHERE 1=1 "
        parameter = {}
        # 開始根據條件搜尋
        if TriggerTime is not None:
            command += " AND TriggerTime=:trigeertime "
            parameter["trigeertime"] = TriggerTime
        if TagID is not None:
            command += " AND TagID=:tagid "
            parameter["tagid"] = TagID

        return SqlLiteUtil().Execute(command, parameter)
