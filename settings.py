import logging

DONE_FILE = 'uploaded.mf'
LOG_FILE = 'mf_sync.log'
NOT_TO_SYNC = [DONE_FILE, LOG_FILE]

LOGGING_LEVEL = logging.DEBUG
FTP_DIR = ''
MF_DIR = ''

FOLDER_PAIRS = [
    {"ftp": "/HomeMade/Kepek/",
     "mf": "Kepek"
     },
    {"ftp": "/HomeMade/Kamera/",
     "mf": "Kamera"
     }
]


