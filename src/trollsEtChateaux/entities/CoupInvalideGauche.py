#!/usr/bin/python
# -*-coding:utf-8 -*

class CoupInvalideGauche(Exception):
    """Exception levee lorsque le joueur de gauche propose un coup invalide"""
    
    def __init__(self, message = "Coup invalide du joueur de gauche"):
        Exception.__init__(self, message)    
