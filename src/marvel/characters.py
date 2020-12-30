from utils import csvUtils
from utils import parsers

SOURCE_CSV_FILEPATH = "src/marvel/characters.csv"
DIST_CSV_FILEPATH = "dist/marvel/characters.csv"
DIST_CSV_HEADERS = ["name", "identity", "alignment", "appearanceCount", "yearOfAppearance"]


class Character:
    def __init__(self, rawCharacter):
        self.name = rawCharacter["name"]
        self.identity = rawCharacter["ID"]
        self.alignment = rawCharacter["ALIGN"]
        self.appearanceCount = parsers.parseInteger(rawCharacter["APPEARANCES"])
        self.yearOfAppearance = parsers.parseInteger(rawCharacter["Year"])
        
    def __repr__(self):
        return "{0} \n - Identity: {1}\n - Alignment: {2}\n - Appearance count: {3}\n - Year of appearance: {4}".format(
            self.name.upper(), self.identity, self.alignment, self.appearanceCount, self.yearOfAppearance)

def fetchAllCharacters():
    rawCharacters = csvUtils.readCsv(SOURCE_CSV_FILEPATH, delimiter=",")
    characters = [Character(rawCharacter) for rawCharacter in rawCharacters]
    return characters

def isValidCharacter(character):
    return (character.yearOfAppearance != None) and (character.yearOfAppearance > 1955)

def createCharacterCSV():
    allCharacters = fetchAllCharacters()
    characterRows = [character.__dict__ for character in allCharacters if isValidCharacter(character)]

    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, characterRows)
