import os
import pytest
import webtest
from webtest import TestApp
from journalapp import main
from passlib.apps import custom_app_context as pwd_context
# from pyramid.authorization import ACLAuthorizationPolicy
# from pyramid.authentication import AuthTktAuthenticationPolicy
# from journalapp.views import list_view, detail_view
# from journalapp.models import DefaultRoot


@pytest.fixture()
def app():
    """TestApp setup."""
    setting = {
        'sqlalchemy.url': 'sqlite:////tmp/test_journal.sqlite',
        'pyramid.debug_authorization': 'true'
    }
    app = main({}, **setting)
    return TestApp(app)


@pytest.fixture()
def auth_env():
    """Authtication env seup."""
    # from journalapp.security import check_password
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('testpassword')
    os.environ['AUTH_USERNAME'] = 'Authenticated'


@pytest.fixture()
def authenticated_app(app, auth_env):
    """Authenticated user input."""
    user_input = {'username': 'Authenticated', 'password': 'testpassword'}
    app.post('/add', user_input)

def test_access_to_home(app, dbtransaction):
    """View permitted to everyone."""
    response = app.get('/')
    assert response.status_code == 200


def test_access_to_add(app):
    """View permitted."""
    with pytest.raises(webtest.app.AppError):
        assert app.get('/add')
# can't assert status code 403
# raising at least one scoped session is already in present -v -s


def test_password_exist(auth_env):
    """Pwd exists in AUTH ENV."""
    assert os.getenv('AUTH_PASSWORD', None) is not None


def test_username_exist(auth_env):
    """Username exists in AUTH ENV."""
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_pwd_true(auth_env):
    """Check if pwd is matching with authenv."""
    from journalapp.security import check_password
    password = 'testpassword'
    assert check_password(password) == True


def test_check_pwd_fail(auth_env):
    """Check if pwd is matching with authenv."""
    from journalapp.security import check_password
    password = 'teapassword'
    assert check_password(password) == False


def test_store_pwd_true(app):
    """Check if pwd is stored in app."""
    # from journalapp.security import check_password
    assert os.environ.get('AUTH_PASSWORD', None) is not None


# def test_post_login_permission(app, auth_env):
#     """Test weather user can visit add page w/ right usrname and pwd."""
#     user_input = {'username': 'Authenticated', 'password': 'testpassword'}
#     response = app.post('/add', user_input)
#     assert response.status_code == 200


# def test_post_login_fail(app, auth_env):
#     """Test weather user can visit add page w/ wrong usrname and pwd."""
#     user_input = {'username': 'Authenticated', 'password': 'teapassword'}
#     response = app.post('/add', user_input)
#     assert response.status_code == 403



