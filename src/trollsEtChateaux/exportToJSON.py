#!/usr/bin/python
# -*-coding:utf-8 -*

import json
from trollsEtChateaux import *
from trollsEtChateaux.rankings import *

class StrategyEncoder(json.JSONEncoder):
    """Encodeur JSON pour la classe Strategie"""

    def default(self, obj):
        if isinstance(obj, list):
            return [StrategyEncoder.default(self, item) for item in obj]
        if isinstance(obj, Strategie):    
            return {
                'name': obj.nom,
                'finalRank': obj.rangFinal,
                'pointTotal': obj.totalPoints,
                'scoreTotal': obj.totalScores,
                'rankings': [RankingEncoder.default(self, classement) for classement in obj.classements]
            }
        return json.JSONEncoder.default(self, obj)


class RankingEncoder(json.JSONEncoder):
    """Encodeur JSON pour la classe Classement"""
    
    def default(self, obj):
        if isinstance(obj, Classement):
            return {
                'rank': obj.rang,
                'points': obj.points,
                'victoryCount': obj.victoires,
                'defeatCount': obj.defaites,
                'drawCount': obj.matchsNuls,
                'invalidMoveCount': obj.coupsInvalides,
                'score': obj.score,
                'battles': [MatchEncoder.default(self, affrontement) for affrontement in obj.affrontements]
            }
        return json.JSONEncoder.default(self, obj)


class MatchEncoder(json.JSONEncoder):
    """Encodeur JSON pour les tuples correspondants à un affrontement"""
    
    def default(self, obj):
        if isinstance(obj, tuple):
            strategieAdverse = obj[0]
            resultats = obj[1]
            return {
                'opponent': strategieAdverse,
                'expectedMatchCount': resultats.matchPrevus,
                'matchCount': resultats.matchJoues,
                'victoryCount': resultats.victoiresGauche,
                'defeatCount': resultats.victoiresDroite,
                'drawCount': resultats.matchsNuls,
                'winner': resultats.gagnant
            }
        return json.JSONEncoder.default(self, obj)

def genererJSON(listeStrategies, nomDuFichier = "classements.json"):
    """Generer le code JSON correspondant aux résultats"""  

    nbStrategies = len(listeStrategies)

    # Calcul du classement partie pour chaque configuration
    calculerClassement(listeStrategies, 7, 15)
    calculerClassement(listeStrategies, 7, 30)
    calculerClassement(listeStrategies, 15, 30)
    calculerClassement(listeStrategies, 15, 50)

    # Calcul du classement general
    calculerClassementGeneral(listeStrategies)

    # Extraction des résultats à sérialiser
    resultatsJson = json.dumps(listeStrategies, cls = StrategyEncoder)

    # Le code JSON est stocké dans un fichier plat    
    fichier = open(nomDuFichier, "w")
    fichier.writelines(resultatsJson)
    fichier.close()


