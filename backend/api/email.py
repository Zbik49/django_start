import smtplib
from email import message
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BaseEmailClient(object):
    def send_email(self, to_addr='', subject='', body=''):
        pass

    def send_password_recovery_email(self, to_addr, full_name, recovery_token):
        subject = f'{settings.CONFIG["APP_NAME"]} - password recovery'
        password_recovery_url = f'{settings.CONFIG["FRONT_END_DOMAIN"]}' \
            f'/#/auth/reset-password?reset_password_token={recovery_token}'
        body = f'Hello {full_name},' \
            f'\nWe have received password reset request. ' \
            f'To do this, please proceed at {password_recovery_url}' \
            f'\nIf it wasn\'t you, take no action or contact support.\n' \
            f'\nThank you,\nSupport team.'

        self.__get_email_client().send_email(to_addr, subject, body)

    @staticmethod
    def __get_email_client():
        return FakeEmailClient() if settings.CONFIG['SMTP_SETTINGS']['DEBUG'] else SMTPEmailClient()


class FakeEmailClient(BaseEmailClient):

    def send_email(self, to_addr='', subject='', body=''):
        logging.info(f"Sending email\nFrom: {settings.CONFIG['SMTP_SETTINGS']['FROM']}"
                     f"\nTo: {to_addr}\nSubject: {subject}\nBody:\n{body}")


class SMTPEmailClient(BaseEmailClient):
    def send_email(self, to_addr='', subject='', body=''):
        from_addr = settings.CONFIG['SMTP_SETTINGS']['FROM']

        msg = message.Message()
        msg.add_header('from', from_addr)
        msg.add_header('to', to_addr)
        msg.add_header('subject', subject)
        msg.set_payload(body)

        server = smtplib.SMTP(settings.CONFIG['SMTP_SETTINGS']['HOST'],
                              settings.CONFIG['SMTP_SETTINGS']['PORT'])
        server.login(from_addr, settings.CONFIG['SMTP_SETTINGS']['PASSWORD'])
        server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
