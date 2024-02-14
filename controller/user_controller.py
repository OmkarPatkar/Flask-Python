from app import app
from model.user_model import user_model
from flask import request

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
