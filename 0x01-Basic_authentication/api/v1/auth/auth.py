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
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        for p in excluded_paths:
            if p.endswith('*') and path.startswith(p[:-1]):
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
