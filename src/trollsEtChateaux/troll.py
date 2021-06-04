#!/usr/bin/python
# -*-coding:utf-8 -*

import random
import traceback

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