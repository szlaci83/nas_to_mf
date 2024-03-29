from utils import ultimate_replacer
from utils import ekezettelenit, correct
from settings import DATABASE_NAME, DATABASE_HOST, FOLDER_PAIRS
import pymongo
import datetime

class MongoDB:
    class __impl:
        def __init__(self):
            self.host = DATABASE_HOST
            self.connection = pymongo.MongoClient(self.host)

        def get_singleton_id(self):
            """ Just an example method that returns Singleton instance's ID """
            return id(self)
    __instance = __impl()

    @staticmethod
    def close():
        MongoDB.__instance.connection.close()

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class MongoUtils:
    def __init__(self, coll_name="", db_name=DATABASE_NAME):
        self.host = MongoDB().host
        self.db_name = db_name
        self.conn = MongoDB().connection
        self.db = self.conn[self.db_name]
        self.coll = coll_name

    def get_all(self, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find()


    def add_root_paths(self, item, folder_pair,  coll_name=None):
        coll = coll_name or self.coll
        self.db[coll].update_one({"_id": item["_id"]}, {"$set": {"mf_root": folder_pair['mf'], 'ftp_root': folder_pair['ftp']}})

    def correct_ftp_path(self, to_correct, coll_name=None, delete_none=True):
        coll = coll_name or self.coll
        for item in self.db[coll].find():
            try:
                corrected = ultimate_replacer(item[to_correct])
                if item[to_correct] != corrected:
                    print(corrected)
                    self.db[coll].update_one({"_id": item["_id"]}, {"$set": {to_correct: corrected}})
            except KeyError:
                if delete_none:
                    self.db[coll].delete_one({"_id": item["_id"]})

    def missing_from_ftp(self, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find({"mf": {'$ne': None}, "ftp_path": {'$eq': None}})

    def missing_from_mf(self, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find({"mf": {"$eq": None}, "ftp_path": {"$ne": None}}, no_cursor_timeout=True)

    def missing_from_local(self, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find({"local_path": {"$eq": None}, "ftp_path": {"$ne": None}}, no_cursor_timeout=True)

    def update_item(self, item, properties, coll_name=None):
        coll = coll_name or self.coll
        self.db[coll].update_one({"_id": item["_id"]}, {"$set": properties})

    def remove_missing_from_ftp(self, coll_name=None):
        coll = coll_name or self.coll
        for missing in self.db[coll].find({"mf": {'$ne': None}, "ftp_path": {'$eq': None}}):
            self.db[coll].delete_one({"_id": missing["_id"]})

    def find_by_ftp_path(self, corrected_filepath, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find_one({'ftp_path': corrected_filepath})

    def find_by_local_path(self, corrected_filepath, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find_one({'local_path': corrected_filepath})

    def insert_one(self, record, coll_name=None):
        coll = coll_name or self.coll
        self.db[coll].insert_one(record)

    def get_by_mf_mod_date(self, n_days, coll_name=None):
        coll = coll_name or self.coll
        return self.db[coll].find({'mf.updated_at' :{"$gt": datetime.datetime.now() - datetime.timedelta(days=n_days)}}, no_cursor_timeout=True)

def info():

    # TODO: get name from param
    m = MongoUtils("Kepek")
    print("Using host: %s, db: %s, collection: %s" % (m.host,  m.db_name, m.coll))
    print("Missing from Mediafire: %d" % len(list(m.missing_from_mf())))
    print("Missing from NAS: %d" % len(list(m.missing_from_ftp())))
    # TODO : missing from local, total ..

    from pprint import pprint as p
    for i in list(m.missing_from_mf()):
        p(i)

    for i in m.db['Kepek'].find():
        m.add_root_paths(i, FOLDER_PAIRS[0])


if __name__ == '__main__':
    m = MongoUtils('Kepek')
    to_reset = m.get_by_mf_mod_date(1)
    print(len(list(m.missing_from_mf())))
    for item in to_reset:
        m.update_item(item, {'mf': None})
    print(len(list(m.missing_from_mf())))
