#!/usr/bin/env python3
""" Module of basic Auth views
"""
from flask import request
from typing import List, Type
from models.user import User
from api.v1.auth.auth import Auth


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
        if base64_authorization_header is None or \
           type(base64_authorization_header) is not str:
            return None
        try:
            return base64_authorization_header.\
                encode('utf-8').decode('base64')
        except Exception:
            return None
