"""Redirect / to /api

As we expect all api access to go trough /api and the / is shielded
by the reverse proxy, we redirect / to /api.
"""
from flask import Blueprint, redirect

redirect_to_api = Blueprint("redirect_to_api", __name__)


@redirect_to_api.route("/")
def root_redirect():
    return redirect("/api")
