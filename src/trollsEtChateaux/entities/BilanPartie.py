#!/usr/bin/python
# -*-coding:utf-8 -*

class BilanPartie:
    """Bilan d'une partie de Trolls et Chateaux
    - gagnant : Gagnant
    - message : Message resumant la partie
    - exception : Eventuelle exception levee
    - partie : Details de la partie"""

    def __init__(self, gagnant, message, exception, partie):
        """Creer un bilan de partie
        - gagnant : Gagnant
        - message : Message resumant la partie
        - exception : Eventuelle exception levee
        - partie : Details de la partie"""
        self.gagnant = gagnant
        self.message = message
        self.exception = exception
        self.partie = partie

    def __repr__(self):
        """Fonction utilisee pour l'affichage"""
        print(self.partie)
