import hashlib

def get_md5(url):
    if isinstance(url,str):
        url = url.encode()
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


