from msilib.schema import Directory
from utils.disk import Disk
from utils.buffer import *
from fileHandler.Fat32File import *

def main():
    try:
        #init root path for folder
        disk = Disk()
        #generate object file for disk driver
        disk.selectDiskPath()
        file = disk.generateDiskFile()



        #main
        #generate directory
        directory = disk.generateDirectory()

        #check ntfs disk or fat32 
        bootsec_buffer = getBufferDataBySector(file, 0, 1)
        fat32_volfs = getBufferDataByOffset(bootsec_buffer, 0x52, 8)
        ntfs_volfs = getBufferDataByOffset(bootsec_buffer, 3, 4)

        if b'FAT32' in fat32_volfs:
            fat32File = disk.generateFAT32File(file, directory)
            #demo handle PARTITION BOOT SECTOR
            print('\n\n----------------------FAT32----------------------')
            print('--------------PARTITION BOOT SECTOR--------------\n')
            fat32File.readPartitionRootSector()
        elif b'NTFS' in ntfs_volfs:
            #create new tnfs file system
            ntfsFile = disk.generateNTFSFile(file, directory)
            #demo handle PARTITION BOOT SECTOR
            print('\n\n--------------NTFS--------------')
            print('\n\n--------------PARTITION BOOT SECTOR--------------')
            ntfsFile.readPartitionRootSector()
            print('\n\nPress enter to switch to READ MASTER FILE TABLE function demo')
            input()

            #demo handle READ MASTER FILE TABLE
            #build DIRECTORY TREE by console
            ntfsFile.build()
        else: 
            raise AttributeError('Filesystem not supported')

        

        

    except:
        pass
if __name__ == '__main__':
    main()