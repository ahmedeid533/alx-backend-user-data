#!/usr/bin/env python3
""" Module for filtering log messages. """
import re
from typing import List
import os
import mysql.connector
import logging
import sys


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
	""" Returns the log message obfuscated. """
	for field in fields:
		message = re.sub(f'{field}=.*?{separator}',
						 f'{field}={redaction}{separator}', message)
	return message
