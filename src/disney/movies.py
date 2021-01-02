from utils import csvUtils
from utils import parsers

SOURCE_CSV_FILEPATH = "src/disney/movies.csv"
DIST_CSV_FILEPATH_1 = "dist/disney/movies.csv"
DIST_CSV_HEADERS_1 = ["title", "releaseYear", "genre", "rating"]
DIST_CSV_FILEPATH_2 = "dist/disney/movies-gross.csv"
DIST_CSV_HEADERS_2 = ["title", "releaseYear", "totalGross", "inflationAdjustedGross"]

class Movie:
    def __init__(self, rawMovie):
        self.title = rawMovie["movie_title"]
        self.releaseYear = rawMovie["release_date"].split()[-1]
        self.genre = rawMovie["genre"]
        self.rating = rawMovie["MPAA_rating"]
        self.totalGross = parsers.parseDollarSum(rawMovie["total_gross"])
        self.inflationAdjustedGross = parsers.parseDollarSum(rawMovie["inflation_adjusted_gross"])
        
    def __repr__(self):
        return "{0}\n - Release year: {1}\n - Genre: {2}\n - Rating: {3}\n - Total gross: {4}\n - Inflation adjusted gross: {5}".format(
            self.title.upper(), self.releaseYear, self.genre, self.rating, self.totalGross, self.inflationAdjustedGross)

def fetchAllMovies():
    rawMovies = csvUtils.readCsv(SOURCE_CSV_FILEPATH)
    movies = [Movie(rawMovie) for rawMovie in rawMovies]
    return movies

def extractFieldsForCSV1(movie):
    return { "title": movie.title, "releaseYear": movie.releaseYear, "genre": movie.genre, "rating": movie.rating }

def createMovieCSV1():
    allMovies = fetchAllMovies()
    movieRows = [extractFieldsForCSV1(movie) for movie in allMovies]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_1, DIST_CSV_HEADERS_1, movieRows)

def extractFieldsForCSV2(movie):
    return { "title": movie.title, "releaseYear": movie.releaseYear, "totalGross": movie.totalGross, "inflationAdjustedGross": movie.inflationAdjustedGross }

def getTitle(movie):
    return movie.title

def createMovieCSV2():
    allMovies = fetchAllMovies()
    sortedMovies = sorted(allMovies, key=getTitle)
    movieRows = [extractFieldsForCSV2(movie) for movie in sortedMovies]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_2, DIST_CSV_HEADERS_2, movieRows)
