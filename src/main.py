import disney.movies
import disney.voiceActors
import harryPotter.characters
import harryPotter.spells
import marvel.characters
import nba.players
import nba.seasonStats
import swapi.movies
import swapi.planets

import trollsEtChateaux.exportToJSON
import trollsEtChateaux.gui as trollGUI
import trollsEtChateaux

# disney.movies.createMovieCSV1()
# disney.movies.createMovieCSV2()
# disney.voiceActors.createVoiceActorCSV()

#harryPotter.characters.createCharacterCSV()
#harryPotter.spells.createSpellCSV()

# nba.players.createPlayerCSV1()
# nba.players.createPlayerCSV2()
# nba.seasonStats.createSeasonStatsCSV1()
# nba.seasonStats.createSeasonStatsCSV2()

#marvel.characters.createCharacterCSV()

#swapi.movies.createMovieCSV()
#swapi.planets.createPlanetCSV()



partie0 = trollsEtChateaux.Partie(7, 15)
print(partie0)

partie0.tourDeJeu(2,4)
print(partie0) # Affiche

trollsEtChateaux.jouerPartie(7, 15, trollsEtChateaux.strategieExemple1, trollsEtChateaux.strategieExemple2) # Affiche

trollsEtChateaux.jouerPlusieursParties(7, 15, trollsEtChateaux.strategieExemple1, trollsEtChateaux.strategieExemple2)



strategie1 = trollsEtChateaux.Strategie("Exemple 1", trollsEtChateaux.strategieExemple1)
strategie2 = trollsEtChateaux.Strategie("Exemple 2", trollsEtChateaux.strategieExemple2)


strategiesTests = [strategie1, strategie2]
trollsEtChateaux.exportToJSON.genererJSON(strategiesTests)

trollGUI.GUI(7, 15, strategie1, strategie2)