import bcrypt


def truncate_line(line):
    return line.replace('\n').strip()


def get_hash_passwd(passwd):
    passwd = str(passwd).encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed.decode('utf-8')
