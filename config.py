"""
TODO: make flask look in a .gitignored config file and create one 
if not exists
"""
import os
from flask import current_app

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    admin = {
        "username": "adminpapi",
        "password": "password"
    }