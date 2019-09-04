#!/usr/bin/env python
import os
import utils
from settings import DONE_FILE, LOG_FILE, LOGGING_LEVEL, NOT_TO_SYNC
from MediaFireConnection import MediaFireConnection
import sys
import logging

global files_done


def iterate_dir(source_path=None, target_dir=None):
    global files_done
    source_path = source_path or os.getcwd()
    for filename in [f for f in os.listdir(source_path) if f not in files_done]:
        if not filename.endswith(".py") and filename not in NOT_TO_SYNC:
            logging.info("Uploading: %s" % filename)
            res = mf.upload_file(source_path, filename, target_dir, filename)
            if res:
                logging.info("Upload result: %s" % mf.get_file_info(uploadresult=res))
                files_done.append(filename)
                utils.save_done(source_path, files_done)
            else:
                logging.info("Failed to upload: %s" % filename)
    return


def arg_upload():
    target_dir = str(sys.argv[1])
    logging.info("Syncing target directory: %s" % target_dir)
    iterate_dir(source_path=None, target_dir=target_dir)
    logging.info("Syncing: %s done, see %s for file list." % (target_dir, DONE_FILE))
    return


def _example():
    global files_done
    path = ''
    target_dir = ''
    utils.load_done(DONE_FILE, path)
    logging.info("Syncing: %s to target directory: %s" % (path, target_dir))
    iterate_dir(source_path=path, target_dir=target_dir)
    logging.info("Syncing: %s done, see %s for file list." % (target_dir, DONE_FILE))
    return


if __name__ == "__main__":
    if LOG_FILE and LOG_FILE != '':
        print("Syncing on MediaFire see " + LOG_FILE + " for details!")
    logging.basicConfig(filename=LOG_FILE, level=LOGGING_LEVEL, format="%(asctime)s:%(levelname)s:%(message)s")

    mf = MediaFireConnection()
    _example()
