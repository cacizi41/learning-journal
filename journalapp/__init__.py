"""Initiliazes the journalapp in Pyramid."""
import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
# from .security import groupfinder
from .models import (
    DBSession,
    Base,
    DefaultRoot
)


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""

    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    settings['auth.username'] = os.environ.get('AUTH_USERNAME', '')
    settings['auth.password'] = os.environ.get('AUTH_PASSWORD', '')
    secret = os.environ.get('AUTH_SECRET', 'i dunno what this is')
    authn_policy = AuthTktAuthenticationPolicy(secret)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory=DefaultRoot, settings=settings)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_route('list', '/')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('detail', '/detail/{detail_id}')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{detail_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
