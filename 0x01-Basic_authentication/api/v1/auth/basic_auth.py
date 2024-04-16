#!/usr/bin/env python3
""" Module of basic Auth views
"""
from flask import request
from typing import List, Type
from models.user import User
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract_base64_authorization_header
        """
        if authorization_header is None\
            or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode_base64_authorization_header
        """
        if base64_authorization_header is None\
            or type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extract_user_credentials
        """
        if decoded_base64_authorization_header is None\
            or type(decoded_base64_authorization_header) is not str\
                or ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> Type[User]:
        """ user_object_from_credentials
        """
        if user_email is None or user_pwd is None\
            or type(user_email) is not str or type(user_pwd) is not str:
            return None
        user = User.search({'email': user_email})
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> Type[User]:
        """ current_user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_base64_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(
            decoded_base64_auth_header)
        if user_credentials[0] is None or user_credentials[1] is None:
            return None
        return self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
