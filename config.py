# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 18:42:06 2021

@author: Sathish
"""

class Config(object):
    TESTING=False
    DEBUG=False
    
class Production(Config):
    TESTING=False
    DEBUG=False
    SECRET_KEY='thisismysecretkey'

class Development(Config):
    DEBUG=True
    SERVER_NAME='localhost:5000'
    SECRET_KEY='thisismysecretkey'
    
class Testing(Config):
    TESTING=True
    SERVER_NAME='localhost:5000'
    
    
config = {
        'development':Development,
        'testing':Testing,
        'production':Production
    }
    
