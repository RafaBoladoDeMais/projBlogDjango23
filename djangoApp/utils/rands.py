import string as s
from random import SystemRandom
from django.utils.text import slugify

def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        s.ascii_lowercase + s.digits, k=k
    )) 

def slugify_new(text):
    return slugify(text) + '-' + random_letters()
