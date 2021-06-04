#!/usr/bin/python
# -*-coding:utf-8 -*

class CoupInvalideDroite(Exception):
    """Exception levee lorsque le joueur de droite propose un coup invalide"""
    
    def __init__(self, message = "Coup invalide du joueur de droite"):
        Exception.__init__(self, message)
