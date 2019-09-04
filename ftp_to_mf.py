#!/usr/bin/env python
import os
from settings import DONE_FILE, LOG_FILE, LOGGING_LEVEL, NOT_TO_SYNC, FOLDER_PAIRS
from MediaFireConnection import MediaFireConnection
from FtpConnection import FtpConnection
import properties as p
import sys
import logging
from ftptool import FTPHost

global files_done

def main():
    ftp = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for (dirname, subdirs, files) in ftp.walk(FOLDER_PAIRS[0]['ftp']):
        print(str(dirname).replace(FOLDER_PAIRS[0]['ftp'], ""), "==>", ", ".join(files))


if __name__ == '__main__':
    main()