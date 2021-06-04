#!/usr/bin/python
# -*-coding:utf-8 -*

from trollsEtChateaux.entities.CoupInvalideDroite import CoupInvalideDroite
from trollsEtChateaux.entities.CoupInvalideGauche import CoupInvalideGauche
from trollsEtChateaux.entities.CoupInvalideSimultane import CoupInvalideSimultane

class Strategie:
    """Strategie participant au concours Trolls et chateaux"""

    def __init__(self, nom, fonction):
        """Declarer une nouvelle strategie
        - nom : Nom de la strategie
        - fonction : Fonction decrivant la strategie"""
        self.nom = nom
        self.fonction = fonction

        self.points = 0
        self.victoires = 0
        self.defaites = 0
        self.matchsNuls = 0
        self.coupsInvalides = 0
        self.score = 0

        self.affrontements = []

        self.listePoints = []
        self.totalPoints = 0
        self.totalScores = 0
        self.rangFinal = 0

        self.classements = []


    def remettreAZero(self):
        """Remettre a zero les compteurs pour une strategie"""
        self.points = 0
        self.victoires = 0
        self.defaites = 0
        self.matchsNuls = 0
        self.coupsInvalides = 0
        self.score = 0
        self.totalScores = 0
        self.totalPoints = 0
        self.rangFinal = 0
        self.affrontements.clear()


    def completerListePoints(self):
        """Ajouter les valeurs courantes dans les totaux"""
        self.listePoints.append((self.points, self.score))


    def appliquerResultats(self, resultats):
        """Appliquer les resultats d'une simulation pour mettre a jour les compteurs"""

        # On regarde s'il y a eu un coup invalide
        if( (type(resultats.exception) == CoupInvalideGauche) or (type(resultats.exception) == CoupInvalideSimultane) ):
            self.coupsInvalides += 1
            self.points -= 1

        else:
            self.score += resultats.victoiresGauche - resultats.victoiresDroite

            if(resultats.gagnant == 0):
                self.matchsNuls += 1
                self.points += 1

            elif(resultats.gagnant == 1):
                self.victoires += 1
                self.points += 3

            elif(resultats.gagnant == 2):
                self.defaites += 1


    def __lt__(self, autreResultats):
        """Operateur de comparaison (utilise pour les tris)"""
        if (self.totalPoints != autreResultats.totalPoints):
            return self.totalPoints < autreResultats.totalPoints
        elif (self.totalScores != autreResultats.totalScores):
            return self.totalScores < autreResultats.totalScores
        elif (self.points != autreResultats.points):
            return self.points < autreResultats.points
        else:
            return self.score < autreResultats.score


    def __repr__(self):
        """Fonction utilisee pour l'affichage"""

        s = """\nNom : {0}
Points : {1}
Victoires : {2}
Defaites : {3}
Match nuls : {4}
Coups invalides : {5}
Score : {6}\n""".format(self.nom, self.points, self.victoires, self.defaites, self.matchsNuls, self.coupsInvalides, self.score)

        return s