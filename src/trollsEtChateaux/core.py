#!/usr/bin/python
# -*-coding:utf-8 -*

from trollsEtChateaux.entities import *
import traceback

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


