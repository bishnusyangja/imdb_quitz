import random
import string
import bcrypt


def get_random_string(chars=22):
    char_set = f'{string.digits}{string.ascii_letters}'
    random.choice(char_set)
    return ''.join(random.sample(char_set, chars))


def truncate_line(line):
    return line.replace('\n', '').strip()


def append_slash(path):
    return path if path[-1] == '/' else f'{path}/'


def get_hash_passwd(passwd):
    passwd = str(passwd).encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed.decode('utf-8')
