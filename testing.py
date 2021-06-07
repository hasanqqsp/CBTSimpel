import random

def generate_id():
    # from https://stackoverflow.com/questions/39137344/short-unique-hexadecimal-string-in-python?
    digits = '0123456789'
    letters = 'abcdef'
    all_chars = digits + letters
    length = 16
    while True:
    val = ''.join(random.choice(all_chars) for i in range(length))
    if not val.isdigit():
        break
    return val