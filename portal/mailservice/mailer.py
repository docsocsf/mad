import smtplib

from config import HOST, PORT, TLS, USER, PASSWORD, FROM, SEND_EMAILS


class Mailer:
    def __init__(self, send_emails=SEND_EMAILS):
        """
        :param send_emails: Boolean whether emails should be sent. Suggested to set to  False when debugging
        """
        self.__send_emails = send_emails
        if not self.__send_emails:
            return

        smtp = smtplib.SMTP(HOST, PORT)
        if TLS:
            smtp.starttls()
        smtp.login(USER, PASSWORD)

        self.__smtp = smtp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__send_emails:
            return

        self.__smtp.quit()

    def send_email(self, mail):
        if not self.__send_emails:
            return

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, mail.recipient(), mail.subject(), mail.message())

        self.__smtp.sendmail(FROM, mail.recipient(), message)
