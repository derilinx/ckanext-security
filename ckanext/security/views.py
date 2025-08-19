# -*- coding: utf-8 -*-

import logging
import os
from functools import wraps

from flask import Blueprint, make_response, send_file, Response
from ckan.plugins import toolkit as tk
from ckan.lib import helpers

from ckanext.security import utils

log = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        utils.check_user_and_access()
        return f(*args, **kwargs)
    return decorated_function


# Blueprints
mfa_user = Blueprint("mfa_user", __name__)
securitytxt = Blueprint("securitytxt", __name__)


# --- MFA routes ---
def login():
    headers = {'Content-Type': 'application/json'}
    (status, res_data) = utils.login()
    return make_response((res_data, status, headers))


@login_required
def configure_mfa(id=None):
    extra_vars = utils.configure_mfa(id)
    return tk.render('security/configure_mfa.html',
                     extra_vars={'c': extra_vars})


@login_required
def new(id=None):
    utils.new(id)
    return helpers.redirect_to('mfa_user.configure_mfa', id=id)


def security_txt():
    # Path from config, fallback to bundled file adjacent to this views.py
    default_path = os.path.join(os.path.dirname(__file__), 'security.txt')
    filepath = tk.config.get('ckan.securitytxt.path', default_path)

    if os.path.exists(filepath):
        return send_file(filepath, mimetype='text/plain')
    return Response("Not found", status=404, mimetype='text/plain')


mfa_user.add_url_rule('/api/mfa_login', view_func=login, methods=['POST'])
mfa_user.add_url_rule('/configure_mfa/<id>',
                      view_func=configure_mfa, methods=['GET', 'POST'])
mfa_user.add_url_rule('/configure_mfa/<id>/new',
                      view_func=new, methods=['GET', 'POST'])

securitytxt.add_url_rule('/.well-known/security.txt',
                         view_func=security_txt, methods=['GET'])


def get_blueprints():
    return [mfa_user, securitytxt]
