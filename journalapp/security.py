"""Define security groups."""
import os
from passlib.apps import custom_app_context as pwd_context

USERS = {'editor': 'editor',
         'viewer': 'viewer'}


def check_password(password):
    """Check password."""
    secret = os.environ.get('AUTH_PASSWORD', 'default')
    hashed = pwd_context.encrypt(secret)
    return pwd_context.verify(password, hashed)

