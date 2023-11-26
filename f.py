import os
import shutil

source = '/media/local/sda3/HomeMade/Kepek/'

for root, dirs, files in os.walk(source):
    for dir in dirs:
        if dir.find("_") == -1:
            t = os.path.join(root, dir)
           # shutil.rmtree(t)
            print(t)

