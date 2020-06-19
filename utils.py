import os
import re
from db_handler import MongoUtils
import shutil

def correct(line):
    return line.replace('Ã¼', 'u').replace('Å', 'o').replace('Ã©', 'e').replace('Ã³','o').replace('Ã­','i').replace('Ã¡', 'a').replace('Å±','u').replace('Å?', 'o')


def ekezettelenit(line):
    return line.replace('ü', 'u').replace('ő', 'o').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á','a')


def ultimate_remover(line):
    return re.sub("[^0-9a-zA-Z-/._]+", "", line)


def replace_spec_chars(line):
    return ekezettelenit(correct(line)).replace(" ", "_").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "")


def ultimate_replacer(line):
    return ultimate_remover(replace_spec_chars(line))


def load_done(done_file, path=None):
    global files_done
    path = path or os.getcwd()
    with open(os.path.join(path, done_file)) as f:
        lines = f.read().splitlines()
    files_done = lines
    return


def save_done(done_file,path=None):
    global files_done
    path = path or os.getcwd()
    with open(os.path.join(path, done_file), "w+") as f:
        for item in files_done:
            f.write(item + "\n")
    f.close()
    return


def find_dups(filename):
    dups = open(filename + 'dups', 'w')
    hashes = {}
    total_size = 0
    for line in open(filename, "r"):
        try:
            name, hash, size = line.split(',')
            if hash in hashes:
                dups.write(name + '\n')
                total_size += int(size)
            else:
                hashes[hash] = name
        except ValueError:
            print(line)
    dups.close()
    print("Total duplicatin size = %d Gb" % (total_size / 1000000000))


def rename_mf_path(old_path, new_path):
    m = MongoUtils('Kepek')
    docs = m.get_mf_path_like("Kepek/"+ old_path)
    for d in docs:
        print(d["mf"]["path"])
        d["mf"]["path"] = d.get("mf").get("path").replace(old_path, new_path)
        m.update_item(d, {"mf": d.get("mf")})
        print(d["mf"]["path"])


def add_local_path():
    local_root = '/media/local/sda3'
    m = MongoUtils('Kepek')
    to_update = m.missing_from_local()

    for i in to_update:
        new_local = local_root + i['ftp_path']
        if not os.path.exists(new_local):
            print(f"Doesnt exist: {new_local}")
        else:
            print(i['ftp_path'])
            m.update_item(i, {'local_path': new_local})


def copy_without_spec_chars(source, dest):
    for root, dirs, files in os.walk(source):
        dest_root = root.replace(source, dest)
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)
        for file in files:
            shutil.copyfileobj(
                 os.path.join(root,  file),
                 os.path.join(ultimate_replacer(dest_root), ultimate_replacer(file))
                 )


if __name__ == '__main__':
    copy_without_spec_chars("/media/triton/HomeMade/Kepek/", "/media/triton/Backups/Kepek/")
