from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost',
                 '127.0.0.1',
                 '16.170.224.110',
                 '172.31.35.218',
                 '13.53.130.235',
                 '172.31.32.59',
                 '16.171.5.173']

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT')
    }
}
