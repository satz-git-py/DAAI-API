# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 12:07:25 2021

@author: S@tZ
"""

from flask import Flask
from .customers.routes import customer
from config import config

def create_app(apps_config='development'):
    app = Flask(__name__)
    app.config.from_object(config[apps_config])
    app.register_blueprint(customer)
    
    return app