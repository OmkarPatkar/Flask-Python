import os.path

from app import app
from model.user_model import user_model
from flask import request, jsonify
from datetime import datetime

obj = user_model()


@app.route("/user/getall")
def user_getall_controller():
    return obj.user_getall_model()


@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    data = request.form
    return obj.user_addone_model(data)


@app.route("/user/update", methods=["PUT"])
def user_update_controller():
    data = request.form
    return obj.user_update_model(data)


@app.route("/user/delete/<int:id>", methods=["DELETE"])
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

        unique_filename = str(datetime.now().timestamp()).replace('.', '')
        filename_with_extension = f"{unique_filename}.{file.filename.split('.')[-1]}"
        print(filename_with_extension)
        file_with_path = os.path.join(upload_dir, filename_with_extension)
        file.save(file_with_path)
        obj.user_upload_avatar_model(uid, file_with_path)

        return jsonify({'message': 'File uploaded successfully', 'filename': filename_with_extension}), 200

    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500

