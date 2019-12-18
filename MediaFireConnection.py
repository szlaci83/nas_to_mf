from mediafire import (MediaFireApi, MediaFireUploader)
import properties
import os
import logging
from mediafire.client import (MediaFireClient,File,
                              Folder, ResourceNotFoundError)
from settings import  LOGGING_LEVEL, FOLDER_PAIRS, DATABASE_NAME
from utils import ekezettelenit
from db_handler import MongoUtils

ROOT = 'mf:/'


class MediaFireConnection:
    def __init__(self, api=MediaFireApi(), email=properties.email, password=properties.password, app_id=properties.app_id):
        self.__api = api
        self.session = api.user_get_session_token(email=email,
                                                  password=password,
                                                  app_id=app_id)
        self.__api.session = self.session
        self.uploader = MediaFireUploader(self.__api)
        self.client = MediaFireClient()
        self.client.login(email=email,
                                                  password=password,
                                                  app_id=app_id)
        self.ROOT = ROOT

    def get_info(self):
        res = self.__api.system_get_info()
        return res

    def get_user_info(self):
        res = self.__api.user_get_info()
        return res

    def get_file_info(self, uploadresult):
        return self.__api.file_get_info(uploadresult.quickkey)['result']

    def upload_file(self, source_path, source_filename, target_path, target_filename):
        result = None
        while not result:
            try:
                result = self.client.upload_file(os.path.join(source_path, source_filename), target_path + "/" + target_filename)
            except IsADirectoryError:
                result = None# Todo: idk why we need this...
            except ResourceNotFoundError:
                logging.info("%s path not found, lets create it." % target_path)
                self.client.create_folder(target_path, recursive=True)
        result = self.client.get_resource_by_key(result.quickkey)
        return result

    def do_ls(self, client, args):
        """List directory"""

        for item in client.get_folder_contents_iter(args.uri):
            # privacy flag
            if item['privacy'] == 'public':
                item['pf'] = '@'
            else:
                item['pf'] = '-'

            if isinstance(item, Folder):
                # type flag
                item['tf'] = 'd'
                item['key'] = item['folderkey']
                item['size'] = ''
            else:
                item['tf'] = '-'
                item['key'] = item['quickkey']
                item['name'] = item['filename']

            print("{tf}{pf} {key:>15} {size:>10} {created} {name}".format(**item))

        return True

    def to_mongo(self, db, folder_pair):
        path = folder_pair['mf']
        ftp_root = folder_pair['ftp']
        coll_name = folder_pair['name']

        logging.info("Processing path: %s" % path)
        try:
            for item in self.client.get_folder_contents_iter(path):
                if type(item) is File:
                    mf_path = (path + item['filename'])
                    ftp_path = (ftp_root + item['filename'])
                    logging.debug("Checking in Mongo for %s  ==>  %s" % (mf_path, ftp_path))
                    existing = db.find_by_ftp_path(ftp_path, coll_name=coll_name)
                    if existing:
                        logging.debug("updating Mongo")
                        item['path'] = path
                        db.update_item(existing, properties={"mf": item}, coll_name=coll_name)
                    else:
                        logging.debug("inserting into Mongo")
                        item['path'] = path
                        db.insert_one({"mf": item}, coll_name=coll_name)
                elif type(item) is Folder:
                    self.to_mongo(db, {
                        "mf": path + item['name'] + '/',
                        "ftp": folder_pair['ftp'] + item['name'] + '/',
                        "name": coll_name
                    })
        except ResourceNotFoundError as rne:
            logging.error("Resource NOT Found: %s", exc_info=rne)
            return
        except Exception as e:
            logging.error("Error: %s", exc_info=e)



def mf_filelist_to_mongo():
    for folder_pair in FOLDER_PAIRS:
        mongo = MongoUtils()
        mf = MediaFireConnection()
        mf.to_mongo(mongo, folder_pair=folder_pair)


if __name__ == '__main__':
    logging.basicConfig(filename="", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
    mf_filelist_to_mongo()

