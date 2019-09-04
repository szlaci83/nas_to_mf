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

