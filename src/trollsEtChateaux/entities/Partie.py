#!/usr/bin/python
# -*-coding:utf-8 -*

from trollsEtChateaux.entities.CoupInvalideDroite import CoupInvalideDroite
from trollsEtChateaux.entities.CoupInvalideGauche import CoupInvalideGauche
from trollsEtChateaux.entities.CoupInvalideSimultane import CoupInvalideSimultane

class Partie():
    """Partie de Trolls et Chateaux"""
    
    def __init__(self, nombreCases, stockInitial):
        """Cree une nouvelle partie
        - nombreCases : Nombre total de cases d'un chateau a l'autre
        - stockInitial : Nombre initial de pierres"""

        if(nombreCases % 2 != 1):
            raise Exception("Le nombre de cases doit etre un nombre impair")
        self.nombreCases = nombreCases
        self.positionTroll = nombreCases // 2
        
        self.stockInitial = stockInitial
        self.stockGauche = stockInitial
        self.stockDroite = stockInitial
        
        self.gagnant = 0
        self.coupsPrecedents = []


    def __copy__(self):
        """Constructeur de copie"""

        copie = type(self)(self.nombreCases, self.stockInitial)

        copie.nombreCases = self.nombreCases
        copie.positionTroll = self.positionTroll

        copie.stockInitial = self.stockInitial
        copie.stockGauche = self.stockGauche
        copie.stockDroite = self.stockDroite

        copie.gagnant = self.gagnant
        copie.coupsPrecedents = list(self.coupsPrecedents)

        return copie


    def copier(self):
        """Créer une copie de la partie"""
        return self.__copy__()


    def miroir(self):
        """Créer une copie inversée de la partie"""

        copie = type(self)(self.nombreCases, self.stockInitial)

        copie.nombreCases = self.nombreCases
        copie.positionTroll = self.nombreCases - self.positionTroll - 1

        copie.stockInitial = self.stockInitial
        copie.stockGauche = self.stockDroite
        copie.stockDroite = self.stockGauche

        if(self.gagnant == 0):
            copie.gagnant = self.gagnant
        else:
            copie.gagnant = 3 - self.gagnant

        copie.coupsPrecedents = list(map(lambda coup : (coup[1], coup[0]), self.coupsPrecedents))

        return copie


        
    def __repr__(self):
        """Fonction utilisée pour l'affichage"""
        
        return """----- Partie en cours -----
        
[Parametres initiaux]
    Nombre de cases : {0}
    Stock initial : {1}
    
[Etat de la partie]
    Position du troll : {2}
    Stock gauche : {3}
    Stock droite : {4}
    
[Coups precedents]
{5}
""".format(self.nombreCases, self.stockInitial, self.positionTroll, self.stockGauche, self.stockDroite, self.coupsPrecedents)
      


    def LigneResume(self):
        """Renvoyer une ligne qui resume l'etat de la partie"""

        longueur = len(str(self.stockInitial))
        return "[{0}] {1}#{2} [{3}]".format(str(self.stockGauche).rjust(longueur), "_" * self.positionTroll, "_" * (self.nombreCases - self.positionTroll - 1), str(self.stockDroite).rjust(longueur))



    def LigneDernierCoup(self):
        """Renvoyer une ligne qui presente les derniers coups joues"""

        longueur = len(str(self.stockInitial))
        gauche, droite = self.coupsPrecedents[len(self.coupsPrecedents)-1]
        return " {0}  {1}  {2} ".format(str(gauche).rjust(longueur), " " * self.nombreCases, str(droite).rjust(longueur))
 


    def tourDeJeu(self, nombreGauche, nombreDroite):
        """Jouer un tour de jeu
        - nombreGauche : Nombre de pierres lancees par le joueur de gauche
        - nombreDroite : Nombre de pierres lancees par le joueur de droite"""

        self.coupsPrecedents.append((nombreGauche, nombreDroite))

        invalideGauche = False
        invalideDroite = False

        messageCoupInvalideGauche = ""
        messageCoupInvalideDroite = ""

        if(nombreGauche == None):
            invalideGauche = True
            messageCoupInvalideGauche = "Le joueur de gauche n'a rien renvoyé"
        elif(type(nombreGauche) != type(1)):
            invalideGauche = True
            messageCoupInvalideGauche = "Le joueur de gauche a renvoyé autre chose qu'un nombre entier (valeur renvoyée : {0})".format(nombreGauche)
        elif(nombreGauche > self.stockGauche):
            invalideGauche = True
            messageCoupInvalideGauche = "Le joueur de gauche a renvoyé une valeur ({0}) supérieure à son nombre de pierres ({1})".format(nombreGauche, self.stockGauche)
        elif(nombreGauche < 1):
            invalideGauche = True
            messageCoupInvalideGauche = "Le joueur de gauche a renvoyé une valeur négative ou nulle ({0})".format(nombreGauche)

        if(nombreDroite == None):
            invalideDroite = True
            messageCoupInvalideDroite = "Le joueur de droite n'a rien renvoyé"
        elif(type(nombreDroite) != type(1)):
            invalideDroite = True
            messageCoupInvalideDroite = "Le joueur de droite a renvoyé autre chose qu'un nombre entier (valeur renvoyée : {0})".format(nombreDroite)
        elif(nombreDroite > self.stockDroite):
            invalideDroite = True
            messageCoupInvalideDroite = "Le joueur de droite a renvoyé une valeur ({0}) supérieure à son nombre de pierres ({1})".format(nombreDroite, self.stockDroite)
        elif(nombreDroite < 1):
            invalideDroite = True
            messageCoupInvalideDroite = "Le joueur de droite a renvoyé une valeur négative ou nulle ({0})".format(nombreDroite)
        
        if(invalideGauche):

            if(invalideDroite):
                raise CoupInvalideSimultane(messageCoupInvalideGauche + "\n" + messageCoupInvalideDroite)
            
            else:
                raise CoupInvalideGauche(messageCoupInvalideGauche)
        
        else:

            if(invalideDroite):
                raise CoupInvalideDroite(messageCoupInvalideDroite)
            
            else:
                self.stockGauche -= nombreGauche
                self.stockDroite -= nombreDroite    
                if(nombreGauche > nombreDroite):
                    self.positionTroll += 1
                elif(nombreGauche < nombreDroite):
                    self.positionTroll -= 1

                # Si le troll n'est pas dans un des chateaux mais qu'un des joueurs n'a plus de pierres, on vide les stocks de pierres
                if( ( (self.positionTroll != 0) and (self.positionTroll != self.nombreCases - 1) ) and ( (self.stockGauche == 0) or (self.stockDroite == 0) ) ):
                    self.__ViderStocks()

                partieTerminee = self.__PartieTerminee()
                return (partieTerminee, self.gagnant)



    def __ViderStocks(self):
        """Vider les stocks de pierre (fonction privee, utilisee uniquement quand l'un des deux joueurs n'a plus de pierres)"""

        if(self.stockGauche > 0):
            deplacement = min(self.stockGauche, self.nombreCases - self.positionTroll - 1)
            self.positionTroll += deplacement
            self.stockGauche -= deplacement

        if(self.stockDroite > 0):
            deplacement = min(self.stockDroite, self.positionTroll)
            self.positionTroll -= deplacement
            self.stockDroite -= deplacement



    def __PartieTerminee(self):
        """Tester si la partie est terminee (fonction privee, utilisee uniquement a la fin d'un tour de jeu)"""
        
        if(self.positionTroll == 0): # Le troll a atteint le chateau du joueur 1
            self.gagnant = 2
            return True

        elif(self.positionTroll == self.nombreCases - 1): # Le troll a atteint le chateau du joueur 2
            self.gagnant = 1
            return True

        elif((self.stockGauche == 0) or (self.stockDroite == 0)): # Au moins l'un des deux joueurs n'a plus de pierres
            if(self.positionTroll < self.nombreCases // 2):
                self.gagnant = 2
            elif(self.positionTroll > self.nombreCases // 2):
                self.gagnant = 1
            return True
        
        else:
            return False

