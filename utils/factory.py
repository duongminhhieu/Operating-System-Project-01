from pattern.composite import *

#đây là hàm để tạo folder hoặc file dựa vào isFolder khi đọc ở 2 byte offset 16 của 1 MFT
def createItem(isFolder, data):
    (name, size, content, path, createAt, updateAt) = data

    if isFolder:
        return CFolder(name, path, createAt, updateAt)
    else:
        return CFile(name, path, content, size, createAt, updateAt)
