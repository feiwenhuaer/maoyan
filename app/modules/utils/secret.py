"""
This module includes many of common methods about secret
"""


def md5(string):
    """
    MD5 for a string
    """
    import hashlib
    md5_obj = hashlib.md5()
    md5_obj.update(string.encode("utf8"))
    return md5_obj.hexdigest()
