import json
import jwt
import pyodbc
from flask import jsonify
from datetime import datetime, timedelta


class user_model:
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

    def user_getall_model(self):
        try:
            select_query = "SELECT * FROM Users;"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()

            result = [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]

            if len(result) > 0:
                return jsonify({'Payload': result}), 200
            else:
                return jsonify({"message": "No Records Found."}), 204

        except Exception as e:
            print(f'Error in fetching users: {e}')
            return jsonify({'message': f'Error in fetching users: {e}'}), 500
        # finally:
        #     # Close cursor and connection
        #     self.cursor.close()
        #     self.conn.close()

    def user_addone_model(self, data):
        try:
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            role = data.get('role_id')
            password = data.get('password')

            insert_query = "insert into Users(name, phone, email, role_id, password) values (?, ?, ?, ?, ?);"

            self.cursor.execute(insert_query, (name, phone, email, role, password))

            print('User created successfully')
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            print(f'Error in creating user: {e}')
            return jsonify({'message': 'Failed to create user'}), 500

    def user_update_model(self, data):
        try:
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            role = data.get('role_id')
            password = data.get('password')
            userid = data.get('id')

            update_query = "Update Users set name=?, phone=?, email=?, role_id=?, password=? where id=?;"

            self.cursor.execute(update_query, (name, phone, email, role, password, userid))

            print('User Record updated successfully')
            if self.cursor.rowcount > 0:
                return jsonify({'message': "User Record Updated Successfully"}), 201
            else:
                return jsonify({"message": "No Records to Update. Please provide correct id."}), 202

        except Exception as e:
            print(f'Error in updating user: {e}')
            return jsonify({'message': 'Failed to update user'}), 204

    def user_delete_model(self, id):
        try:
            delete_query = "Delete from Users where id=?;"

            self.cursor.execute(delete_query, (id,))

            if self.cursor.rowcount > 0:
                print('User Record deleted successfully')
                return jsonify({'message': "User Record deleted Successfully"}), 200
            else:
                print('Error in deleting user record, Provided id is not present in the database.')
                return jsonify(
                    {'message': "Error in deleting user record, Provided id is not present in the database."}), 204

        except Exception as e:
            print(f'Error in deleting user record: {e}')
            return jsonify({'message': 'Failed to delete user record'}), 500

    def user_patch_model(self, data, id):
        try:
            query = "Update Users set "
            for key in data:
                query += f"{key}='{data[key]}',"
            query = query[:-1] + f" Where id=?;"

            self.cursor.execute(query, (id,))
            print('User Record updated successfully')
            if self.cursor.rowcount > 0:
                return jsonify({'message': "User Record Updated Successfully"}), 201
            else:
                return jsonify({"message": "No Records to Update. Please provide correct id."}), 202

        except Exception as e:
            print(e)

    def user_pagination_model(self, limit, page):
        try:
            start = (page - 1) * limit
            query = f"SELECT * FROM Users ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY;"
            self.cursor.execute(query, (start, limit))
            rows = self.cursor.fetchall()

            result = [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]

            if len(result) > 0:
                return jsonify({'Payload': result, "page_no": page, "no_of_rocords": limit}), 200
            else:
                return jsonify({"message": "No Records Found."}), 204

        except Exception as e:
            print(f'Error in fetching records: {e}')
            return jsonify({"message": "Internal Server Error"}), 500  # Use status code 500 for internal server error

    def user_upload_avatar_model(self, uid, file_with_path):
        try:
            update_query = "Update Users set avatar=? where id=?;"

            self.cursor.execute(update_query, (file_with_path, uid))

            # print('File uploaded successfully')
            if self.cursor.rowcount > 0:
                return jsonify({'message': "File uploaded Successfully"}), 201
            else:
                return jsonify({"message": "No Records to Update. Please provide correct id."}), 202

        except Exception as e:
            print(f'Error in updating user: {e}')
            return jsonify({'message': 'Failed to update user'}), 204

    def user_login_model(self, data):
        try:
            query = "select id, name, email, phone, avatar, role_id from Users where email = ? and password = ?"
            email = data.get('email')
            password = data.get('password')
            self.cursor.execute(query, (email, password))
            row = self.cursor.fetchone()

            if row:
                userdata = {
                    'id': row.id,
                    'name': row.name,
                    'email': row.email,
                    'phone': row.phone,
                    'avatar': row.avatar,
                    'role_id': row.role_id
                }

                exp_time = datetime.now() + timedelta(minutes=15)
                epoch_time = int(exp_time.timestamp())
                payload = {'payload': userdata,
                           'exp': epoch_time
                           }
                jwt_token = jwt.encode(payload, "patkar", algorithm="HS256")

                if jwt_token:
                    return jsonify({'token': jwt_token}), 200
                else:
                    return jsonify({"message": "Error generating token."}), 502
            else:
                return jsonify({'message': 'Invalid email or password.'}), 401

        except Exception as e:
            print(f'Error in login: {e}')
            return jsonify({'message': 'Failed to login.'}), 500
