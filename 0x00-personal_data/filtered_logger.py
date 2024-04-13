#!/usr/bin/env python3
""" Module for filtering log messages. """

import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ Returns the log message obfuscated. """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        """ Constructor method. """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Format the record. """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
        NotImplementedError


def get_logger() -> logging.Logger:
    """ Returns a logging object. """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter())
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database."""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn


def main():
    """ Main function. """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    [print(user) for user in cursor]
