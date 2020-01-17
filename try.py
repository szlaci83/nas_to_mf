import ftptool
import properties

conn = ftptool.FTPHost.connect(host="192.168.0.243",port=12345, user=properties.ftp_user, password=properties.ftp_password)
pic = conn.current_directory
print(pic)
print(conn.listdir(pic +"/DCIM"))
ftp = ftptool.FTPFileClient.connect(host="192.168.0.243",port=12345, user=properties.ftp_user, password=properties.ftp_password)

#f = conn.file_proxy("pics\\test0.jpg")

for i in range(11):
    ftp.put("pics\\small-test%d.jpg" %i, "/storage/emulated/0/DCIM/test%d.jpg" % i)

#ftp .set_current_directory("/storage/emulated/0/DCIM")
#ftp.mput(["pics\\test0.jpg"])
#print(pic)



