import bcrypt


def truncate_line(line):
    return line.replace('\n').strip()


def append_slash(path):
    return path if path[-1] == '/' else f'{path}/'


def get_hash_passwd(passwd):
    passwd = str(passwd).encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed.decode('utf-8')
