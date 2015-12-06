#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    print 'Connecting to database'
    return psycopg2.connect("dbname=tournament")

shared_conn = connect()


def deleteMatches():
    """Remove all the match records from the database."""
    with shared_conn.cursor() as cursor:
        cursor.execute("delete from matches")
        shared_conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    with shared_conn.cursor() as cursor:
        cursor.execute("delete from players")
        shared_conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    with shared_conn.cursor() as cursor:
        cursor.execute("select count(*) from players")
        return cursor.fetchone()[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    cursor = shared_conn.cursor()
    insert_sql = "insert into players (name) values (%s)"
    cursor.execute(insert_sql, [name])
    shared_conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """select pw.id, pw.name, pw.wins, players_matches.matches
               from players_wins as pw left join players_matches
               ON (players_matches.id = pw.id)"""
    with shared_conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with shared_conn.cursor() as cursor:
        insert_sql = "insert into matches (winner, loser) values (%s, %s)"
        cursor.execute(insert_sql, [winner, loser])
        shared_conn.commit()


def swissPairings():
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
    with shared_conn.cursor() as cursor:
        cursor.execute("""select players_wins.id, players_wins.name
                        from players_wins
                        order by players_wins.wins""")
        pairings = []
        for player_id, player_name in cursor:
            opponent = cursor.fetchone()
            if opponent:
                pair = (player_id, player_name, opponent[0], opponent[1])
                pairings.append(pair)
            else:
                print("Warning: no pair for player %s(%s)" %
        return pairings




