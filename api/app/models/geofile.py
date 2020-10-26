"""Description of each set of gis informations.
"""
import os

from flask import current_app, safe_join


def get_user_upload(user="user"):
    user_dir = safe_join(current_app.config["UPLOAD_DIR"], user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir
