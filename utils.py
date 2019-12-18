import os

def correct(line):
    return line.replace('Ã¼', 'u').replace('Å', 'o').replace('Ã©', 'e').replace('Ã³','o').replace('Ã­','i').replace('Ã¡', 'a').replace('Å±','u').replace('Å?', 'o')


def ekezettelenit(line):
    return line.replace('ü', 'u').replace('ő', 'o').replace('é', 'e').replace('ó', 'o').replace('í', 'i').replace('á','a')



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


if __name__ == '__main__':
    find_dups('Kepek_on_mf.txt')

