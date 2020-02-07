import configparser
import json

filePath = 'config.ini'
config = configparser.ConfigParser()

# 產生警報點位置資料
config['AlertPoint'] = {
    'point': json.dumps([
        {'number': 1, 'X': 25, 'Y': 25},
        {'number': 2, 'X': 50, 'Y': 50},
        {'number': 3, 'X': 75, 'Y': 75},
        {'number': 4, 'X': 100, 'Y': 100},
        {'number': 5, 'X': 125, 'Y': 125}
    ])
}

# 寫入設定檔
with open('config.ini', 'w') as configFile:
    config.write(configFile)
