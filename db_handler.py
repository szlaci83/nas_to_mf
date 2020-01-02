from utils import ekezettelenit, correct
from settings import DATABASE_NAME, DATABASE_HOST, FOLDER_PAIRS
import pymongo


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

    def add_root_paths(self, item, folder_pair,  coll_name=None):
        coll = coll_name or self.coll
        self.db[coll].update_one({"_id": item["_id"]}, {"$set": {"mf_root": folder_pair['mf'], 'ftp_root': folder_pair['ftp']}})

    def correct_ftp_path(self, to_correct, coll_name=None, delete_none=True):
        coll = coll_name or self.coll
        for item in self.db[coll].find():
            try:
                corrected = ekezettelenit(correct(item[to_correct]))
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

    def insert_one(self, record, coll_name=None):
        coll = coll_name or self.coll
        self.db[coll].insert_one(record)


if __name__ == '__main__':
    # TODO: get name from param
    m = MongoUtils("Kepek")
    print("Using host: %s, db: %s, collection: %s" % (m.host,  m.db_name, m.coll))
    print("Missing from Mediafire: %d " % m.missing_from_mf())
    print("Missing from NAS: %d " % m.missing_from_ftp())
    # TODO : missing from local, total ..


    # for i in m.db.find():

    #     m.add_root_paths(i, FOLDER_PAIRS[0])
