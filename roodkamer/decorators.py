#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import abort
from flask.ext.login import current_user

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(current_user, 'can') or\
            not current_user.can(permission):
                abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
