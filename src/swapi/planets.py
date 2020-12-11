import parsers
import swapi

PLANETS_URL = swapi.BASE_URL + "planets/"

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
    rawPlanets = swapi.fetchFromSwapi(PLANETS_URL)
    planets = [Planet(rawPlanet) for rawPlanet in rawPlanets]
    return planets