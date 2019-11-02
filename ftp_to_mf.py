#!/usr/bin/env python
import os
from settings import DONE_FILE, LOG_FILE, LOGGING_LEVEL, NOT_TO_SYNC, FOLDER_PAIRS
from MediaFireConnection import MediaFireConnection
from FtpConnection import FtpConnection
import properties as p
import sys
import logging
from ftptool import FTPHost, FTPFileProxy

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
    return [ekezettelenit(f.replace("\n", "").split(',')[0]).lower() for f in read_file(name +"_on_mf.txt")]


def get_ftp_done_list(name):
    return [ekezettelenit(correct(f.replace("\n", ""))).lower() for f in read_file(name + "_on_ftp.txt")]


def diff():
    ftp = get_ftp_done_list(FOLDER_PAIRS[1]['name'])
    mf = get_mf_done_list(FOLDER_PAIRS[1]['name'])
    print(len(ftp))
    print(len(mf))
    # for i in done_ftp:
    #     print(i)
    # for i in done_mf:
    #     print(i)
    to_download = [f for f in ftp if f not in mf and not f.startswith('vhs-rol') and not f.startswith('regi videok')]
    ftp = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for file_path in to_download:
        path_from = FOLDER_PAIRS[1]['ftp']
        file_from = os.path.split(file_path) [-1]
        print(path_from)
        print(file_from)
        print(os.getcwd())
        path_t = os.path.join(os.getcwd(), DESTINATION)
        print(path_t)
        print(path_from.replace("/", "\\"))
        path_to = path_t + path_from.replace("/", "\\")
        print(path_to)
        os.makedirs(path_to, exist_ok=True)
        file_from = os.path.split(file_path)[-1]

        f = FTPFileProxy(ftp.ftp_obj, os.path.join(path_from, file_from))
        f.download_to_file(os.path.join(path_to, file_from))

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
