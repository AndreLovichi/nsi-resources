#!/usr/bin/python
# -*-coding:utf-8 -*

import tkinter
import random
import threading
import time
import logging
import traceback
import json
from logging.handlers import RotatingFileHandler

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

      invalideGauche = False;
      invalideDroite = False;

      messageCoupInvalideGauche = "";
      messageCoupInvalideDroite = "";

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



def jouerPartie(nombreCases, stockInitial, strategie1, strategie2, partiesPrecedentes = [], partiesPrecedentesMiroir = [], affichageTexte = True):
   """Jouer une partie entre deux strategies
   - nombreCases : Nombre de cases
   - stockInitial : Nombre initial de pierres
   - strategie1 : Strategie du joueur de gauche
   - strategie2 : Strategie du joueur de droite
   - partiesPrecedentes : Liste des parties precedentes
   - partiesPrecedentes : Liste des parties precedentes (version miroir)
   - affichageTexte : Indique s'il faut afficher le deroulement de la partie dans la console"""

   partie = Partie(nombreCases, stockInitial)
   partieEnCours = True
   gagnant = 0
   message = "" 
   exception = None

   # On cree une copie de la partie pour chaque joueur (pour eviter de passer en reference la partie en cours)
   partieGauche = partie.copier()
   partieDroite = partie.miroir()

   while(partieEnCours):

      if(affichageTexte):
         print(partie.LigneResume())

      try:

         exceptionGauche = False
         exceptionDroite = False

         exceptionGaucheMessage = ""
         exceptionDroiteMessage = ""

         try:
            nombreGauche = strategie1(partieGauche, partiesPrecedentes)
         except:
            exceptionGauche = True
            stackTrace = traceback.format_exc()
            exceptionGaucheMessage = "Une erreur est survenue dans la fonction du joueur de gauche : \n{0}".format(stackTrace)

         try:            
            nombreDroite = strategie2(partieDroite, partiesPrecedentesMiroir)
         except:
            exceptionDroite = True
            stackTrace = traceback.format_exc()
            exceptionDroiteMessage = "Une erreur est survenue dans la fonction du joueur de droite : \n{0}".format(stackTrace)

         if(exceptionGauche):
            if(exceptionDroite):
               raise CoupInvalideSimultane(exceptionGaucheMessage + "\n" + exceptionDroiteMessage)
            else:
               raise CoupInvalideGauche(exceptionGaucheMessage)
         else:
            if(exceptionDroite):
               raise CoupInvalideDroite(exceptionDroiteMessage)

         (partieTerminee, gagnant) = partie.tourDeJeu(nombreGauche, nombreDroite)

         partieGauche.tourDeJeu(nombreGauche, nombreDroite)
         partieDroite.tourDeJeu(nombreDroite, nombreGauche)


      except CoupInvalideSimultane as e:
         message = "Match nul ! Les deux joueurs ont propose un coup invalide" + "\n{0}".format(str(e))
         exception = e
         partieEnCours = False

      except CoupInvalideGauche as e:
         gagnant = 2
         message = "Victoire du joueur de droite ! Le joueur de gauche a propose un coup invalide" + "\n{0}".format(str(e))
         exception = e
         partieEnCours = False

      except CoupInvalideDroite as e:
         gagnant = 1
         message = "Victoire du joueur de gauche ! Le joueur de droite a propose un coup invalide" + "\n{0}".format(str(e))
         exception = e
         partieEnCours = False

      else:       

         if(partieTerminee):
            partieEnCours = False                      
            if(gagnant == 1):
               message = "Victoire du joueur de gauche !"
            elif(gagnant == 2):
               message = "Victoire du joueur de droite !"
            else:
               message = "Match nul ! Le troll est au milieu du chemin"
      
      finally : 

         if(affichageTexte and (partie.coupsPrecedents != [])):
            print(partie.LigneDernierCoup())


   if(affichageTexte):
      print(partie.LigneResume())     
      print(message)
               
   return BilanPartie(gagnant, message, exception, partie)



def jouerPlusieursParties(nombreCases, stockInitial, strategie1, strategie2, nombreDeParties = 1000, afficherResultats = True, afficherParties = False):
   """Jouer plusieurs parties entre deux strategies
   - nombreCases : Nombre de cases
   - stockInitial : Nombre initial de pierres
   - strategie1 : Strategie du joueur de gauche
   - strategie2 : Strategie du joueur de droite
   - nombreDeParties : Nombre de parties a jouer (par defaut 1000)"""

   partiesTerminees = []
   partiesTermineesMiroir = []
   victoiresGauche = 0
   victoiresDroite = 0
   matchsNuls = 0
   gagnant = 0
   message = ""
   exception = None

   for i in range(nombreDeParties):
      
      bilan = jouerPartie(nombreCases, stockInitial, strategie1, strategie2, partiesTerminees, partiesTermineesMiroir, afficherParties)     
      
      # Gestion des exceptions
      if(type(bilan.exception) == CoupInvalideSimultane):
         message = bilan.message
         exception = CoupInvalideSimultane()
         break 

      if(type(bilan.exception) == CoupInvalideGauche):
         message = bilan.message
         gagnant = 2
         exception = CoupInvalideGauche()
         break 

      if(type(bilan.exception) == CoupInvalideDroite):
         message = bilan.message
         gagnant = 1
         exception = CoupInvalideDroite()
         break 


      # Mise a jour des compteurs
      if(bilan.gagnant == 0):
         matchsNuls += 1

      if(bilan.gagnant == 1):
         victoiresGauche += 1

      if(bilan.gagnant == 2):
         victoiresDroite += 1

      partiesTerminees.append(bilan.partie)
      partiesTermineesMiroir.append(bilan.partie.miroir())


   # Si aucun coup invalide n'a ete joue, le gagnant  est le joueur qui a remporte le plus de matchs
   if(exception == None):

      if(victoiresGauche > victoiresDroite):
         gagnant = 1
         message = "Victoire du joueur de gauche !"

      if(victoiresGauche < victoiresDroite):
         gagnant = 2
         message = "Victoire du joueur de droite !"


   # Creation d'un objet ResultatsSimulation
   resultats = ResultatSimulation(nombreDeParties, i+1, victoiresGauche, victoiresDroite, matchsNuls, gagnant, message, exception)

   if(afficherResultats):
      print(resultats)

   return resultats



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




class CoupInvalideGauche(Exception):
   """Exception levee lorsque le joueur de gauche propose un coup invalide"""
   
   def __init__(self, message = "Coup invalide du joueur de gauche"):
      Exception.__init__(self, message)   

      

class CoupInvalideDroite(Exception):
   """Exception levee lorsque le joueur de droite propose un coup invalide"""
   
   def __init__(self, message = "Coup invalide du joueur de droite"):
      Exception.__init__(self, message)
   


class CoupInvalideSimultane(Exception):
   """Exception levee lorsque les deux joueurs proposent simultanement un coup invalide"""
   
   def __init__(self, message = "Coups invalides simultanés"):
      Exception.__init__(self, message)


class GUI(tkinter.Tk):
   """Fenêtre graphique pour l'affichage d'une partie de Trolls et Chateaux"""

   def __init__(self, nombreCases, stockInitial, strategieGauche, strategieDroite, tempsAttente = 1000, parent = None, largeur = 800, hauteur = 200, marge = 10, title = "Troll et chateaux"):
      """Créer une fenêtre graphique pour l'affichage d'une partie de Trolls et Chateaux
   - nombreCases : Nombre de cases
   - stockInitial : Nombre initial de pierres
   - strategie1 : Strategie du joueur de gauche
   - strategie2 : Strategie du joueur de droite"""

      tkinter.Tk.__init__(self, parent)
      self.parent = parent

      self.largeur = largeur
      self.hauteur = hauteur
      self.marge = marge
      self.tempsAttente = tempsAttente
      
      self.nombreCases = nombreCases
      self.stockInitial = stockInitial
      self.strategieGauche = strategieGauche
      self.strategieDroite = strategieDroite
      self.partie = Partie(nombreCases, stockInitial)
      self.partieEnCours = False
      self.partieTerminee = False
      self.message = ""

      self.title(title)

      nomStrategieGauche = strategieGauche.nom
      self.labelGauche = tkinter.Label(self, text=nomStrategieGauche, justify="left", font=("Helvetica", 18))
      self.labelGauche.grid(row = 0, column = 0, sticky = "W", padx=10, pady=10)

      nomStrategieDroite = strategieDroite.nom
      self.labelDroite = tkinter.Label(self, text=nomStrategieDroite, justify="left", font=("Helvetica", 18))
      self.labelDroite.grid(row = 0, column = 2, sticky = "E", padx=10, pady=10)

      textLabelGauche = "Stock gauche : {0}".format(stockInitial)
      self.labelGauche = tkinter.Label(self, text="   Stock gauche : 20", justify="left", font=("Helvetica", 16))
      self.labelGauche.grid(row = 1, column = 0, sticky = "W", padx=10, pady=10)

      textLabelDroite = "Stock droite : {0}".format(stockInitial)
      self.labelDroite = tkinter.Label(self, text="Stock droite : 20   ", justify="right", font=("Helvetica", 16))
      self.labelDroite.grid(row = 1, column = 2, sticky = "E", padx=10, pady=10)

      self.canvas = tkinter.Canvas(self, width = largeur, height = hauteur, bg="white")
      self.canvas.grid(row = 2, columnspan = 3)
      self.tracerPlateau()

      self.boutonGauche = tkinter.Button(self, text="Lancer la partie", command = self.lancer, font=("Helvetica", 16))
      self.boutonGauche.grid(row = 3, column = 0, sticky = "W", padx=10, pady=10)

      self.boutonQuitter = tkinter.Button(self, text="Quitter", command = self.quitter, font=("Helvetica", 16))
      self.boutonQuitter.grid(row = 3, column = 2, sticky = "E", padx=10, pady=10)

      self.labelMessage = tkinter.Label(self, text = self.message, justify="center", font=("Helvetica", 16))
      self.labelMessage.grid(row = 3, column = 1, padx=10, pady=10)

      self.mainloop()


   def tracerPlateau(self):
      """Trace du plateau"""

      self.canvas.delete("all")

      # Calcul des coordonnees
      largeurDispo = self.largeur - 2*self.marge
      tailleCase = largeurDispo // self.nombreCases
      x0 = (self.largeur - tailleCase*self.nombreCases) // 2
      y0 = (self.hauteur - tailleCase) // 2

      # Trace des chateaux
      self.canvas.create_rectangle(x0, y0, x0+tailleCase, y0+tailleCase, fill="blue")
      self.canvas.create_rectangle(x0 + (self.nombreCases-1)*tailleCase, y0, x0+self.nombreCases*tailleCase, y0+tailleCase, fill="red")

      # Trace du troll
      positionTroll = self.partie.positionTroll
      self.canvas.create_rectangle(x0 + positionTroll*tailleCase, y0, x0+(positionTroll+1)*tailleCase, y0+tailleCase, fill="green")
      
      # Trace des cases
      self.canvas.create_line(x0, y0, x0 + tailleCase * self.nombreCases, y0, fill="black", width = 4)
      self.canvas.create_line(x0, y0+tailleCase, x0 + tailleCase * self.nombreCases, y0+tailleCase, fill="black", width = 4)
      for i in range(self.nombreCases + 1):
         self.canvas.create_line(x0 + i*tailleCase, y0, x0 + i*tailleCase, y0+tailleCase, fill="black", width = 4) 
      
      # Mise a jour des stocks
      textLabelGauche = "Stock gauche : {0}".format(self.partie.stockGauche)
      textLabelDroite = "Stock droite : {0}".format(self.partie.stockDroite)
      self.labelGauche["text"] = textLabelGauche
      self.labelDroite["text"] = textLabelDroite



   def lancer(self):
      """Lancer une partie"""

      # On prepare une nouvelle partie
      self.partie = Partie(self.nombreCases, self.stockInitial)
      self.partieEnCours = True
      self.partieTerminee = False

      # On desactive temporairement le bouton "Lancer la partie" / "Recommencer"
      self.boutonGauche["state"] = "disabled"
      self.message = "" 
      self.labelMessage["text"] = ""

      # On trace le plateau
      self.tracerPlateau()

      # On joue un coup (cette fonction va se rappeller elle-meme tant que la partie continue)
      self.after(self.tempsAttente, self.jouerUnCoup)



   def jouerUnCoup(self):

      # On cree une copie de la partie pour chaque joueur (pour eviter de passer en reference la partie en cours)
      partieGauche = self.partie.copier()
      partieDroite = self.partie.miroir()

      try:

         nombreGauche = self.strategieGauche.fonction(partieGauche, [])
         nombreDroite = self.strategieDroite.fonction(partieDroite, [])

         (partieTerminee_, gagnant_) = self.partie.tourDeJeu(nombreGauche, nombreDroite)

      except CoupInvalideSimultane:
         self.message = "Match nul ! Les deux joueurs ont propose un coup invalide"
         self.partieEnCours = False

      except CoupInvalideGauche:
         self.message = "Victoire du joueur de droite ! Le joueur de gauche a propose un coup invalide"
         self.partieEnCours = False

      except CoupInvalideDroite:
         self.message = "Victoire du joueur de gauche ! Le joueur de droite a propose un coup invalide"
         self.partieEnCours = False
      
      else:

         if(partieTerminee_):
            self.partieEnCours = False                      
               
            if(gagnant_ == 1):
               self.message = "Victoire de \"" + self.strategieGauche.nom + "\" !"
            elif(gagnant_ == 2):
               self.message = "Victoire de \"" + self.strategieDroite.nom + "\" !"
            else:
               self.message = "Match nul ! Le troll est au milieu du chemin"

      finally : 

         self.tracerPlateau()

         if(self.partieEnCours):
            self.after(self.tempsAttente, self.jouerUnCoup)
         else:
            self.partieTerminee = True
            self.labelMessage["text"] = self.message
            self.boutonGauche["state"] = "active"
            self.boutonGauche["text"] = "Recommencer"




   def quitter(self):
      """Quitter la fenêtre graphique"""

      self.quit()




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


class Classement:
   """Classement obtenu par une strategie sur une configuration"""

   def __init__(self, rang, points, victoires, defaites, matchsNuls, coupsInvalides, score, affrontements):
      """Declarer un nouveau classement
      - rang : Rang
      - points : Nombre de points
      - victoires : Nombre de victoires
      - defaites : Nombre de défaites
      - matchsNuls : Nombre de matchs nuls
      - coupsInvalides : Nombre de coups invalides
      - score : Score
      - affrontements : Détails des affrontements
      """
      self.rang = rang
      self.points = points
      self.victoires = victoires
      self.defaites = defaites
      self.matchsNuls = matchsNuls
      self.coupsInvalides = coupsInvalides
      self.score = score
      self.affrontements = affrontements


class JSONStrategie:

   def __init__(self, strategie):
      self.nom = strategie.nom
      self.rangFinal = strategie.rangFinal
      self.totalPoints = strategie.totalPoints
      self.totalScores = strategie.totalScores
      self.classements = strategie.classements


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

   

def genererHTML(listeStrategies):
   """Generer le code HTML de la page contenant les resultats"""  

   nbStrategies = len(listeStrategies)

   # Le code HTML va etre genere dans un fichier plat   
   fichier = open("classements.html", "w")


   # Fonction auxiliaire utilisee pour l'affichage
   def genererHTMLpartiel(nombreCases, stockInitial):
      
      # On calcule le classement
      calculerClassement(listeStrategies, nombreCases, stockInitial)
      listeStrategies.sort()
      listeStrategies.reverse()


      # On affiche le titre et le debut du tableau
      header = """            <!-- ----- Debut du classement pour {cases} cases et {pierres} pierres ----- -->

            <h2 id="classement_{cases}_{pierres}">{cases} cases et {pierres} pierres</h2>

            <table class="table table-hover">

                <thead>
                    <tr>
                        <th>#</th>
                        <th>Stratégie</th>
                        <th>Points</th>
                        <th class="hidden-sm hidden-xs">Victoires</th>
                        <th class="hidden-sm hidden-xs">Défaites</th>
                        <th class="hidden-sm hidden-xs">Matchs nuls</th>
                        <th class="hidden-sm hidden-xs">Coups invalides</th>
                        <th class="hidden-sm hidden-xs">Score total</th>
                        <th>Détails</th>
                    </tr>
                </thead>

                <tbody>
""".format(cases = nombreCases, pierres = stockInitial)
      fichier.writelines(header)


      # On affiche une ligne par strategie
      for i in range(nbStrategies):
         strat = listeStrategies[i]

         line = """                    <tr>
                        <td>{rang}</td>
                        <td>{nom}</td>
                        <td>{points}</td>
                        <td class="hidden-sm hidden-xs">{victoires}</td>
                        <td class="hidden-sm hidden-xs">{defaites}</td>
                        <td class="hidden-sm hidden-xs">{matchsNuls}</td>
                        <td class="hidden-sm hidden-xs">{coupsInvalides}</td>
                        <td class="hidden-sm hidden-xs">{score}</td>
                        <td><button type="button" class="btn btn-default btn-xs" data-toggle="modal" data-target="#modal_{cases}_{pierres}_{rang}">Détails</button></td>
                    </tr>
""".format(rang = (i+1), nom = strat.nom, points = strat.points, victoires = strat.victoires, defaites = strat.defaites, matchsNuls = strat.matchsNuls, coupsInvalides = strat.coupsInvalides, score = strat.score, cases = nombreCases, pierres = stockInitial)         
         fichier.write(line)


      # On ecrit la fin du tableau
      footer = """                </tbody>
            </table>


"""
      fichier.writelines(footer)


      # On cree une popin pour chaque strategie

      for i in range(nbStrategies):
         strat = listeStrategies[i]

         # Haut de la popin
         modal1 = """            <!-- Modal {cases}/{pierres} {rang} -->
            <div id="modal_{cases}_{pierres}_{rang}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">

                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <h4 class="modal-title" id="myModalLabel">{nom}</h4>
                        </div>

                        <div class="modal-body">

                            <h4>Résultats pour {cases} cases et {pierres} pierres</h4>
                            <table class="table table-striped">
                                <tr><td>Rang</td><td>{rang}</td></tr>
                                <tr><td>Points</td><td>{points}</td></tr>
                                <tr><td>Victoires</td><td>{victoires}</td></tr>
                                <tr><td>Défaites</td><td>{defaites}</td></tr>
                                <tr><td>Matchs nuls</td><td>{matchsNuls}</td></tr>
                                <tr><td>Coups invalides</td><td>{coupsInvalides}</td></tr>
                                <tr><td>Score</td><td>{score}</td></tr>
                            </table>

                            <hr>

                            <h4>Détails des matchs</h4>

                            <div class="matchs">
""".format(rang = (i+1), nom = strat.nom, points = strat.points, victoires = strat.victoires, defaites = strat.defaites, matchsNuls = strat.matchsNuls, coupsInvalides = strat.coupsInvalides, score = strat.score, cases = nombreCases, pierres = stockInitial)         
         fichier.write(modal1)


         # Details des matchs
         nbMatches = len(strat.affrontements)
         for j in range(nbMatches):
            resultats = strat.affrontements[j][1]

            joueurGauche = strat.nom
            if(resultats.gagnant == 1):
               joueurGauche = "<strong>" + joueurGauche + "</strong>"

            joueurDroite = strat.affrontements[j][0]
            if(resultats.gagnant == 2):
               joueurDroite = "<strong>" + joueurDroite + "</strong>"

            joueurs = """
                                <p>{gauche} - {droite}</p>

""".format(gauche = joueurGauche, droite = joueurDroite)
            fichier.write(joueurs)

            pourcentageVictoires = (100 * resultats.victoiresGauche) // resultats.matchPrevus
            pourcentageDefaites = (100 * resultats.victoiresDroite) // resultats.matchPrevus

            if(resultats.matchsNuls == 0): # S'il n'y a aucun match nul, on ajuste eventuellement le pourcentage de victoires pour retrouver 100%
               pourcentageMatchsNuls = 0
               pourcentageVictoires = 100 - pourcentageDefaites

            else: # S'il a eu des matchs nuls; on ajuste eventuellement le pourcentage de matchs nuls pour retrouver 100%
               pourcentageMatchsNuls = 100 - (pourcentageVictoires + pourcentageDefaites)

            barres1 = """                                <div class="progress">
"""
            fichier.write(barres1)

            if(pourcentageVictoires > 0):
               victoires = """                                    <div class="progress-bar" style="width: {pourcentage}%;">
                                        {nombre}
                                    </div>
""".format(pourcentage = pourcentageVictoires, nombre = resultats.victoiresGauche)
               fichier.write(victoires)
            if(pourcentageMatchsNuls > 0):
               nuls = """                                    <div class="progress-bar progress-bar-success" style="width: {pourcentage}%;">
                                        {nombre}
                                    </div>
""".format(pourcentage = pourcentageMatchsNuls, nombre = resultats.matchsNuls)
               fichier.write(nuls)
            if(pourcentageDefaites > 0):
               defaites = """                                    <div class="progress-bar progress-bar-danger" style="width: {pourcentage}%;">
                                        {nombre}
                                    </div>
 """.format(pourcentage = pourcentageDefaites, nombre = resultats.victoiresDroite)
               fichier.write(defaites)

            barres2 = """                                </div>

"""
            fichier.write(barres2)


         # Bas de la popin
         modal3 = """                            </div>
                        </div>
                    </div>
                </div>
            </div>
         
"""
         fichier.write(modal3)

      fin = """            <!-- ----- Fin du classement pour {cases} cases et {pierres} pierres ----- -->
      
      
""".format(cases = nombreCases, pierres = stockInitial)
      fichier.write(fin)



   genererHTMLpartiel(7, 15)
   genererHTMLpartiel(7, 30)
   genererHTMLpartiel(15, 30)
   genererHTMLpartiel(15, 50)


   # Calcul du classement general
   calculerClassementGeneral(listeStrategies)
   listeStrategies.sort()
   listeStrategies.reverse()

   general1 = """


            <h2 id="classement_general">Classement général</h2>

            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Stratégie</th>
                        <th>Total des points</th>
                        <th>Total des scores</th>
                        <th class="hidden-sm hidden-xs">Points 7/15</th>
                        <th class="hidden-sm hidden-xs">Points 7/30</th>
                        <th class="hidden-sm hidden-xs">Points 15/30</th>
                        <th class="hidden-sm hidden-xs">Points 15/50</th>
                    </tr>
                </thead>
                <tbody>
"""
   fichier.write(general1)

   for i in range(nbStrategies):
      strat = listeStrategies[i]
      points_7_15 = strat.listePoints[0][0]
      points_7_30 = strat.listePoints[1][0]
      points_15_30 = strat.listePoints[2][0]
      points_15_50 = strat.listePoints[3][0]
      points_totaux = points_7_15 + points_7_30 + points_15_30 + points_15_50
      score_7_15 = strat.listePoints[0][1]
      score_7_30 = strat.listePoints[1][1]
      score_15_30 = strat.listePoints[2][1]
      score_15_50 = strat.listePoints[3][1]
      total_scores = score_7_15 + score_7_30 + score_15_30 + score_15_50

      general2 = """                    <tr>
                        <td>{rang}</td>
                        <td>{nom}</td>
                        <td>{total}</td>
                        <td>{totalScores}</td>
                        <td class="hidden-sm hidden-xs">{p1}</td>
                        <td class="hidden-sm hidden-xs">{p2}</td>
                        <td class="hidden-sm hidden-xs">{p3}</td>
                        <td class="hidden-sm hidden-xs">{p4}</td>
                    </tr>
""".format(rang = (i+1), nom = strat.nom, total = points_totaux, totalScores = total_scores, p1 = points_7_15, p2 = points_7_30, p3 = points_15_30, p4 = points_15_50)
      fichier.write(general2)


   general3 = """                </tbody>
            </table>


"""
   fichier.write(general3)


   # Pour finir, on ferme le fichier
   fichier.close()



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


