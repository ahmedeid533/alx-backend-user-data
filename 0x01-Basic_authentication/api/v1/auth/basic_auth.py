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
	pass