import os

# MediaFire
email = os.environ.get('MF_EMAIL')
password = os.environ.get('MF_PASSWORD')
app_id = os.environ.get('MF_APP_ID')
DONE_FILE = ''

# FTP
private_ftp = os.environ.get('LOCAL_FTP')
public_ftp = os.environ.get('PUBLIC_FTP')
ftp_host = public_ftp
ftp_user = os.environ.get('FTP_USER')
ftp_password = os.environ.get('FTP_PASSWORD')


if __name__ == '__main__':
    from pprint import pprint as p
    p(globals())
