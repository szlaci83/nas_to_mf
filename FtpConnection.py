from ftplib import FTP, error_perm
import properties as p


class FtpConnection:
    def __init__(self, host, user_name, password):
        self.ftp = FTP(host, user_name, password)

    def get_files(self, target_dir):
        if self.set_cwd(target_dir):
            files = self.ftp.retrlines("NLST")
            return files
        return []

    def traverse(self, target_dir, depth=0):
        if depth == 0:
            self.set_cwd(target_dir)
        if depth > 10:
            return ['depth > 10']
        level = {}
        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                self.ftp.cwd(entry)
                print(entry)
                level[entry] = self.traverse(self.ftp, depth + 1)
                self.ftp.cwd('..')
            except error_perm:
                level[entry] = None
        return level

    def upload(self, filename, file):
        try:
            self.ftp.storbinary("STOR " + filename, file)
        except:
            return False
        return True

    def download(self, filename, file):
        try:
            self.ftp.retrbinary('RETR ' + filename, file.write)
        except:
            return False
        return True

    def set_cwd(self, directory):
        try:
            self.ftp.cwd(directory)
        except:
            return False
        return True

    def close(self):
        self.ftp.quit()


def _example():
    ftp = FtpConnection(p.ftp_host, p.ftp_user, p.ftp_password)
    ftp.set_cwd("/Doksik")
    #get_files(ftp, "/Test/Kamera")
    up_file = open('/home/laszlo/test.txt', 'rb')
    down_file = open('/home/laszlo/test2.txt', 'wb')
    ftp.upload(ftp, "test.txt", up_file)
    ftp.get_files(ftp, "/Doksik")
    up_file.close()
    down_file.close()
    ftp.close()


if __name__ == "__main__":
    _example()
