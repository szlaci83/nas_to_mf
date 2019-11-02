import os


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

