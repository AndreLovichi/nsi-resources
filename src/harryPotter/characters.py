from utils import csvUtils

SOURCE_CSV_FILEPATH = "src/harryPotter/characters.csv"
DIST_CSV_FILEPATH = "dist/harryPotter/characters.csv"
DIST_CSV_HEADERS = ["name", "house", "wand", "patronus", "gender", "species", "bloodStatus", "hairColor", "eyeColor"]


class Character:
    def __init__(self, rawCharacter):
        self.name = rawCharacter["Name"]
        self.gender = rawCharacter["Gender"]
        self.house = rawCharacter["House"]
        self.wand = rawCharacter["Wand"]
        self.patronus = rawCharacter["Patronus"]
        self.species = rawCharacter["Species"]
        self.bloodStatus = rawCharacter["Blood status"]
        self.hairColor = rawCharacter["Hair colour"]        
        self.eyeColor = rawCharacter["Hair colour"]
        
    def __repr__(self):
        return "{0}\n - Gender: {1}\n - House: {2}\n - Wand: {3}\n - Patronus: {4}\n - Species: {5}\n - Blood status: {6}\n - Hair color: {7}\n - Eye color: {8}".format(
            self.name.upper(), self.gender, self.house, self.wand, self.patronus, self.species, self.bloodStatus, self.hairColor, self.eyeColor)


def fetchAllCharacters():
    rawCharacters = csvUtils.readCsv(SOURCE_CSV_FILEPATH, delimiter=";")
    characters = [Character(rawCharacter) for rawCharacter in rawCharacters]
    return characters

def createCharacterCSV():
    allCharacters = fetchAllCharacters()
    characterRows = [character.__dict__ for character in allCharacters]

    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, characterRows)
