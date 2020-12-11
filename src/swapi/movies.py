import parsers
import swapi

MOVIES_URL = swapi.BASE_URL + "films/"

class Movie:
    def __init__(self, rawMovie):
        self.title = rawMovie["title"]
        self.episodeNumber = rawMovie["episode_id"]
        self.director = rawMovie["director"]
        self.year = parsers.parseInteger(rawMovie["release_date"][0:4])
    
    def __repr__(self):
        return "{0}\n - Numéro d'épisode : {1}\n - Année de parution : {2}\n - Réalisateur : {3}".format(self.title.upper(), self.episodeNumber, self.year, self.director)


def fetchAllMovies():
    rawMovies = swapi.fetchFromSwapi(MOVIES_URL)
    movies = [Movie(rawMovie) for rawMovie in rawMovies]
    return movies