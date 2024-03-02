import re

import jwt
import pyodbc
from flask import jsonify, request
from datetime import datetime, timedelta


class auth_model:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                r'DRIVER={SQL Server};'
                r'SERVER=(local)\SQLEXPRESS;'
                r'DATABASE=flask_app;'
                r'Trusted_Connection=yes;'
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print('Connection Established Successfully')
        except Exception as e:
            print(f'Error in Connection : {e}')

    def token_auth(self, endpoint):
        def inner1(func):
            def inner2(*args):
                token = request.headers.get('authorization')
                if re.match('^Bearer *([^ ]+) *$', token, flags=0):
                    token = token.split(' ')[1]
                    print(token)
                    return func(*args)
                else:
                    return jsonify({'message': 'invalid token.'}), 401

            return inner2

        return inner1
