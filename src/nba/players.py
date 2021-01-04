from utils import csvUtils
from utils import parsers
import nba.seasonStats

SOURCE_CSV_FILEPATH = "src/nba/players_stats.csv"
DIST_CSV_FILEPATH_1 = "dist/nba/players-stats.csv"
DIST_CSV_HEADERS_1 = ["name", "height", "weight"]
DIST_CSV_FILEPATH_2 = "dist/nba/players-origin.csv"
DIST_CSV_HEADERS_2 = ["name", "yearOfBirth", "birthCity", "birthState", "college"]

class Player:
    def __init__(self, rawPlayer):
        self.name = rawPlayer["Player"].replace("*", "")
        self.height = rawPlayer["height"]
        self.weight = rawPlayer["weight"]
        self.yearOfBirth = parsers.parseInteger(rawPlayer["born"])
        self.birthCity = rawPlayer["birth_city"]
        self.birthState = rawPlayer["birth_state"]
        self.college = rawPlayer["collage"]
        
    def __repr__(self):
        return "{0}\n - Height: {1}\n - Weight: {2}\n - Year of birth: {3}\n - Place of birth: {4}, {5}\n - College: {6}".format(
            self.name.upper(), self.height, self.weight, self.yearOfBirth, self.birthCity, self.birthState, self.college)

def isValidPlayer(line):
    return (line["born"] != None) and (line["height"] != None) and (line["weight"] != None)

def fetchAllPlayers():
    rawPlayers = csvUtils.readCsv(SOURCE_CSV_FILEPATH)
    players = [Player(rawPlayer) for rawPlayer in rawPlayers if isValidPlayer(rawPlayer)]
    return players

def fetchPlayersWithSeasonStats():
    allSeasonStats = nba.seasonStats.fetchAllSeasonStats()
    playerNames = [seasonStats.player for seasonStats in allSeasonStats]
    players = fetchAllPlayers()
    return [player for player in players if player.name in playerNames]

def getName(player):
    return player.name

def extractFieldsForCSV1(player):
    return { "name": player.name, "height": player.height, "weight": player.weight }

def createPlayerCSV1():
    players = fetchPlayersWithSeasonStats()
    players.sort(key=getName)
    playerRows = [extractFieldsForCSV1(player) for player in players]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_1, DIST_CSV_HEADERS_1, playerRows)

def getYearOfBirth(player):
    return player.yearOfBirth

def extractFieldsForCSV2(player):
    return { "name": player.name, "yearOfBirth": player.yearOfBirth, "birthCity": player.birthCity, "birthState": player.birthState, "college": player.college }

def createPlayerCSV2():
    players = fetchPlayersWithSeasonStats()
    players.sort(key=getYearOfBirth)
    playerRows = [extractFieldsForCSV2(player) for player in players]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_2, DIST_CSV_HEADERS_2, playerRows)
