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
            print(file)
            filepath = str(dirname).replace(name, "") + '/' + file
            save_line(filepath)
            filenames.append(filepath)
            print(filepath)
        #print(subdirs)
        #print(str(dirname).replace(FOLDER_PAIRS[0]['ftp'], ""), "==>", ", ".join(files))
    return filenames


def get_mf_done_list(name):
    return dict((ekezettelenit(f.replace("\n", "").split(',')[0]).lower(), f.replace("\n", "").split(',')[0]) for f in read_file(name +"_on_mf.txt"))


def get_ftp_done_list(name):
    return dict((ekezettelenit(correct(f.replace("\n", ""))).lower(), f.replace("\n", "")) for f in read_file(name + "_on_ftp.txt"))


def diff():
    ftp = get_ftp_done_list(FOLDER_PAIRS[1]['name'])
    mf = get_mf_done_list(FOLDER_PAIRS[1]['name'])
    print(len(ftp))
    print(len(mf))
    # for i in done_ftp:
    #     print(i)
    # for i in done_mf:
    #     print(i)
    to_download = [f for f in ftp.keys() if f not in mf.keys() and not f.startswith('vhs-r') and not f.startswith('r�gi vide�k') and not f.endswith('clpi')]
    ftp_host = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for file_path in to_download:
        print(file_path)
        file_path = ftp.get(file_path)
        path_from = FOLDER_PAIRS[1]['ftp'] + file_path[:file_path.rfind('/')]
        #file_from = os.path.split(file_path) [-1]
        file_from=file_path[file_path.rfind('/')+1:]
        print(path_from)
        print(file_path)

        print(file_from)
        print(os.getcwd())
        path_t = os.path.join(os.getcwd(), DESTINATION)
        print(path_t)
        if os.name != 'posix':
            path_from = path_from.replace("/", "\\")
        print(path_from.replace("/", "\\"))
        path_to = path_t + path_from
        print(path_to)
        os.makedirs(path_to, exist_ok=True)
        #file_from = os.path.split(file_path)[-1]

        print("FROM: " +  os.path.join(path_from, file_from))
        print("TO: " + os.path.join(path_to, file_from)) 
        #f = FTPFileProxy(ftp_host.ftp_obj, os.path.join(path_from, file_from))
        #f.download_to_file(os.path.join(path_to, file_from))
        with closing(request.urlopen('ftp://' + p.ftp_user + ':' + p.ftp_password +'@'  + p.private_ftp + "/" + urllib.parse.quote(os.path.join(path_from, file_from)))) as r:
            with open(os.path.join(path_to, file_from), 'wb') as f:
                shutil.copyfileobj(r, f)

    #    print(i)




if __name__ == '__main__':
    #get_file_names_ftp("")
    diff()
    #ftp = get_ftp_done_list(FOLDER_PAIRS[1]['name'])
    #mf = get_mf_done_list(FOLDER_PAIRS[1]['name'])

    #for i in mf:
    #    print(i)
    #files_ftp = get_file_names_ftp(FOLDER_PAIRS[1]['ftp'])
    #print("done")
    #for fn in files_ftp:
    #    print(fn)
