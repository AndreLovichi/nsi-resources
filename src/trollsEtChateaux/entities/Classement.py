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
