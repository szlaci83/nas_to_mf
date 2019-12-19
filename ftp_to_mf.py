#!/usr/bin/env python
import os
from settings import  LOGGING_LEVEL, NOT_TO_SYNC, FOLDER_PAIRS,DESTINATION, DESTINATION_FULL
import MediaFireConnection as mf
import properties as p
import logging
from ftptool import FTPHost
import shutil
import urllib
import urllib.request as request
from contextlib import closing
import logging
from utils import ekezettelenit, correct
from db_handler import MongoUtils

mongo = MongoUtils()

# TODO: create a class with mf and  mondgo instances and move mf_filelist_to_mongo() from Mfconnection.py
def get_file_names_ftp(ftp_root,db, coll_name):
    col = db[coll_name]

    ftp = FTPHost.connect(p.private_ftp, user=p.ftp_user, password=p.ftp_password)
    for (dirname, subdirs, files) in ftp.walk(ftp_root):
        for file in files:
            logging.debug("File: %s" % file)
            file_path = (str(dirname) + '/' + file)
            corrected_filepath = correct(ekezettelenit(file_path).replace("//", "/"))
            existing = mongo.find_by_ftp_path(corrected_filepath, coll_name=coll_name)
            item = {'ftp_path': corrected_filepath, 'original_ftp_path': file_path}
            if existing:
                logging.debug("updating Mongo")
                mongo.update_item(coll_name=coll_name, item=existing, properties=item)
            else:
                logging.debug("inserting into Mongo")
                mongo.insert_one(item, coll_name=coll_name)
            logging.debug("Added: %s" % item)
        logging.debug("Subdirs: %s" % subdirs)
    return



#TODO: Thumbs.db-t kihagyni
def get_one_from_ftp(item, to_path=os.path.join(os.getcwd(), DESTINATION)):
    logging.debug(item["_id"])
    from_path = item['original_ftp_path']
    logging.debug("path_from :  %s" % from_path)
    path_to = from_path.replace(item['ftp_root'], to_path)
    if os.name != 'posix':
        logging.debug("replacing /")
        path_to = path_to.replace("/", "\\")
    logging.debug("path_to :  %s" % path_to)
    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    try:
        with closing(request.urlopen(
                'ftp://' + p.ftp_user + ':' + p.ftp_password + '@' + p.private_ftp + "/" + urllib.parse.quote(
                        from_path))) as source:
            with open(path_to, 'wb') as dest:
                shutil.copyfileobj(source, dest)
    except urllib.error.URLError:
        logging.error(from_path)
        return False
    logging.info("%s DONE" % from_path)
    return path_to


def upload_file_to_mf(file_path):
    print(file_path)
    Kepek = FOLDER_PAIRS[0]['name']
    root = os.path.dirname(file_path)
    name = os.path.basename(file_path)
    mf_path = os.path.join(Kepek, root.replace(DESTINATION_FULL, ""))
    # mf_path = mf_path[:mf_path.rfind(os.path.sep)]
    mf_path = mf_path.replace("\\", "/")
    conn = mf.MediaFireConnection()
    to_path = "/" + mf_path
    logging.debug("MF______to_path:  %s" % to_path)
    # logging.debug(root, urllib.parse.quote(name), to_path, urllib.parse.quote(name))

    print("------------------------------------------")
    print(root)
    print(name)
    print(to_path)
    print(urllib.parse.quote(name))
    print("------------------------------------------")

    result = conn.upload_file(root, name, to_path, urllib.parse.quote(name))
    result["path"] = "mf:" + to_path
    return result

def ftp_filelist_to_mongo():
    for folder_pair in FOLDER_PAIRS:
        get_file_names_ftp(mongo.db, folder_pair['ftp'], folder_pair['Name'])


def process_all_coll_missing_in_mf(force_download=False, keep_downloaded=True):
    for folder_pair in FOLDER_PAIRS:
        process_missing_in_mf(folder_pair['name'], force_download, keep_downloaded)


def process_missing_in_mf(coll, force_download=False, keep_downloaded=True):
    coll = MongoUtils(coll)
    cursor = coll.missing_from_mf()
    try:
        for missing in cursor:
            if not any(missing['ftp_path'].endswith(i) for i in NOT_TO_SYNC):
                local_path =missing.get('local_path', None)
                if not local_path or force_download:
                    local_path = get_one_from_ftp(missing)
                    if local_path and keep_downloaded:
                        coll.update_item(missing, {"local_path": local_path})
                mf = upload_file_to_mf(local_path)
                print(mf)
                coll.update_item(missing, {"mf": mf})
    except Exception as e:
        logging.error(e)
    finally:
        cursor.close()

def main():
    # TODO: fill rootpaths (call db_handler method?)
    #ftp_filelist_to_mongo()
    #mf.mf_filelist_to_mongo()
    process_missing_in_mf(FOLDER_PAIRS[0]['name'], force_download=True)


if __name__ == '__main__':
    logging.basicConfig(filename="", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
    main()