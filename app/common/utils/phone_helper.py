import re


def is_valid_phone(phone: str):
    return re.match("\+[1-9]{1}[0-9]{3,14}", phone)
