import logging 
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

# Handlers
file_handler = logging.FileHandler(f"{os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs', 'app.log')}", mode="a")
file_handler.setLevel(logging.DEBUG)

# Formatters
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter(
  '[%(asctime)s] - %(filename)s - line: %(lineno)d - function: %(funcName)s - %(levelname)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S'
)

file_handler.setFormatter(formatter)

# Configure email handler
class EmailNotificationHandler(logging.Handler):
    def __init__(self, mail_host, mail_port, sender_email, sender_password, receiver_email):
        super().__init__()
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def emit(self, record):
        subject = f"Error Log Notification - {record.levelname}"
        body = self.format(record)
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL(self.mail_host, self.mail_port) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())


# Add email handler to the logger (change the SMTP settings accordingly)
email_handler = EmailNotificationHandler(
    mail_host="MAILSERVER",
    mail_port=465,
    sender_email="SENDER",
    sender_password="PASSWORD",
    receiver_email="RECIPIENT"
)

email_handler.setLevel(logging.WARNING)  # Send email notifications only for WARNING level and above
logger.addHandler(email_handler)
logger.addHandler(file_handler)

# Example usage
logger.debug("This is a debug message")
logger.warning("This is a warning message")
