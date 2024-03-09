import os.path

from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, jsonify, send_from_directory
from datetime import datetime

obj = user_model()
auth = auth_model()


@app.route("/user/getall")
@auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()


@app.route("/user/addone", methods=["POST"])
@auth.token_auth()
def user_addone_controller():
    data = request.form
    return obj.user_addone_model(data)

@app.route("/user/addmultiple", methods=["POST"])
# @auth.token_auth()
def user_addmultiple_controller():
    data = request.json
    return obj.user_addmultiple_model(data)


@app.route("/user/update", methods=["PUT"])
@auth.token_auth()
def user_update_controller():
    data = request.form
    return obj.user_update_model(data)


@app.route("/user/delete/<int:id>", methods=["DELETE"])
@auth.token_auth()
def user_delete_controller(id):
    return obj.user_delete_model(id)


@app.route("/user/patch/<int:id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)


@app.route("/user/get_records/limit/<int:limit>/page/<int:page>", methods=["GET"])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)


@app.route("/user/<int:uid>/upload/avatar", methods=["PUT"])
def user_upload_avatar_controller(uid):
    try:
        if not request.files:
            return jsonify({'error': 'No file in the request'}), 400

        file = request.files['avatar']
        print(file)

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # create unique name using timestamp
        unique_filename = str(datetime.now().timestamp()).replace('.', '')
        # create filename with extension
        filename_with_extension = f"{unique_filename}.{file.filename.split('.')[-1]}"
        print(filename_with_extension)
        # absolute path for the file
        file_with_path = os.path.join(upload_dir, filename_with_extension)
        # print(file_with_path)
        # save the file
        file.save(file_with_path)
        # upload the file to database
        obj.user_upload_avatar_model(uid, file_with_path)

        return jsonify({'message': 'File uploaded successfully', 'filename': filename_with_extension}), 200

    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500


@app.route("/uploads/<string:filename>")
def user_getavatar_controller(filename):
    try:
        return send_from_directory("./uploads", filename)
    except Exception as e:
        return jsonify({'error': 'File not present. Please enter valid file name.'}), 400


@app.route("/user/login", methods=["POST"])
def user_login_controller():
    return obj.user_login_model(request.form)
