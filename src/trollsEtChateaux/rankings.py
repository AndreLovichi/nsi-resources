#!/usr/bin/python
# -*-coding:utf-8 -*

import logging
from logging.handlers import RotatingFileHandler
import time
from trollsEtChateaux import *

def calculerClassement(listeStrategies, nombreCases, stockInitial):
    """Calculer le classement pour une liste de strategies
    - listeStrategies : liste des strategies qui participent au concours
    - nombreCases : nombre de cases entre les deux chateaux
    - stockInitial : stock initial de pierres"""

    nbStrategies = len(listeStrategies)

    # On cree un logger
    logger = logging.getLogger()
    if(len(logger.handlers) == 0):
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(message)s')
        file_handler = RotatingFileHandler('troll.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # On verifie que les compteurs sont bien tous nuls
    for i in range(nbStrategies):
        listeStrategies[i].remettreAZero()


    # Ensuite, pour chaque couple de strategies,
    for i in range(nbStrategies):
        strategieGauche = listeStrategies[i]
        
        for j in range(i+1, nbStrategies):
            strategieDroite = listeStrategies[j]

            log = "Début de l'affrontement {0} VS {1} pour {2} cases et {3} pierres".format(strategieGauche.nom, strategieDroite.nom, nombreCases, stockInitial)
            message = time.asctime(time.localtime()) + " | " + log
          
            print(message)
            logger.info(log)

            # On organise 1000 recontres
            resultats = jouerPlusieursParties(nombreCases, stockInitial, strategieGauche.fonction, strategieDroite.fonction, 1000, False)

            # On met a jour les compteurs de la strategie de gauche
            strategieGauche.appliquerResultats(resultats)
            strategieGauche.affrontements.append((strategieDroite.nom, resultats))

            # On met a jour les compteurs de la strategie de droite
            miroir = resultats.miroir()
            strategieDroite.appliquerResultats(miroir)
            strategieDroite.affrontements.append((strategieGauche.nom, miroir))

            logger.info("Fin de l'affrontement %s VS %s", strategieGauche.nom, strategieDroite.nom)


    # On met a jour les totaux
    for i in range(nbStrategies):
        listeStrategies[i].completerListePoints()

    # On trie les strategiess
    listeStrategies.sort()
    listeStrategies.reverse()

    # On stocke ce classement pour chaque strategie
    for i in range(nbStrategies):
        strategie = listeStrategies[i]
        classement = Classement(i+1, strategie.points, strategie.victoires, strategie.defaites, strategie.matchsNuls, strategie.coupsInvalides, strategie.score, list(strategie.affrontements))    
        strategie.classements.append(classement)


def calculerClassementGeneral(listeStrategies):
    """Calculer le classement general pour une liste de strategies
    - listeStrategies : liste des strategies qui participent au concours"""

    # Pour chaque strategie,
    for i in range(len(listeStrategies)):
        strat = listeStrategies[i]

        # On verifie que les compteurs sont bien nuls
        strat.remettreAZero()

        totalPoints = 0
        totalScores = 0

        # Puis on calcule la somme des points (et des scores)
        for j in range(len(strat.listePoints)):
            points, score = strat.listePoints[j]
            totalPoints += points
            totalScores += score

        # Et on definit ainsi les nouveaux points et scores pour le classement general
        strat.totalPoints = totalPoints
        strat.totalScores = totalScores

    # On trie les strategies
    listeStrategies.sort()
    listeStrategies.reverse()

    # Et on obtient le rang final pour chaque strategie
    for i in range(len(listeStrategies)):
        listeStrategies[i].rangFinal = i+1
