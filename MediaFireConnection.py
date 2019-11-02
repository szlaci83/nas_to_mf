from mediafire import (MediaFireApi, MediaFireUploader)
import properties
import os
import logging
import utils
from pprint import pprint
from mediafire.client import (MediaFireClient,File,
                              Folder, ResourceNotFoundError)
from settings import DONE_FILE, LOG_FILE, LOGGING_LEVEL, NOT_TO_SYNC, FOLDER_PAIRS

Kepek = 0
Kamera = 1

FOLDER = Kamera


ROOT = 'mf:/' + FOLDER_PAIRS[FOLDER]['name']+'/'
files_done = []


def save_line(*args):
    with open(FOLDER_PAIRS[FOLDER]['name'] +"_on_mf.txt", "a+", encoding="utf-8") as f:
        f.write(",".join(args) + '\n')
    f.close()


class MediaFireConnection:
    def __init__(self, api=MediaFireApi(), email=properties.email, password=properties.password,app_id=properties.app_id):
        self.__api = api
        self.session = api.user_get_session_token(email=email,
                                                  password=password,
                                                  app_id=app_id)
        self.__api.session = self.session
        self.uploader = MediaFireUploader(api)
        self.client = MediaFireClient()
        self.client.login(email=email,
                                                  password=password,
                                                  app_id=app_id)

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
        try:
            file = open(os.path.join(source_path, source_filename), 'rb')
            result = self.uploader.upload(file, target_filename, path=target_path)
        except IsADirectoryError:
            pass
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

    def get_content(self, path):
        logging.info("Processing path: %s" % path)
        try:
            for item in self.client.get_folder_contents_iter(path):
                if type(item) is File:
                    file_path = (path + item['filename']).replace(ROOT, "")
                    logging.info("Processsing file: %s" % file_path)
                    save_line(file_path, item['hash'], item['size'])
                elif type(item) is Folder:
                    self.get_content(path + item['name'] +'/')
        except ResourceNotFoundError as rne:
           logging.error("Resource NOT Found: %s", exc_info=rne)
           return
        except Exception as e:
           logging.error("Error: %s",  exc_info=e)


def save_file_list():
    mf = MediaFireConnection()
    mf.get_content(ROOT)
    print("done")


def example2():
    mf = MediaFireConnection()
    for i in mf.client.get_folder_contents_iter(ROOT+ 'Zoe szuletes'):
        pprint(i)


if __name__ == '__main__':
    logging.basicConfig(filename="", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    save_file_list()
    #example2()

