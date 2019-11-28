from passlib.hash import django_pbkdf2_sha256 as handler
import time
from Crypto.Cipher import AES
from Crypto import Random
import json
import hashlib
from django.conf import settings
from ..email import BaseEmailClient
from ..models import User, UserSettings

encryptor = None


def __get_aes_obj():
    global encryptor
    if not encryptor:
        encryptor = AESCipher(settings.CONFIG['PASSWORD_RECOVERY_SECRET'])
    return encryptor


def get_user_by_email(email):
    if not email:
        raise Exception('No user email provided.')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    return user


def get_user_by_id(id):
    if not id:
        raise Exception('No user id provided.')

    return User.objects.get(id=id)


def get_user_settings_by_id(id):
    if not id:
        raise Exception('No user id provided.')

    return UserSettings.objects.get(id=id)


def check_password(user, password):
    return handler.verify(password, user.password) if user else False


def create_user(email, password, fullname, login='', age=18, street='',
                city='', zip='', role='user'):
    res = fullname.split(' ')
    first_name = '' if len(res) == 1 else res[0]
    last_name = res[0] if len(res) == 1 else ' '.join(res[1:])

    user = User(email=email,
                password=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                login=login,
                age=age,
                street=street,
                city=city,
                zip=zip,
                role=role)

    user_settings = UserSettings(id=user.id,
                                 theme='default')
    user.save()
    user_settings.save()


def update_user_password(user, new_password):
    user.password = generate_password_hash(new_password)
    user.objects.filter(email=user.email).update(password=user.password)
    user.save()


def check_user_exists(email):
    return True if get_user_by_email(email) else False


def update_user(user):
    user.objects.filter(email=user.email).update(password=user.password,
                                                 first_name=user.first_name,
                                                 last_name=user.last_name,
                                                 login=user.login,
                                                 age=user.age,
                                                 street=user.street,
                                                 city=user.city,
                                                 zip=user.zip,
                                                 role=user.role)
    user.save()


def generate_password_hash(password):
    return handler.hash(secret=password)


def send_password_reset_link(email):
    user = get_user_by_email(email)
    if user:
        obj = {'user_id': user.id,
               'valid': time.time() + settings.CONFIG['PASSWORD_RECOVERY_TTL']}
        payload = json.dumps(obj, ensure_ascii=False)

        asd = BaseEmailClient()
        asd.send_password_recovery_email(user.email,
                                         user.last_name if not user.first_name else user.first_name,
                                         __get_aes_obj().encrypt(payload))
    else:
        raise ValueError('No user found')


def reset_user_password(token, new_password):
    payload = __get_aes_obj().decrypt(token)
    obj = json.loads(payload)

    if obj['valid'] < time.time():
        raise Exception('Reset password token has expired')

    user = get_user_by_id(obj['user_id'])
    if user:
        update_user_password(user, new_password)


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return (iv + cipher.encrypt(raw.encode('utf8'))).hex()

    def decrypt(self, enc):
        enc = bytes.fromhex(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
