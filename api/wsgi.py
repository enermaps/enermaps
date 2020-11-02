"""WSGI entrypoint for production run
"""
from app import create_app

app = create_app()
