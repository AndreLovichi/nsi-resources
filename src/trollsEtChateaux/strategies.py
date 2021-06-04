#!/usr/bin/python
# -*-coding:utf-8 -*

import random

def strategieExemple1(partie, partiesPrecedentes):
    stockActuel = partie.stockGauche
    return min(2, stockActuel)

def strategieExemple2(partie, partiesPrecedentes):
    stockActuel = partie.stockGauche
    nombreAleatoire = random.randint(1, 4)
    return min(nombreAleatoire, stockActuel)

def strategieExemple3(partie, partiesPrecedentes):
    stockActuel = partie.stockGauche
    nombreAleatoire = random.randint(1, 6)
    return min(nombreAleatoire, stockActuel)
