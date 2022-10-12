#đọc n sector trong file
def getBufferDataBySector(file, begin, sector, bts=512):
    file.seek(begin*bts)

    result = file.read(sector*bts)
    return result

#đọc số lương offset trong 1 buffer (trả về dạng buffer)
def getBufferDataByOffset(buffer, begin, offset, bts=512):
    '''
        get sub buffer
    '''
    result = buffer[begin: begin+offset]
    return result

#đọc số lượng offset trong 1 buffer (trả về dạng byte)
def getValueOfBufferByOffset(buffer, begin, offset, bts=512):
    '''
        get sub buffer in byte type
    '''
    subBuffer = getBufferDataByOffset(buffer, begin, offset, bts)

    #do là little-radien nên ta phải đảo các offset đọc được và lấy giá trị của nó
    result = int(subBuffer[::-1].hex(), 16)
    return result

#hàm này được dùng cho việc đọc content ở dạng non-resident
def getContentByCluster(file, begin, clusters, sc, bts=512):
    listOfSector = []
    #lấy tất cả sector từ cluster bắt đầu tới kết thúc,
    #sc: số sector/cluster
    for cluster in range(begin, begin+clusters):
        for i in range(sc):
            sector = cluster*sc + i
            listOfSector.append(sector)
    
    #đọc tất cả sector và lấy ra content nó đang chứa
    content = b''
    for sector in listOfSector:
        content = content + getBufferDataBySector(file, sector, 1, bts)

    return content
