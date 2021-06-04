#!/usr/bin/python
# -*-coding:utf-8 -*

class CoupInvalideSimultane(Exception):
    """Exception levee lorsque les deux joueurs proposent simultanément un coup invalide"""
    
    def __init__(self, message = "Coups invalides simultanés"):
        Exception.__init__(self, message)
