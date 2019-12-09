#!/usr/bin/env python
import os
from settings import DONE_FILE, LOG_FILE, LOGGING_LEVEL, NOT_TO_SYNC, FOLDER_PAIRS
from MediaFireConnection import MediaFireConnection
from FtpConnection import FtpConnection
import properties as p
import sys
import logging
from ftptool import FTPHost, FTPFileProxy
import shutil
import urllib
import urllib.request as request
from contextlib import closing
import logging

global files_done

DESTINATION = 'downloads'

def save_line(*args):
    with open(FOLDER_PAIRS[1]['name'] +"_on_ftp.txt", "a+",  errors='replace') as f:
        f.write(",".join(args) + '\n')


def read_file(filename):
    with open(filename, "r",  errors='replace') as f:
        return f.readlines()


def correct(line):
    return line.replace('Ã¼', 'u').replace('Å', 'o').replace('Ã©', 'e').replace('Ã³','o').replace('Ã­','i').replace('Ã¡', 'a').replace('Å±','u').replace('Å?', 'o')


def ekezettelenit(line):
    return line.replace('ü', 'u').replace('ő', 'o').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á','a')


def get_file_names_ftp(name):
    filenames=[]
    ftp = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for (dirname, subdirs, files) in ftp.walk(name):
        for file in files:
            logging.debug("File: %s" % file)
            filepath = str(dirname).replace(name, "") + '/' + file
            save_line(filepath)
            filenames.append(filepath)
            logging.debug("Filepath: %s" % filepath)
        logging.debug("Subdirs: %s" % subdirs)
        logging.debug(str(dirname).replace(FOLDER_PAIRS[0]['ftp'], ""), "==>", ", ".join(files))
    return filenames


def get_mf_done_list(name):
    return dict((ekezettelenit(f.replace("\n", "").split(',')[0]).lower(), f.replace("\n", "").split(',')[0]) for f in read_file(name +"_on_mf.txt"))


def get_ftp_done_list(name):
    return dict((ekezettelenit(correct(f.replace("\n", ""))).lower(), f.replace("\n", "")) for f in read_file(name + "_on_ftp.txt"))


def get_from_ftp():
    ftp = get_ftp_done_list(FOLDER_PAIRS[1]['name'])
    mf = get_mf_done_list(FOLDER_PAIRS[1]['name'])
    logging.info("%d files on NAS (FTP)" % len(ftp))
    logging.info("%d files on Mediafire" % len(mf))
    to_download = [f for f in ftp.keys() if f not in mf.keys() and not f.startswith('vhs-r') and not f.startswith('r�gi vide�k') and not f.endswith('clpi')]
    logging.debug("%d to download" % len(to_download))

    #ftp_host = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for file_path in to_download:
        logging.debug("path:  %s" % file_path)
        file_path = ftp.get(file_path)
        logging.debug("file_path :  %s" % file_path)
        path_from = FOLDER_PAIRS[1]['ftp'] + file_path[:file_path.rfind(os.path.sep)]
        logging.debug("path_from :  %s" % path_from)
        #file_from = os.path.split(file_path) [-1]
        file_from = file_path[file_path.rfind(os.path.sep)+1:]
        logging.debug("file_from :  %s" % file_from)
        path_t = os.path.join(os.getcwd(), DESTINATION)
        logging.debug("path_t :  %s" % path_t)

        if os.name != 'posix':
            logging.debug("replacing /")
            path_from = path_from.replace("/", "\\")

        logging.debug("new path :  %s" % path_from)

        path_to = path_t + path_from
        logging.debug("path_to :  %s" % path_to)
        os.makedirs(path_to, exist_ok=True)
        #file_from = os.path.split(file_path)[-1]
        logging.info("FROM: %s" % os.path.join(path_from, file_from))
        logging.info("TO: %s" % os.path.join(path_to, file_from))
        #f = FTPFileProxy(ftp_host.ftp_obj, os.path.join(path_from, file_from))
        #f.download_to_file(os.path.join(path_to, file_from))
        try:
            with closing(request.urlopen('ftp://' + p.ftp_user + ':' + p.ftp_password +'@'  + p.private_ftp + "/" + urllib.parse.quote(os.path.join(path_from, file_from)))) as r:
                with open(os.path.join(path_to, file_from), 'wb') as f:
                    shutil.copyfileobj(r, f)
        except urllib.error.URLError:
            logging.error(file_path)
        logging.info("%s DONE" % file_from)


def upload_to_Mf():
    conn = MediaFireConnection()
    cwd = os.getcwd()
    path = os.path.join(cwd, DESTINATION)
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            logging.debug("root:  %s" % root)
            logging.debug("name:  %s" % name)
            path = os.path.join(root, name)

            mf_path = os.path.join(root.replace(cwd, "").replace(DESTINATION + os.path.sep, ""), name)
            mf_path = mf_path[:mf_path.rfind(os.path.sep)]
            mf_path = mf_path.replace("\\", "/")
            to_path = conn.ROOT + mf_path
            logging.debug("to_path:  %s" % to_path)
            # mf.upload_file("C:\\Users\\Laszlo.Szoboszlai\\Documents\personal\\git\\nas_to_mf\\", "mail_service.py", ROOT + "Test1/neww/neww2/nn", "Fppv99.py")
            conn.upload_file(root, name, to_path, name)





if __name__ == '__main__':
    logging.basicConfig(filename="", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    #get_from_ftp()
    upload_to_Mf()
    #ftp = get_ftp_done_list(FOLDER_PAIRS[1]['name'])
    #mf = get_mf_done_list(FOLDER_PAIRS[1]['name'])

    #for i in mf:
    #    print(i)
    #files_ftp = get_file_names_ftp(FOLDER_PAIRS[1]['ftp'])
    #print("done")
    #for fn in files_ftp:
    #    print(fn)
