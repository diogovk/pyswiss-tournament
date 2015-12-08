-- Table definitions for the tournament project.
--

-- Make sure database is empty
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE tournaments (
        id SERIAL primary key NOT NULL,
        description VARCHAR
);

CREATE TABLE players ( id SERIAL primary key, name VARCHAR NOT NULL);

CREATE TABLE participants (
        tournament_id INTEGER REFERENCES tournaments(id) NOT NULL,
        player_id INTEGER REFERENCES players(id) NOT NULL,
        wins INTEGER DEFAULT 0 NOT NULL,
        ties INTEGER DEFAULT 0 NOT NULL,
        bye BOOLEAN NOT NULL DEFAULT FALSE,
        PRIMARY KEY (tournament_id, player_id)
);

CREATE TABLE matches (
        tournament_id INTEGER NOT NULL,
        participant1 INTEGER NOT NULL,
        participant2 INTEGER NOT NULL,
        FOREIGN KEY (tournament_id, participant1)
            REFERENCES participants(tournament_id, player_id),
        FOREIGN KEY (tournament_id, participant2)
            REFERENCES participants(tournament_id, player_id),
        PRIMARY KEY (tournament_id, participant1, participant2)

);

CREATE VIEW player_standings AS
        SELECT participants.*,
        count(matches.tournament_id) AS matches,
        -- each win 3 points, bye 3 points, tie 1 point
        participants.wins*3 + participants.ties +
            (case when participants.bye then 3 else 0 end) as points
        FROM participants LEFT JOIN matches
        ON (
                (
                    participant1 = participants.player_id
                    OR participant2 = participants.player_id
                  )
                AND matches.tournament_id = participants.tournament_id)
       GROUP BY participants.tournament_id, participants.player_id
       ORDER BY points DESC;
