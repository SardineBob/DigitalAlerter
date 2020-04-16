import os
from utilset.SqlLiteUtil import SqlLiteUtil


# 偵測若DB檔案存在就不做Create Table的動作
if os.path.isfile('dbfile/AbnormalRecord.db'):
    print('DB檔案存在，不允許再次創建，請手動移除該檔案後再嘗試。')
    exit()

# create table for abnormal record
command = "CREATE TABLE AbnormalRecord(\
    TrigeerTime Text PRIMARY KEY,\
    TagID INTEGER NOT NULL\
)"

# go to execoute
SqlLiteUtil().Execute(command, [])

print('DB創建成功。')
