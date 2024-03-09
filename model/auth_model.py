import json
import re
import jwt
import pyodbc
from functools import wraps
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

    def token_auth(self):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                try:
                    endpoint = request.path
                    token = request.headers.get('authorization')
                    if re.match('^Bearer *([^ ]+) *$', token, flags=0):
                        token = token.split(' ')[1]
                        try:
                            jwt_decoded = jwt.decode(token, 'patkar', algorithms='HS256')
                        except jwt.ExpiredSignatureError:
                            print('Token has expired. Generate new token.')
                            return jsonify({'message': 'Token has expired. Generate new token.'})

                        role_id = jwt_decoded['payload']['role_id']

                        query = 'select roles from EndpointAccessibility where endpoint = ?'
                        self.cursor.execute(query, (endpoint,))
                        result = self.cursor.fetchall()

                        if len(result) > 0:
                            allowed_roles = result[0][0]
                            if str(role_id) in allowed_roles:
                                return func(*args)
                            else:
                                return jsonify({'message': 'invalid role'}), 404
                        else:
                            return jsonify({'message': 'invalid endpoint'}), 404
                except Exception as e:
                    print(f'Error : {str(e)}')
                    return f'Error: {e}', 401
                else:
                    return jsonify({'message': 'invalid token.'}), 401

            return inner2

        return inner1
