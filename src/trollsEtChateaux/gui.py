#!/usr/bin/python
# -*-coding:utf-8 -*

import tkinter
from trollsEtChateaux.entities import *

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
        self.labelGauche = tkinter.Label(self, text="    Stock gauche : 20", justify="left", font=("Helvetica", 16))
        self.labelGauche.grid(row = 1, column = 0, sticky = "W", padx=10, pady=10)

        textLabelDroite = "Stock droite : {0}".format(stockInitial)
        self.labelDroite = tkinter.Label(self, text="Stock droite : 20    ", justify="right", font=("Helvetica", 16))
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
