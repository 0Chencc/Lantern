import time
import hashlib


def now_timestamp_md5():
    hash_object = hashlib.md5(str(int(time.time())).encode())
    return hash_object.hexdigest()
