from datetime import datetime
from os.path import splitext

import os, random, string
from uuid import uuid4


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


def path_and_rename(path):
    def wrapper(instance, filename):
        # ext = filename.split('.')[-1]
        ext = splitext(filename)[1]
        f_name = '-'.join(filename.replace(ext, '').split())
        rand_strings = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))
        filename = '%s%s%s' % (rand_strings, uuid4().hex, ext)
        return os.path.join(path, filename)
    return wrapper


def rename_file(instance, file_name):
    ext = splitext(file_name)[1]
    rand_strings = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))
    return '%s%s%s' % (rand_strings, uuid4().hex, ext)

