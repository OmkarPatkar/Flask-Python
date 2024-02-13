import json
import pyodbc
from flask import jsonify


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

            for row in rows:
                print(row)

            if len(result) > 0:
                return result
            else:
                print("No Records Found.")
                return jsonify({'message': 'No Records Found.'}), 204
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
            role = data.get('role')
            password = data.get('password')

            insert_query = "insert into Users(name, phone, email, role, password) values (?, ?, ?, ?, ?);"

            self.cursor.execute(insert_query, (name, phone, email, role, password))

            print('User created successfully')
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            print(f'Error in creating user: {e}')
            return jsonify({'message': 'Failed to create user'}), 500
        # finally:
        #     # Close cursor and connection
        #     self.cursor.close()
        #     self.conn.close()

    def user_update_model(self, data):
        try:
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            role = data.get('role')
            password = data.get('password')
            userid = data.get('id')
            print(userid)

            update_query = "Update Users set name=?, phone=?, email=?, role=?, password=? where id=?;"

            self.cursor.execute(update_query, (name, phone, email, role, password, userid))

            print('User Record updated successfully')
            if self.cursor.rowcount > 0:
                return jsonify({'message': "User Record Updated Successfully"}), 201
            else:
                return jsonify({"message": "No Records to Update. Please provide correct id."}), 202

        except Exception as e:
            print(f'Error in updating user: {e}')
            return jsonify({'message': 'Failed to update user'}), 204
        # finally:
        #     # Close cursor and connection
        #     self.cursor.close()
        #     self.conn.close()

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
        # finally:
        #     # Close cursor and connection
        #     self.cursor.close()
        #     self.conn.close()

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

        # finally:
        #     # Close cursor and connection
        #     self.cursor.close()
        #     self.conn.close()
