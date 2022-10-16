from abc import ABC, abstractmethod

#đây là interface của 1 tree root được mô phỏng và sử dụng composite pattern
class CItem(ABC):
    @property
    def name(self):
        '''
            name of this folder or file
        '''

    @property
    def name(self):
        '''
            name of this folder or file
        '''

    def add(self, item) -> None:
        '''
            add file on folder
        '''

    @abstractmethod
    def findByPath(self, path) -> None:
        '''
            file folder or file by path
        '''
    @abstractmethod
    def getSize(self) -> int:
        '''
            get size of file or folder
        '''
    @abstractmethod
    def print(self) -> None:
        '''
            print information of file or folder
        '''
    def printContent(self):
        '''
            print content
        '''
        
    def printDetail(self): 
        '''
            print detail
        '''
    def printCurrentItem(self):
        '''
            print current item
        '''

#đây là class lưu trữ con là dạng file
class CFile(CItem):
    #override name property
    name = None
    path = None
    def __init__(self, name, path, content, size, createAt, updateAt):
        #init default size for file
        #constructor
        self.name = name
        self.path = path
        self.content = content
        self.size = size
        self.createAt = createAt
        self.updateAt = updateAt



    def findByPath(self, path) -> None:
        if path == self.path:
            return self
        return None

    def getSize(self) -> int:
        return self.size

    def print(self, space) -> None:
        print(f'{space}Name: {self.name}, size: {self.size}')
        
    def printContent(self):
        print(self.content)
        
    def printDetail(self): 
        print(f'FileName: {self.name}')
        print(f'Size: {self.size}')
        print(f'CreateAt: {self.createAt}')
        print(f'UpdateAt: {self.updateAt}')

    def printCurrentItem(self):
        print(self.name)

#đây là class được lưu trữ dưới dạng folder
class CFolder(CItem):
    name = None
    path = None
    def __init__(self, name, path, createAt = 0, updateAt = 0) -> None:
        #init for list of subitem
        self.subItem:list[CItem] = []
        self.name = name
        self.path = path
        self.size = 0
        self.createAt = createAt
        self.updateAt = updateAt

    def add(self, item:CItem) -> None:
        self.subItem.append(item)

    #tìm các Node con bằng path
    def findByPath(self, path) -> None:
        result = None
        if self.path == path:
            return self
        
        for item in self.subItem:
            if item.path == path:
                return item

            result = item.findByPath(path)
            if result:
                return result
        return None

    #lấy size = totalSize(child) (như 1 lời thực hiện duyệt cây)
    def getSize(self) -> int:
        size = 0
        for item in self.subItem:
            size = size + item.getSize()
        return size

    #chỉ print các phần tử trong 1 cấp thư mục
    def printCurrentItem(self):
        for item in self.subItem:
            print(item.name)

    #size thực của 1 folder là kích thước tổng tập tin con nó đang lưu trữ
    def print(self, space='----') -> None:
        
        print(f'{space}Folder: {self.name}, size: {self.getSize()}')

        for item in self.subItem:
            item.print(space*2)



########################################################

from abc import ABCMeta, abstractmethod


class AbstractVolume(metaclass=ABCMeta):
    @property
    @abstractmethod
    def root_directory(self):
        """
        Con trỏ đến thư mục gốc của volume
        """
        pass
    
    @property
    @abstractmethod
    def size(self) -> int:
        """
        Kích thước (byte) của volume
        """
        pass
    
    @property
    @abstractmethod
    def volume_label(self) -> str:
        """
        Nhãn (tên) của volume
        """
        pass

    @property
    @abstractmethod
    def file_object(self):
        """
        Kích thước (byte) của volume
        """
        pass

class AbstractEntry(metaclass=ABCMeta):
    """
    Lớp đối tượng thể hiện một entry
    """
    @property
    @abstractmethod
    def path(self) -> str:
        """
        Đường dẫn đến entry
        """
        pass

    @property
    @abstractmethod
    def volume(self) -> AbstractVolume:
        """
        Con trỏ đến volume chứa entry này (để truy cập vào bảng FAT/MFT và duyệt các cluster)
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tên của thư mục này
        """
        pass

    @property
    @abstractmethod
    def attr(self) -> list:
        """
        Tên của thư mục này
        """
        pass

    @abstractmethod
    def describe_attr(self) -> str:
        """
        Diễn giải các thuộc tính dưới dạng chuỗi
        """
        pass

    @property
    @abstractmethod
    def sectors(self) -> list:
        """
        Là mảng các chỉ số sector chứa dữ liệu nhị phân của SDET/RDET của thư mục này
        """
        pass

class AbstractDirectory(AbstractEntry):
    @property
    @abstractmethod
    def subentries(self) -> list:
        """
        Mảng của các subentries (file/subdirectory) của thư mục này.
        """
        pass

    @abstractmethod
    def build_tree(self):
        """
        Hàm để dựng được danh sách các subentry tương ứng với thư mục này (dữ liệu là từ SDET/RDET của thư mục). Danh sách này lưu vào mảng subentries[].
        """
        pass


class AbstractFile(AbstractEntry):
    @property
    @abstractmethod
    def size(self) -> int:
        """
        Kích thước (byte) của file
        """
        pass

    @abstractmethod
    def dump_binary_data(self) -> bytes:
        pass