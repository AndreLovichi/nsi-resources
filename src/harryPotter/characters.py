from utils import csvUtils

SOURCE_CSV_FILEPATH = "src/harryPotter/characters.csv"
DIST_CSV_FILEPATH = "dist/harryPotter/characters.csv"
DIST_CSV_HEADERS = ["firstName", "lastName", "house", "gender", "bloodStatus", "hairColor", "eyeColor"]


class Character:
    def __init__(self, rawCharacter):
        nameParts = rawCharacter["Name"].split()
        self.firstName = " ".join(nameParts[:-1])
        self.lastName = nameParts[-1]
        self.gender = rawCharacter["Gender"]
        self.house = rawCharacter["House"]
        self.bloodStatus = rawCharacter["Blood status"]
        self.hairColor = rawCharacter["Hair colour"]        
        self.eyeColor = rawCharacter["Eye colour"]
        
    def __repr__(self):
        return "{0} {1}\n - Gender: {2}\n - House: {3}\n - Blood status: {4}\n - Hair color: {5}\n - Eye color: {6}".format(
            self.firstName.upper(), self.lastName.upper(), self.gender, self.house, self.bloodStatus, self.hairColor, self.eyeColor)


def fetchAllCharacters():
    rawCharacters = csvUtils.readCsv(SOURCE_CSV_FILEPATH, delimiter=";")
    characters = [Character(rawCharacter) for rawCharacter in rawCharacters]
    return characters

def createCharacterCSV():
    allCharacters = fetchAllCharacters()
    characterRows = [character.__dict__ for character in allCharacters if character.firstName != ""]

    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, characterRows)
