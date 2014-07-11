import os
import configparser
import pathlib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import urllib.request


# noinspection PyAttributeOutsideInit
class EmailClient(object):
    def __init__(self):
        config_file = '/etc/pin-monitor/modules/emailer.conf'
        path = pathlib.Path(config_file)
        if not path.exists():
            raise FileNotFoundError('Configuration file not found at Path: {0}\r\nCurrent working directory is {1}'
                                    .format(path, os.path.dirname(os.path.realpath(__file__))))
        self._config = configparser.RawConfigParser()
        self._config._interpolation = configparser.ExtendedInterpolation()
        self._config.read(config_file)
        self.sections = self._config.sections()
        self.host = self._config.get('EMAIL', 'host')
        self.login = self._config.get('EMAIL', 'login')
        self.password = self._config.get('EMAIL', 'password')
        self.recipients = self._config.get('EMAIL', 'recipients')
        self.message = self._config.get('EMAIL', 'message')
        self.use_camera = self._config.getboolean("CAMERA", "use_camera")
        self.url = self._config.get('CAMERA', 'url')

    @staticmethod
    def send_email(login, password, recipients, host):

        now = datetime.datetime.now()
        msg = MIMEText(
            'This is a test message from Raspberry Pi.\r\nSomeone pressed the button @ {0} on {1}.'
            .format(now.strftime('%H:%M:%S'), now.strftime('%A %d %B %Y')),
            'plain', 'utf-8')
        msg['Subject'] = Header('Raspberry Pi', 'utf-8')
        msg['From'] = login
        msg['To'] = recipients

        s = smtplib.SMTP(host, 587, timeout=10)
        s.set_debuglevel(0)
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(msg['From'], recipients, msg.as_string())
        finally:
            s.quit()

    @staticmethod
    def send_email_conf(self):
        self.send_email(self.login, self.password, self.recipients, self.host)

    @staticmethod
    def send_email_image(self, login, password, recipients, image_url, host):
        # Message Text
        """ Get a an image from a camera using the image_url and attaches it to the email

        :param login: smtp username
        :param password: smtp password
        :param recipients: csv list of intended recipients
        :param image_url: the url to request image from camera
        :param host: the smtp host
        """
        now = datetime.datetime.now()
        body = 'This is a test message from Raspberry Pi.<br>Someone pressed the button @ {0} on {1}.<br />' \
            .format(now.strftime('%H:%M:%S'), now.strftime('%A %d %B %Y'))
        # Message Image
        img_path = '{0}/snap.jpg'.format(self._config.get('CAMERA', 'temp_dir_path'))
        urllib.request.urlretrieve(image_url, img_path)

        msg = MIMEMultipart(subtype='mixed')
        msg['Subject'] = Header('Raspberry Pi', 'utf-8')
        msg['From'] = login
        msg['To'] = recipients

        msg_text = MIMEText(
            '<b>{0}</b>'.format(body),
            'html')
        msg.attach(msg_text)

        fp = open(img_path, 'rb')
        img = MIMEImage(fp.read())
        fp.close()

        msg.attach(img)
        img.add_header('Content-ID', img_path)

        s = smtplib.SMTP(host, 587, timeout=10)
        s.set_debuglevel(0)
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            s.quit()

    @staticmethod
    def send_email_image_conf(self):
        """ Send an email and if use_camera is True
         an image from url in config file will be attached using CAMERA values from config file

        :param self: class
        """
        if self._use_camera:
            self.send_email_image(self, self.login, self.password, self.recipients, self.url, self.host)
        else:
            self.send_email_conf(self)

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, value):
        self._sections = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, value):
        self._recipients = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def use_camera(self):
        return self._use_camera

    @use_camera.setter
    def use_camera(self, value):
        self._use_camera = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value