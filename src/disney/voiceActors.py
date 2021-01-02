from utils import csvUtils
from utils import parsers

SOURCE_CSV_FILEPATH = "src/disney/voice-actors.csv"
DIST_CSV_FILEPATH = "dist/disney/voice-actors.csv"
DIST_CSV_HEADERS = ["voiceActor", "movie", "character"]

class VoiceActor:
    def __init__(self, rawLine):
        self.voiceActor = rawLine["voice-actor"].split(";")[0]
        self.movie = rawLine["movie"]
        self.character = rawLine["character"]
        
    def __repr__(self):
        return "{0}\n - Movie: {1}\n - Character: {2}".format(
            self.voiceActor, self.movie, self.character)

def fetchAllVoiceActors():
    rawLines = csvUtils.readCsv(SOURCE_CSV_FILEPATH)
    voiceActors = [VoiceActor(rawLine) for rawLine in rawLines]
    return voiceActors

def createVoiceActorCSV():
    allVoiceActors = fetchAllVoiceActors()
    voiceActorRows = [voiceActor.__dict__ for voiceActor in allVoiceActors if voiceActor.voiceActor != "None"]
    csvUtils.saveAsCsv(DIST_CSV_FILEPATH, DIST_CSV_HEADERS, voiceActorRows)