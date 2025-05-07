import re


def snake_to_lower_camel(string):
    return re.sub("_[a-z0-9]", lambda p: p.group(0)[1].upper(), string)


def keep_same(string):
    return string
