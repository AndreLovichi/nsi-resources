from utils import csvUtils
from utils import parsers
import nba.teamAbbreviations


SOURCE_CSV_FILEPATH = "src/nba/seasons_stats.csv"
DIST_CSV_FILEPATH_1 = "dist/nba/seasons-stats-2000-2009.csv"
DIST_CSV_FILEPATH_2 = "dist/nba/seasons-stats-2010-2017.csv"
DIST_CSV_HEADERS = ["year", "player", "team", "games", "points", "assists", "blocks", "rebounds" ]

class SeasonStats:
    def __init__(self, rawLine):
        self.year = parsers.parseInteger(rawLine["Year"])
        self.player = rawLine["Player"].replace("*", "")
        self.team = nba.teamAbbreviations.ABBREVIATIONS[rawLine["Tm"]]
        self.games = parsers.parseInteger(rawLine["G"])
        self.points = parsers.parseInteger(rawLine["PTS"])
        self.assists = parsers.parseInteger(rawLine["AST"])
        self.blocks = parsers.parseInteger(rawLine["BLK"])
        self.rebounds = parsers.parseInteger(rawLine["TRB"])
        
    def __repr__(self):
        return "{0} - {1} ({2})\n - Games: {3}\n - Points: {4}\n - Assists: {5}\n - Blocks: {6}\n - Rebounds: {7}".format(
            self.year, self.player, self.team, self.games, self.points, self.assists, self.blocks, self.rebounds)

def fetchAllSeasonStats():
    rawLines = csvUtils.readCsv(SOURCE_CSV_FILEPATH)
    recentLines = [rawLine for rawLine in rawLines if (rawLine["Year"] != "") and (int(rawLine["Year"]) >= 2000) and (rawLine["Tm"] != "TOT")]
    seasonStats = [SeasonStats(rawLine) for rawLine in recentLines ]
    return seasonStats

def createSeasonStatsCSV1():
    allSeasonStats = fetchAllSeasonStats()
    seasonStatsRows = [seasonStats.__dict__ for seasonStats in allSeasonStats if seasonStats.year < 2010]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_1, DIST_CSV_HEADERS, seasonStatsRows)

def createSeasonStatsCSV2():
    allSeasonStats = fetchAllSeasonStats()
    seasonStatsRows = [seasonStats.__dict__ for seasonStats in allSeasonStats if seasonStats.year >= 2010]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH_2, DIST_CSV_HEADERS, seasonStatsRows)

