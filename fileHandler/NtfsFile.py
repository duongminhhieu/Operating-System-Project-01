from datetime import datetime, timedelta
from utils.buffer import *
from utils.directory import Directory
from utils.factory import *
from constant.attribute import *
from constant.offset import *
from constant.document import *
from pattern.composite import *
from build.console import *

class NtfsFile:
    def __init__(self, file, root:CItem, directory:Directory):
        self.file = file
        self.root:CItem = root
        self.directory = directory

    #đọc phần boot sector
    def readPartitionRootSector(self):
        #get first sector to read prs
        buffer = getBufferDataBySector(self.file, 0, 1)

        # đọc size của sector
        self.sectorSize = getValueOfBufferByOffset(buffer, PDS_SECTOR_SIZE['hex'], PDS_SECTOR_SIZE['byte'])
        # đọc số sector / cluster
        self.sc = getValueOfBufferByOffset(buffer, PDS_SECTOR_CLUSTER['hex'], PDS_SECTOR_CLUSTER['byte'])
        # đọc tổng số sector
        self.totalSector = getValueOfBufferByOffset(buffer, PDS_TOTAL_SECTOR['hex'], PDS_TOTAL_SECTOR['byte'])
        # đọc vị trí bắt đầu của MFT cluster
        self.startedMFTCluster = getValueOfBufferByOffset(buffer, PDS_STARTED_MFT_CLUSTER['hex'], PDS_STARTED_MFT_CLUSTER['byte'])
        # đọc vị trí của MFT cluster dự phòng cho MFT cluster chính
        self.mirrorMFTCluster = getValueOfBufferByOffset(buffer, PDS_MIRROR_MFT_CLUSTER['hex'], PDS_MIRROR_MFT_CLUSTER['byte'])

        #in thông tin
        print(f'Sector size: {self.sectorSize}(bytes)')
        print(f'Sector/cluster: {self.sc}(s)')
        print(f'Total Sector: {self.totalSector}(s)')
        print(f'Started MFT Cluster: {self.startedMFTCluster * self.sc}(s)')
        print(f'Mirror MFT Cluster: {self.mirrorMFTCluster * self.sc}(s)')

    def readMasterFileTable(self):
        sector = 0

        # lưu trữ file hoặc folder bằng composite pattern
        subFolder:CItem = None

        # lưu các thông tin lưu trữ của file hoặc folder
        size = 0
        name = ''
        content = ''
        createAt = ''
        updateAt = ''

        #chúng ta thực hiện demo nên không thể đọc hết tất cả sector, nên ta chỉ cần đọc đến hết phần content 
        #đang có trong ổ đĩa
        total_skip_signature = 0

        while sector <= self.totalSector:
            #lấy 2 sector, tương ứng 1024 byte để đọc
            buffer = getBufferDataBySector(self.file, sector + self.startedMFTCluster * self.sc, 2)
            #đọc phần signature 
            signature = getBufferDataByOffset(buffer, MFT_SIGNATURE['hex'], MFT_SIGNATURE['byte'])

            #nếu signature không phải FILE (BADD) thì ta không xử lý
            if b'FILE' != signature:
                sector = sector + 2
                total_skip_signature +=1

                #khi đã đọc hết content trong ổ đĩa (mà chưa hết GB) thì ta cũng nên break để tránh tràn stack
                if total_skip_signature > 100: break
                continue
            
            #check xem có phải folder hay file
            isFolder = getValueOfBufferByOffset(buffer, MFT_ATTRIBUTE_TYPE['hex'], MFT_ATTRIBUTE_TYPE['byte']) & 0x02

            #lấy vị trí bắt đầu của MFT
            attributeOffsetStarted = getValueOfBufferByOffset(buffer, MFT_STARTED_ATTRIBUTE['hex'], MFT_STARTED_ATTRIBUTE['byte'])

            index = 0
            attributeType = 0x00

            #duyệt qua MFT table
            while index <= 1024 and attributeType != 0xFFFFFFFF:
                #lấy attribute type ($filename, $data)
                attributeType = getValueOfBufferByOffset(
                    buffer, 
                    attributeOffsetStarted + ATB_TYPE['hex'], 
                    ATB_TYPE['byte']
                )
                #lấy size của attribute
                attributeSize = getValueOfBufferByOffset(
                    buffer,
                    attributeOffsetStarted + ATB_ATTRIBUTE_SIZE['hex'], 
                    ATB_ATTRIBUTE_SIZE['byte']
                )
                #lấy giá trị resident của 1 attribute
                resident = getValueOfBufferByOffset(
                    buffer,
                    attributeOffsetStarted +  ATB_IS_RESIDENT['hex'], 
                    ATB_IS_RESIDENT['byte']
                )
                #lấy nơi bắt đầu của phần content trong attribute
                contentStarted = getValueOfBufferByOffset(
                    buffer,
                    attributeOffsetStarted +  ATB_STARTED_CONTENT['hex'], 
                    ATB_STARTED_CONTENT['byte']
                )
                #lấy phần content size
                contentSize = getValueOfBufferByOffset(
                    buffer,
                    attributeOffsetStarted + ATB_CONTENT_SIZE['hex'],
                    ATB_CONTENT_SIZE['byte']
                )
                #chuyển tới phần content để tiếp tục thực hiện lấy dữ liệu
                currentContent = contentStarted + attributeOffsetStarted
                if attributeType == FILENAME:
                    # print('FILENAME')

                    #lấy độ dài của tên attribute
                    nameLength = getValueOfBufferByOffset(
                        buffer,
                        currentContent + FN_NAME_LENGTH['hex'], 
                        FN_NAME_LENGTH['byte']
                    )
                    #lấy tên attribute
                    name = getBufferDataByOffset(
                        buffer, 
                        currentContent +  FN_NAME['hex'], 
                        FN_NAME['byte'] + nameLength * 2
                    ).decode('utf-16le')

                    #nếu name bắt đầu là $ VD ($MFT, $LOGFILE) ta không xử lý
                    if name.startswith('$'):
                        break
                    
                    #lấy vị trí index của folder
                    parentIndex = getValueOfBufferByOffset(buffer, currentContent, 6)

                    #thời gian tạo của attribute
                    createAt = getValueOfBufferByOffset(
                        buffer, 
                        currentContent +  FN_CREATE_AT['hex'], 
                        FN_CREATE_AT['byte']
                    )
                    #thời gian update gần nhất
                    updateAt = getValueOfBufferByOffset(
                        buffer, 
                        currentContent +  FN_UPDATE_AT['hex'], 
                        FN_UPDATE_AT['byte']
                    )
                elif attributeType == DATA:
                    # print('DATA')

                    #gán lại size thực tế của attribute
                    if resident == 0:
                        size = contentSize
                    else:
                        size = getValueOfBufferByOffset(buffer, attributeOffsetStarted + 0x30, 7)

                    #xử lý phần content
                    if name.endswith('.txt'): 
                        if resident == 0:
                            #resident: content sẽ bằng với kích thước lưu trữ trong MFT
                            rawContent = getBufferDataByOffset(buffer, currentContent, contentSize)
                        else:
                            #non-resident: phần content sẽ được dịch đến 1 cluster khác vì không đủ để lưu trong bảng MFT table

                            offsetRunList = getValueOfBufferByOffset(buffer, attributeOffsetStarted + 0x20, 2)
                            #lấy tổng số cluster lưu trữ content
                            totalCluster = getValueOfBufferByOffset(buffer, attributeOffsetStarted + offsetRunList + 1, 1)
                            #lấy cluster bắt đầu
                            clusterStarted = getValueOfBufferByOffset(buffer, attributeOffsetStarted + offsetRunList + 2, 2)
                            #đọc phần content
                            rawContent = getContentByCluster(self.file, clusterStarted, totalCluster, self.sc)
                        content = rawContent.decode('utf-8')
                    else:
                        #trường hợp không phải txt, ta lấy các application ứng với các hậu tố tương ứng
                        #để thông báo ứng dụng nào sẽ dùng để mở
                        try:
                            extension = document[f'.{name.split(".")[-1]}']
                        except KeyError:
                            extension = 'Not support'

                        content = f'Application to open is: {extension}'

                #ta sẽ tăng index và nơi bắt đầu offset lên, và tiếp tục lặp
                attributeOffsetStarted = attributeOffsetStarted + attributeSize
                index = index + attributeSize
            #khi đọc hết 1 MFT, ta kiểm tra name có phải $MFT, $LOGFILE, nếu không ta lưu chúng vào cây thư mục
            if not name.startswith('$'):

                #tạo đường dẫn đến cây thư mục cha
                if isFolder:
                    path = self.directory.add(parentIndex, sector / 2, name)
                else:
                    path = f'{self.directory.get(parentIndex)}\{name}'

                #tạo 1 tree node (thư mục hoặc tập tin con) (trong composite pattern) để add vào trong parent
                subFolder = createItem(isFolder, (name, size, content, path, createAt, updateAt))

                #tìm cha của nó (bằng việc lấy path)
                parentFolder = self.root.findByPath(self.directory.get(parentIndex))

                if parentFolder is not None:
                    #thêm vào node cha
                    parentFolder.add(subFolder)

            sector = sector + 2

    #hàm này dùng để tạo cây thư mục
    def generateTree(self):
        self.readPartitionRootSector()
        self.readMasterFileTable()
    #hàm này để build project với console
    def build(self):
        self.generateTree()
        console = Console(self.root)
        console.windowShell()
            
