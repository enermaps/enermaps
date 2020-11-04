import os

from flask import Blueprint, Flask, redirect
from flask_restx import Api

from app.endpoints import cm, geofile, wms

redirect_to_api = Blueprint("redirect_to_api", __name__)


@redirect_to_api.route("/")
def root_redirect():
    return redirect("/api")
