# Operating-System-Project-01
Xây dựng chương trình máy tính (sử dụng ngôn ngữ tùy ý) nhằm đọc các thông tin trên phân vùng FAT32 và NTFS 


Xây dựng chương trình máy tính (sử dụng ngôn ngữ tùy ý) nhằm đọc các thông tin trên phân vùng FAT32 và NTFS như sau: 

1.	Đọc các thông tin chi tiết của một phân vùng:
-	Gợi ý: Đọc các thông tin được mô tả trong Boot Sector (đối với phân vùng FAT32) hoặc Partition Boot Sector (đối với phân vùng NTFS) 


2.	Hiển thị thông tin cây thư mục của phân vùng


-	Chương trình hiển thị cây thư mục gốc gồm tên tập tin / thư mục, trạng thái, kích thước (nếu có), chỉ số sector lưu trữ trên đĩa cứng


-	Khi truy xuất thông tin trên cây thư mục: chương trình hiển thị thông tin là nội dung tập tin đối với tập tin có phần mở rộng là txt, các loại tập tin khác hiển thị thông báo dùng phần mềm tương thích để đọc nội dung. Trường hợp đối tượng là thư mục, chương trình cho phép hiển thị cây thư mục con (thông tin hiển thị tương tự như cây thư mục gốc) 


-	Gợi ý: Để đọc các thông tin trên, đọc và phân tích bảng RDET + Bảng FAT đối với hệ thống FAT32, hoặc Master file table đối với NTFS

Tham khảo về NTFS: 	http://ntfs.com/ntfs_basics.htm	 
