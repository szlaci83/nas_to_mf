import logging

DONE_FILE = 'uploaded.mf'
LOG_FILE = 'mf_sync.log'
NOT_TO_SYNC = [DONE_FILE, LOG_FILE]

LOGGING_LEVEL = logging.DEBUG
FTP_DIR = ''
MF_DIR = ''

FOLDER_PAIRS = [
    {"ftp": "/Test/Kepek/",
     "mf": "mf:/Kepek/",
     "name": 'Kepek'
     },
    {"ftp": "/Test/Kamera/",
     "mf": "mf:/Kamera/",
     "name": 'Kamera'
     }
]


