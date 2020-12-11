from utils import csvUtils
from utils import parsers
from swapi import api

MOVIES_URL = api.BASE_URL + "films/"
MOVIES_CSV_FILENAME = "dist/starwars/movies.csv"
MOVIES_CSV_HEADERS = ["title", "episodeNumber", "year", "director"]

MISSING_MOVIES = [
    { "title": "The Force Awakens", "episode_id": "7", "director": "J. J. Abrams", "release_date": "2015-12-18" },
    { "title": "The Last Jedi", "episode_id": "8", "director": "Rian Johnson", "release_date": "2017-12-15" },
    { "title": "The Rise of Skywalker", "episode_id": "9", "director": "J. J. Abrams", "release_date": "2019-12-20" },
]


class Movie:
    def __init__(self, rawMovie):
        self.title = rawMovie["title"]
        self.episodeNumber = rawMovie["episode_id"]
        self.director = rawMovie["director"]
        self.year = parsers.parseInteger(rawMovie["release_date"][0:4])
    
    def __repr__(self):
        return "{0}\n - Numéro d'épisode : {1}\n - Année de parution : {2}\n - Réalisateur : {3}".format(self.title.upper(), self.episodeNumber, self.year, self.director)


def fetchAllMovies():
    rawMovies = api.fetchAllResults(MOVIES_URL)
    rawMovies.extend(MISSING_MOVIES)
    movies = [Movie(rawMovie) for rawMovie in rawMovies]
    return movies


def createMovieCSV():
    allMovies = fetchAllMovies()
    movieRows = [movie.__dict__ for movie in allMovies]

    csvUtils.saveAsCsv(MOVIES_CSV_FILENAME, MOVIES_CSV_HEADERS, movieRows)