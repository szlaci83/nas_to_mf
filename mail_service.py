import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_properties import *
from mail_repo import create_report_mail

'''
  Service to send invitation and registration e-mails
'''

def _sendmail(to, subject, html, text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM_ADDR
    msg['To'] = to

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.login(FROM_ADDR, PW)
    server.sendmail(FROM_ADDR, to, msg.as_string())
    server.quit()


def send_report_mail(to_mail, title, no_of_files, file_list):
    html, text = create_report_mail(title, no_of_files, file_list)
    _sendmail(to_mail, SUBJECT, html, text)


def _example():
    send_report_mail(TEST_EMAIL, "Triton -> Mediafire", 3, ["file1.jpg", "file2.jpg"])


if __name__ == "__main__":
    _example()

