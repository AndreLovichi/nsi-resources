#!/usr/bin/python
# -*-coding:utf-8 -*

from trollsEtChateaux.entities.CoupInvalideDroite import CoupInvalideDroite
from trollsEtChateaux.entities.CoupInvalideGauche import CoupInvalideGauche
from trollsEtChateaux.entities.CoupInvalideSimultane import CoupInvalideSimultane

class ResultatSimulation:
    """Resultat d'une simulation entre deux strategies
    - matchsPrevus : Nombre de matchs prevus
    - matchsJoues : Nombre de matchs joues
    - victoiresGauche : Nombre de matchs remportes par le joueur de gauche
    - victoiresDroite : Nombre de matchs remportes par le joueur de droite
    - matchsNuls : Nombre de matchs nuls
    - gagnant : Gagnant
    - message : Message resumant la simulation
    - exception : Eventuelle exception rencontree"""


    def __init__(self, matchPrevus, matchJoues, victoiresGauche, victoiresDroite, matchsNuls, gagnant, message, exception):
        """Creer les resultats pour une simulation entre deux strategies
        - matchsPrevus : Nombre de matchs prevus
        - matchsJoues : Nombre de matchs joues
        - victoiresGauche : Nombre de matchs remportes par le joueur de gauche
        - victoiresDroite : Nombre de matchs remportes par le joueur de droite
        - matchsNuls : Nombre de matchs nuls
        - gagnant : Gagnant
        - message : Message resumant la simulation
        - exception : Eventuelle exception rencontree"""

        self.matchPrevus = matchPrevus
        self.matchJoues = matchJoues
        self.victoiresGauche = victoiresGauche
        self.victoiresDroite = victoiresDroite
        self.matchsNuls = matchsNuls
        self.gagnant = gagnant
        self.message = message
        self.exception = exception


    def __repr__(self):
        """Fonction utilisee pour l'affichage"""

        return """----- Resultats de la simulation -----
        
Matchs prevus : {0}
Matchs joues : {1}

Victoires du joueur de gauche : {2}
Victoires du joueur de droite : {3}
Matchs nuls : {4}

{5}""".format(self.matchPrevus, self.matchJoues, self.victoiresGauche, self.victoiresDroite, self.matchsNuls, self.message)

    def miroir(self):
        """Calcule le miroir des resultats d'une simulation"""

        m = ResultatSimulation(self.matchPrevus, self.matchJoues, self.victoiresDroite, self.victoiresGauche, self.matchsNuls, self.gagnant, self.message, self.exception)

        if(m.gagnant != 0):
            m.gagnant = 3 - m.gagnant
            if(m.exception == None):
                if(m.gagnant == 1):
                    m.message = "Victoire du joueur de gauche !"
                if(m.gagnant == 2):
                    m.message = "Victoire du joueur de droite !"

        if(type(m.exception) == CoupInvalideDroite):
            m.message = "Victoire du joueur de droite ! Le joueur de gauche a propose un coup invalide"
            m.exception = CoupInvalideGauche()
        elif(type(m.exception) == CoupInvalideGauche):
            m.message = "Victoire du joueur de gauche ! Le joueur de droite a propose un coup invalide"
            m.exception = CoupInvalideDroite()

        return m
