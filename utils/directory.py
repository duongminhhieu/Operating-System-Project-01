#class này khai báo cho việc lưu trữ thư mục cha của 1 file hoặc folder
#vì NTFS cung cấp parentIndex nên ta sẽ sử dụng 1 dictionary để lưu trữ dạng
#{'parentIndex': 'c:/folder/...', ...} 
# VD: {'1': 'c:/folder', '2': 'c:/folder/folder1', ...}
class Directory: 
    def __init__(self, default):
        self.default = default
        self.listOfDirectory = {}

    #thêm 1 thư mục vào list directory với index là index của thư mục con, parentIndex là index của thư mục cha của nó
    def add(self, parentIndex, index, name)->None:
        try:
            #nếu hiện đang không có thư mục cha của 1 Node con nào đó, ta sẽ set thư mục cha là defaut
            result = self.listOfDirectory[str(parentIndex)]
        except KeyError:
            self.listOfDirectory[str(parentIndex)] = self.default

        #nếu thư mục con là thư mục cha (chỉ xảy ra với thư mục . (NODE để đi ra ngoài ổ đĩa)), ta sẽ không lưu trữ
        if int(index) == parentIndex:
            return self.default

        #thêm vào 1 thư mục
        self.listOfDirectory[str(int(index))] = f'{self.listOfDirectory[str(parentIndex)]}\{name}'

        result = self.listOfDirectory[str(int(index))]
        return result

    #lấy thư mục cha
    def get(self, parentIndex):
        try:
            result = self.listOfDirectory[str(parentIndex)]
        except KeyError:
            self.listOfDirectory[str(parentIndex)] = self.default

        result = self.listOfDirectory[str(parentIndex)]
        return result
