# 根據目前視窗的縮放比例，計算出新的座標位置
def Relocate(para):
    # 取出KV結構內資料待處理
    curWindowWidth = para['curWindowWidth'] if 'curWindowWidth' in para else 640
    curWindowHeight = para['curWindowHeight'] if 'curWindowHeight' in para else 480
    oriWindowWidth = para['oriWindowWidth'] if 'oriWindowWidth' in para else 640
    oriWindowHeight = para['oriWindowHeight'] if 'oriWindowHeight' in para else 480
    oriMapWidth = para['oriMapWidth'] if 'oriMapWidth' in para else 640
    oriMapHeight = para['oriMapHeight'] if 'oriMapHeight' in para else 480
    oriX = para['oriX'] if 'oriX' in para else 0
    oriY = para['oriY'] if 'oriY' in para else 0
    # 計算目前視窗寬高與原寬高異動比率(ex.據比例調整保全器材位置)
    ratioWidth = curWindowWidth / oriWindowWidth if curWindowWidth <= oriMapWidth \
        else oriMapWidth / oriWindowWidth
    ratioHeight = curWindowHeight / oriWindowHeight if curWindowHeight <= oriMapHeight \
        else oriMapHeight / oriWindowHeight
    # 判斷視窗放大超過原始地圖寬高，則增加空白偏移量(因地圖在視窗置中，故(視窗寬高-地圖寬高) / 2)
    offsetX = 0 if curWindowWidth <= oriMapWidth \
        else (curWindowWidth - oriMapWidth) / 2
    offsetY = 0 if curWindowHeight <= oriMapHeight \
        else (curWindowHeight - oriMapHeight) / 2
    # 計算新的座標位置
    newX = oriX * ratioWidth + offsetX
    newY = oriY * ratioHeight + offsetY
    # 回傳一份新座標位置的物件
    return {"newX": newX, "newY": newY}
