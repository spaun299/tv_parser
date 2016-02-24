import config
import smtplib
import sys
import traceback
from email.mime.text import MIMEText
import os


class SendEmail:
    def __init__(self, username=config.MAIL_USERNAME, password=config.MAIL_PASSWORD,
                 send_to=None):
        self.username = username
        self.password = password
        self.send_to = send_to or [config.MAIL_USERNAME]

    def send_email(self, subject='Parse Error', text='Parse Error', exception=None,
                   use_smtp=True):
        if exception:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)
            filename_, line_, func_, text_ = tb_info[-1]
            message = 'An error occurred on File "{file}" line {line}\n {assert_message}'.format(
                line=line_, assert_message=exception.args, file=filename_)
            print(message)
            text = message
        text += '. Server {server_name}'.format(
            server_name='OPENSHIFT' if os.environ.get('OPENSHIFT_DATA_DIR')
            else 'localhost')
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = 'tvparser <tvparser.in.ua@gmail.com>'
        msg['To'] = ','.join(self.send_to)
        if use_smtp:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(self.username, self.password)
        else:
            server = smtplib.SMTP('localhost')
        server.sendmail(self.username, self.send_to, msg.as_string())
        server.quit()
