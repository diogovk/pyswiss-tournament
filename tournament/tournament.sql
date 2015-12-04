-- Table definitions for the tournament project.
--

-- Make sure database is empty
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players ( id SERIAL primary key, NAME VARCHAR NOT NULL);

CREATE TABLE matches ( id SERIAL primary key,
                       winner INTEGER REFERENCES players(id) NOT NULL,
                       loser INTEGER REFERENCES players(id) NOT NULL);

-- creates a view with the row `wins` containing how many matches a certain 
-- player on
CREATE VIEW players_wins AS SELECT players.*, COUNT(matches.winner) as wins 
                            FROM players LEFT JOIN matches 
                            ON (matches.winner = players.id) 
                            GROUP BY players.id; 

-- creates a view with the row `matches` containing how many matches were
-- played by a certain player
CREATE VIEW players_matches AS SELECT players.*, COUNT(matches.id) AS matches 
                               FROM players LEFT JOIN matches 
                               ON (matches.winner = players.id 
                                   OR matches.loser = players.id) 
                               GROUP BY players.id;

