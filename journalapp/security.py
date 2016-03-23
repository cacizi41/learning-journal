"""Define security groups."""
import os
from passlib.apps import custom_app_context as pwd_context

USERS = {'editor': 'editor',
         'viewer': 'viewer'}


# GROUPS = {'editor': ['group:editors']}


# def groupfinder(username, request):
#     """If user in editor, return group editor. Else, none. authn callback."""
#     if username in USERS:
#         return GROUPS.get(username, [])


def check_password(password):
    """check password."""
    hashed = os.environ.get('AUTH_PASSWORD', 'default')
    return pwd_context.verify(password, hashed)
