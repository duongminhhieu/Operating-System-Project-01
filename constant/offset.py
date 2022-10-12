#PDS: PARTITION BOOT SECTOR
PDS_SECTOR_SIZE = {'hex': 0x0B, 'byte': 2}
PDS_SECTOR_CLUSTER = {'hex': 0x0D, 'byte': 1}
PDS_TOTAL_SECTOR = {'hex': 0x28, 'byte': 8}
PDS_STARTED_MFT_CLUSTER = {'hex': 0x30, 'byte': 8}
PDS_MIRROR_MFT_CLUSTER = {'hex': 0x38, 'byte': 8}

#MFT: MASTER FILE TABLE
MFT_SIGNATURE = {'hex': 0x00, 'byte': 4}
MFT_STARTED_ATTRIBUTE = {'hex': 0x14, 'byte': 2}
MFT_ATTRIBUTE_TYPE = {'hex': 0x16, 'byte': 2}

#ATB: ATTRIBUTE
ATB_TYPE = {'hex': 0x00, 'byte': 4}
ATB_ATTRIBUTE_SIZE = {'hex': 0x04, 'byte': 4}
ATB_IS_RESIDENT = {'hex': 0x08, 'byte': 1}
ATB_ATTRIBUTE_NAME = {'hex': 0x0A, 'byte': 2}
ATB_CONTENT_SIZE = {'hex': 0x10, 'byte': 4}
ATB_STARTED_CONTENT = {'hex': 0x14, 'byte': 2}

#FN: FILENAME
FN_PARENT_ADDRESS = {'hex': 0x00, 'byte': 8}
FN_CREATE_AT = {'hex': 0x08, 'byte': 8}
FN_UPDATE_AT = {'hex': 0x20, 'byte': 8}
FN_NAME = {'hex': 0x42, 'byte': 0}
FN_NAME_LENGTH = {'hex': 0x40, 'byte': 1}