import logging
import os

NOT_TO_SYNC = ["Thumbs.db"]

DATABASE_HOST = "192.168.0.150"
DATABASE_NAME = "sync"

LOCAL_ROOT = "C:\\Users\\Laszlo.Szoboszlai\\Documents\\personal\\git\\nas_to_mf\\"
DESTINATION = 'downloads\\'
DESTINATION_FULL = os.path.join(LOCAL_ROOT, DESTINATION)
Kepek = "Kepek"

LOGGING_LEVEL = logging.DEBUG
FTP_DIR = ''
MF_DIR = ''

FOLDER_PAIRS = [
    {"ftp": "/HomeMade/Kepek/",
     "mf": "mf:/Kepek/",
     "local": 'C:\\temp\\',
     "name": 'Kepek'
     },
    {"ftp": "/HomeMade/Kamera/",
     "mf": "mf:/Kamera/",
     "local": 'C:\\temp\\',
     "name": 'Kamera'
     }
]


if __name__ == '__main__':
    print(locals())