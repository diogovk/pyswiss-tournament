#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def setupTournament():
    """ Returns a new tournament with 4 players enrolled in it """
    id1 = createNewPlayer("Bruno Walton")
    id2  = createNewPlayer("Boots O'Neal")
    id3 = createNewPlayer("Cathy Burton")
    id4 = createNewPlayer("Diane Grant")
    tournament_id = createNewTournament()
    entryTournament(tournament_id, id1)
    entryTournament(tournament_id, id2)
    entryTournament(tournament_id, id3)
    entryTournament(tournament_id, id4)
    return (tournament_id, [id1, id2, id3, id4])

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    createNewPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    createNewPlayer("Markov Chaney")
    createNewPlayer("Joe Malik")
    createNewPlayer("Mao Tsu-hsi")
    createNewPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."

def testCreateTournament():
    deleteAllTournaments()
    c = countTournaments()
    tournament_id = createNewTournament()
    tournament_id = createNewTournament()
    tournament_id = createNewTournament()
    if type(tournament_id) != int:
        raise ValueError("Tourament id should be an integer")
    c = countTournaments()
    if c != 3:
        raise ValueError("After creating 3 tournaments, countTournaments should be 3")
    deleteAllTournaments()
    c = countTournaments()
    if c != 0:
        raise ValueError("After deleting, countTournaments should return zero.")
    print "6. Tournaments can be created and deleted"


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    player1_id = createNewPlayer("Melpomene Murray")
    player2_id = createNewPlayer("Randy Schwartz")
    tournament_id = createNewTournament()
    entryTournament(tournament_id, player1_id)
    entryTournament(tournament_id, player2_id)
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only players registered in the tournament should "
                         "appear in standings.")
    for standing in standings.values():
        if (standing.matches != 0 or standing.wins != 0
                or standing.ties != 0 or standing.points != 0):
            raise ValueError("Newly registered players should have no matches, "
                             "ties, wins or points.")
    set_player_names = set([s.name for s in standings.values()])
    if set_player_names != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportVictory():
    deleteAllTournaments()
    tournament_id, [id1, id2, id3, id4] = setupTournament()
    reportVictory(tournament_id, id1, id2)
    reportVictory(tournament_id, id3, id4)
    standings = playerStandings(tournament_id)
    for standing in standings.values():
        if standing.matches != 1:
            raise ValueError("Each player should have one match recorded.")
    if standings[id1].wins != 1 and standings[id3].wins != 1:
        raise ValueError("Each match winner should have one win recorded.")
    if standings[id2].wins != 0 and standings[id4].wins != 0:
        raise ValueError("Each match loser should have zero wins recorded.")
    print "8. After a match, players have updated standings."


def testPairings():
    deleteAllTournaments()
    tournament_id, [id1, id2, id3, id4] = setupTournament()
    reportVictory(tournament_id, id1, id2)
    reportVictory(tournament_id, id3, id4)
    pairings = swissPairings(tournament_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."

def testPoints():
    deleteAllTournaments()
    tournament_id, [id1, id2, id3, id4] = setupTournament()
    reportVictory(tournament_id, id2, id1)
    reportTie(tournament_id, id3, id4)
    standings = playerStandings(tournament_id)
    if standings[id2].points != 3:
        raise ValueError(
                "A player should have 3 points after winning one round.")
    if standings[id1].points != 0:
        raise ValueError(
                "A player should have 0 points after losing one round.")
    for p_id in (id3, id4):
        if standings[p_id].ties != 1 or standings[p_id].points != 1:
            raise ValueError("Players should have one tie and one point after "
                             "a reported tie.")
    first = next(iter(standings.values()))
    if first.points != 3:
        raise ValueError("After the first round, where a player has won a "
                         "match, the player on top should have 3 points.")
    print "10. Points are given correctly depending on player win, loss or tie."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testCreateTournament()
    testStandingsBeforeMatches()
    testReportVictory()
    testPairings()
    testPoints()
    print "Success!  All tests pass!"


