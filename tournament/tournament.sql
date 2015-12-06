-- Table definitions for the tournament project.
--

-- Make sure database is empty
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE tournaments ( id SERIAL primary key, description VARCHAR );
CREATE TABLE players ( id SERIAL primary key, name VARCHAR NOT NULL);

CREATE TABLE participants ( id SERIAL PRIMARY KEY,
                           player_id INTEGER REFERENCES players(id) NOT NULL,
                           wins INTEGER NOT NULL,
                           ties INTEGER NOT NULL,
                           bye  BOOLEAN NOT NULL DEFAULT FALSE);

CREATE TABLE matches ( id SERIAL PRIMARY KEY NOT NULL,
                       tournament_id INTEGER REFERENCES tournaments(id) NOT NULL,
                       participant1 INTEGER REFERENCES participants(id) NOT NULL,
                       participant2 INTEGER REFERENCES participants(id) NOT NULL);

-- -- creates a view with the row `wins` containing how many matches a certain
-- -- player on
-- CREATE VIEW players_wins AS SELECT players.*, COUNT(matches.winner) as wins
--                             FROM players LEFT JOIN matches
--                             ON (matches.winner = players.id)
--                             GROUP BY players.id;
--
-- -- creates a view with the row `matches` containing how many matches were
-- -- played by a certain player
-- CREATE VIEW players_matches AS SELECT players.*, COUNT(matches.id) AS matches
--                                FROM players LEFT JOIN matches
--                                ON (matches.winner = players.id
--                                    OR matches.loser = players.id)
--                                GROUP BY players.id;
--
