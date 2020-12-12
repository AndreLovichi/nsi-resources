from utils import csvUtils
from utils import parsers
from swapi import api

PLANETS_URL = api.BASE_URL + "planets/"
DIST_CSV_FILEPATH = "dist/starwars/planets.csv"
DIST_CSV_HEADERS = ["name", "climate", "terrain", "population", "diameter"]

class Planet:
    def __init__(self, rawPlanet):
        self.climate = rawPlanet["climate"]
        self.diameter = parsers.parseInteger(rawPlanet["diameter"])
        self.name = rawPlanet["name"]
        self.population = parsers.parseInteger(rawPlanet["population"])
        self.terrain = rawPlanet["terrain"]
    
    def __repr__(self):
        return "{0}\n - Climat : {1}\n - Diamètre : {2}\n - Population : {3}\n - Terrain : {4}".format(self.name.upper(), self.climate, self.diameter, self.population, self.terrain)


def fetchAllPlanets():
    rawPlanets = api.fetchAllResults(PLANETS_URL)
    planets = [Planet(rawPlanet) for rawPlanet in rawPlanets]
    return planets

def isValidPlanet(planet):
    return (planet.population != None) and (planet.diameter != None) and (planet.diameter != 0) and (planet.climate != "unknown") and (planet.terrain != "unknown")

def createPlanetCSV():
    allPlanets = fetchAllPlanets()
    planetRows = [planet.__dict__ for planet in allPlanets if isValidPlanet(planet)]

    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, planetRows)