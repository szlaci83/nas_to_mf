from mediafire import (MediaFireApi, MediaFireUploader)
import properties
import os
from pprint import pprint
from mediafire.client import (MediaFireClient,
                              Folder, ResourceNotFoundError)


class MediaFireConnection:
    def __init__(self, api=MediaFireApi(), email=properties.email, password=properties.password,
                 app_id=properties.app_id):
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


def example():
    mf = MediaFireConnection()
    pprint(mf.get_user_info())


if __name__ == '__main__':
    example()


