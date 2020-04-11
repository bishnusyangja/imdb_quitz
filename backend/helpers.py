import binascii
import hashlib
import os
import random
import string


class Anonymous:
    pass


def get_random_string(chars=22):
    char_set = f'{string.digits}{string.ascii_letters}'
    random.choice(char_set)
    return ''.join(random.sample(char_set, chars))


def truncate_line(line):
    return line.replace('\n', '').strip()


def append_slash(path):
    return path if path[-1] == '/' else f'{path}/'


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    print(len(pwdhash), f'  {type(pwdhash)} ', pwdhash)
    print(len(stored_password), f' {type(pwdhash)} ', stored_password)
    return pwdhash == stored_password
