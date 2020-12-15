from utils import csvUtils

SOURCE_CSV_FILEPATH = "src/harryPotter/spells.csv"
DIST_CSV_FILEPATH = "dist/harryPotter/spells.csv"
DIST_CSV_HEADERS = ["name", "effect", "type", "incantation", "light", "incantationLength"]


class Spell:
    def __init__(self, rawSpell):
        self.name = rawSpell["Name"]
        self.incantation = rawSpell["Incantation"]
        self.type = rawSpell["Type"]
        self.effect = rawSpell["Effect"]
        self.light = rawSpell["Light"]
        self.incantationLength = len(rawSpell["Incantation"])
        
    def __repr__(self):
        return "{0}\n - Effect: {1}\n - Type: {2}\n - Incantation: {3} ({5})\n - Light: {4}".format(
            self.name.upper(), self.effect, self.type, self.incantation, self.light, self.incantationLength)


def fetchAllSpells():
    rawSpells = csvUtils.readCsv(SOURCE_CSV_FILEPATH, delimiter=";")
    spells = [Spell(rawSpell) for rawSpell in rawSpells]
    return spells

def createSpellCSV():
    allSpells = fetchAllSpells()
    spellRows = [spell.__dict__ for spell in allSpells]

    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, spellRows)
