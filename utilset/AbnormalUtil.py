from utilset.SqlLiteUtil import SqlLiteUtil

# 處理異常紀錄寫DB的Util


class AbnormalUtil:

    # 新增一筆異常紀錄
    def InsertAbnormalRecord(self, TriggerTime, TagID):
        command = " INSERT INTO AbnormalRecord VALUES (:triggertime, :tagid) "
        parameter = {
            'triggertime': TriggerTime,
            'tagid': TagID
        }
        SqlLiteUtil().Execute(command, parameter)

    # 根據條件搜尋需要的異常紀錄
    def FindAbnormalRecord(self, TriggerTime=None, TagID=None):
        command = " SELECT * FROM AbnormalRecord WHERE 1=1 "
        parameter = {}
        # 開始根據條件搜尋
        if TriggerTime is not None:
            command += " AND TriggerTime=:trigeertime "
            parameter.trigeertime = TriggerTime
        if TagID is not None:
            command += " AND TagID=:tagid "
            parameter.tagid = TagID

        SqlLiteUtil().Execute(command, parameter)
