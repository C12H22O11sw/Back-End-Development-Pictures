from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


def find_picture(id):
    global data
    for picture in data:
        if picture['id'] == id:
            return picture
    return None

def find_picture_id(id):
    global data
    for i, picture in enumerate(data):
        if picture['id'] == id:
            return i
    return None

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        picture = find_picture(id)
        if picture is None:
            return {"message": "Invalid ID"}, 404
        return picture, 200
    except Excteption as e:
        return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        picture = request.json
        id = picture['id']
        if find_picture(id):
            return {"Message": f"picture with id {id} already present"}, 302
        data.append(picture)
        return picture, 201
    except Exception as e:
        return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        global data
        picture = find_picture(id)
        if picture is None:
            return {"message": "picture not found"}, 404
        for key in request.json:
            picture[key] = request.json[key]
        return picture, 201
    except Exception as e:
        return {"message": f"Internal server error{e}"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        global data
        picture = find_picture(id)
        if picture is None:
            return {"message": "picture not found"}, 404
        data.remove(picture)
        return {}, 204
    except Exception as e:
        return {"message": f"Internal server error{e}"}, 500
        
