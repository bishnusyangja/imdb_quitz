import binascii
import hashlib
import os
import random
import string

from settings import NOMINEES_SPLIT


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


def get_question_text(content):
    return f"Which of the following is awarded as {content.category} in {content.award} award?"


def get_options_from_content(content, right_number=None):
    try:
        options = random.sample(content.nominees.replace(content.winner, '').strip(NOMINEES_SPLIT).replace(
            NOMINEES_SPLIT * 2, NOMINEES_SPLIT).split(NOMINEES_SPLIT), 3)
    except Exception as exc:
        print('Excep', exc)
        return None
    right_number = random.choice(range(4)) + 1 if right_number is None else right_number
    params = {f'option{right_number}': content.winner}
    right_assigned = False
    right_option = f'option{right_number}'
    for i in range(3):
        if i + 1 == right_number:
            right_assigned = True
        index = i + 2 if right_assigned else i + 1
        params[f'option{index}'] = options[i]
    params['right_answer'] = right_option
    return params


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
