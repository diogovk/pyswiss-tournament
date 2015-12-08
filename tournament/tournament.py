#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    print 'Connecting to database'
    return psycopg2.connect("dbname=tournament")

shared_conn = connect()


def deleteAllTournaments():
    """Remove all the tournaments and associated date from the database. """
    with shared_conn.cursor() as cursor:
        cursor.execute("delete from matches")
        cursor.execute("delete from participants")
        cursor.execute("delete from tournaments")
        shared_conn.commit()

def deleteMatches(tournament_id="*"):
    """Remove all the match records from the database.

    Please note that when removing matches, the participants scores are also
    cleared.

    Args:
      tournament_id: the id of the tournament whose matches should be
                     deleted, or "*" to delete all matches from all tournaments
    """
    with shared_conn.cursor() as cursor:
        if tournament_id == "*":
            cursor.execute("delete from matches")
            cursor.execute("update participants set wins=0, ties=0, bye=false")
        else:
            cursor.execute("delete from matches where tournament = %s",
                    tournament)
            cursor.execute("update participants set wins=0, ties=0, bye=false"
                    "where tournament = %s", tournament)
        shared_conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    with shared_conn.cursor() as cursor:
        cursor.execute("delete from participants")
        cursor.execute("delete from players")
        shared_conn.commit()


def countTournaments():
    """Returns the number of tournaments in the database."""
    with shared_conn.cursor() as cursor:
        cursor.execute("select count(*) from tournaments")
        return cursor.fetchone()[0]


def countPlayers():
    """Returns the number of players currently registered."""
    with shared_conn.cursor() as cursor:
        cursor.execute("select count(*) from players")
        return cursor.fetchone()[0]


def countParticipants(tournament_id):
    """Returns the number of participants currently registered in a tournament

    Args:
      tournament_id: the id of the tournament
    """
    with shared_conn.cursor() as cursor:
        cursor.execute("select count(*) from players")
        return cursor.fetchone()[0]

def createNewPlayer(name):
    """Register a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    with shared_conn.cursor() as cursor:
        insert_sql = "insert into players (name) values (%s) returning id"
        cursor.execute(insert_sql, [name])
        shared_conn.commit()
        return cursor.fetchone()[0]

def createNewTournament(description=""):
    """Creates a new tournament in the database returning its id.

    The database assigns a unique serial id number for the tournament.

    Args:
      description: A description for the tournament.
    Returns:
      The new tournament id, which is an integer
    """
    with shared_conn.cursor() as cursor:
        insert_sql = """
            insert into tournaments (description) values (%s) returning id"""
        cursor.execute(insert_sql, [description])
        shared_conn.commit()
        return cursor.fetchone()[0]


def entryTournament(tournament_id, player_id):
    """Register a player in a tournament.

    Args:
      tournament_id: The ID of an existing tournament.
      player_id: The ID of the player registering for the tournament.
    """
    insert_sql = """
        insert into participants (tournament_id, player_id) values (%s, %s)"""
    with shared_conn.cursor() as cursor:
        cursor.execute(insert_sql, (tournament_id, player_id))
        shared_conn.commit()


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """
            select participants_matches.player_id, players.name,
            participants_matches.wins, participants_matches.ties,
            participants_matches.matches, participants_matches.points
            from participants_matches, players
            where players.id = participants_matches.player_id"""
    with shared_conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def reportTie(tournament_id, player1, player2):
    """Records the outcome of a single match between two players.

    Both participants will get 1 tie (1 point), and match counts will
    be updated.

    See also: reportVictory()
    Args:
      tournament_id: the id of the tournament
      player1:  the id number of the first player
      player2:  the id number of the second player
    """
    with shared_conn.cursor() as cursor:
        _insertMatch(cursor, tournament_id, player1, player2)
        update_sql = """
            update participants set ties = ties+1
            where tournament_id = %s and
            (player_id = %s or player_id = %s ) """
        cursor.execute(update_sql, (tournament_id, player1, player2))
        shared_conn.commit()


def reportVictory(tournament_id, winner, loser):
    """Records the winner and loser of a single match.

    The winner participant will get 1 win (3 points), and match counts will
    be updated for both players.

    See also: reportTie()
    Args:
      tournament_id: the id of the tournament
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with shared_conn.cursor() as cursor:
        _insertMatch(cursor, tournament_id, winner, loser)
        update_sql = """update participants set wins = wins+1
                where tournament_id = %s and player_id = %s """
        cursor.execute(update_sql, (tournament_id, winner))
        shared_conn.commit()


def _insertMatch(cursor, tournament_id, player1, player2):
    """ Inserts a match into the database.

    The column in which each player is stored should be constant, as to avoid
    that two matches with the same players in the same tournament are stored.
    This means that insertMatch(c,t, 1, 2) followed by insertMatch(c, t, 2, 1)
    will generate a primary key violation.
    The user should not use this function directly, istead using reportVictory()
    and reportTie()
    """
    insert_sql = """insert into matches (tournament_id, participant1,
            participant2) values (%s, %s, %s)"""
    if player1 > player2:
        cursor.execute(insert_sql, (tournament_id, player2, player1))
    else:
        cursor.execute(insert_sql, (tournament_id, player1, player2))




def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = """
        select participants.player_id, players.name from participants, players
        where participants.player_id = players.id and tournament_id = %s
        order by participants.wins
        """
    with shared_conn.cursor() as cursor:
        cursor.execute(query, [tournament_id])
        pairings = []
        for player_id, player_name in cursor:
            opponent = cursor.fetchone()
            if opponent:
                pair = (player_id, player_name, opponent[0], opponent[1])
                pairings.append(pair)
            else:
                print("Warn: no pair for player %s(%s)" %
                      (player_id, player_name))
        return pairings

