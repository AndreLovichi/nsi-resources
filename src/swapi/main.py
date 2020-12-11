import csvUtils
import movies
import planets


# PLANETS
planetFilename = "planets.csv"
planetHeaders = ["name", "climate", "terrain", "population", "diameter"]

def isValidPlanet(planet):
    return (planet.population != None) and (planet.diameter != None) and (planet.diameter != 0) and (planet.climate != "unknown") and (planet.terrain != "unknown")

allPlanets = planets.fetchAllPlanets()
planetRows = [planet.__dict__ for planet in allPlanets if isValidPlanet(planet)]

csvUtils.saveAsCsv(planetFilename, planetHeaders, planetRows)


# MOVIES
movieFilename = "movies.csv"
movieHeaders = ["title", "episodeNumber", "year", "director"]

allMovies = movies.fetchAllMovies()
movieRows = [movie.__dict__ for movie in allMovies]

csvUtils.saveAsCsv(movieFilename, movieHeaders, movieRows)
