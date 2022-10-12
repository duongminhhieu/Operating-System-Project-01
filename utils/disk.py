import os
from utils.directory import Directory
from fileHandler.NtfsFile import NtfsFile
from fileHandler.Fat32File import FATVolume
from pattern.composite import *

#class này viết để đọc ổ đĩa
class Disk:
    def __init__(self):
        #các platform cho phép handle
        self.platformName = os.name
        if self.platformName == 'nt':
            print('===============you are running on nt window===============')
        elif self.platformName == 'posix':
            print('===============you are running on posix===============')
        else:
            raise Exception(f'we are not implement in {self.platformName} platform')
    
    #hàm chọn ổ đĩa để tiến hành xử lý
    def selectDiskPath(self):
        diskPath = input('type your disk path: ')

        if self.platformName == 'nt':
            self.diskPath = f'\\\\.\\{diskPath}:'
        else:
            self.diskPath = diskPath
            

    #hàm setup đọc file, trả về 1 object file để có thể xử lý trên sector
    def generateDiskFile(self):
        diskFile = os.open(self.diskPath, os.O_BINARY)
        diskObjectFile = os.fdopen(diskFile, 'rb')
        
        return diskObjectFile

    #tạo 1 NTFS file container để xử lý file vừa đọc
    def generateNTFSFile(self, file, directory):
        root = CFolder(self.diskPath[-2], f'{self.diskPath[-2]}:')
        ntfsFile = NtfsFile(file, root, directory)
        return ntfsFile
    
    #tạo 1 FAT32 file container để xử lý file vừa đọc
    def generateFAT32File(self, file, directory):
        root = CFolder(self.diskPath[-2], f'{self.diskPath[-2]}:')
        fatFile = FATVolume(file, root, directory)
        return fatFile

    #tạo 1 directory để lưu trữ các parent index của 1 folder hoặc file
    def generateDirectory(self):
        directory = Directory(f'{self.diskPath[-2]}:')
        return directory


