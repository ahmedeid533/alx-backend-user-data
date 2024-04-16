#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, Type
from models.user import User


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> Type[User]:
        """ current_user
        """
        return None


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def current_user(self, request=None) -> Type[User]:
        """ current_user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        if auth_header[:6] != 'Basic ':
            return None
        auth_header = auth_header[6:]
        from base64 import b64decode
        try:
            auth_header = b64decode(auth_header.encode('utf-8'))\
                .decode('utf-8')
        except Exception:
            return None
        auth_header = auth_header.split(':')
        if len(auth_header) != 2:
            return None
        email = auth_header[0]
        password = auth_header[1]
        user = User.search({'email': email})
        if user is None or user[0].is_valid_password(password) is False:
            return None
        return user[0]
