
# Swiss tournament management written in python

### About Swiss-system tournament

A Swiss-system tournament is a tournament which uses a non-elimination format.
Competitors meet one-to-one in each round and are paired using a predetermined set of rules designed to ensure that as far as possible a competitor plays competitors with the same current score, subject to not playing the
same opponent more than once. The winner is the competitor with the highest aggregate points earned in all rounds.

## Setting up

### Vagrant

Vagrant use is optional, but it will make dependencies set up easier, as well as providing
the same environment as where the tests were run.
To create and boot the virtual machine:

```
vagrant up
```

To access the machine:
```
vagrant ssh
```

To get to the "working directory":

```
cd /vagrant/tournament
```

### Database set-up
The following command will create the database structure, after DELETING ALL DATA IN THE DATABASE **tournament**.

```
psql -af tournament.sql
```

## Running the tests
To run the test suite:

```
python2 tournament_test.py
```

### Used resources

https://storage.googleapis.com/supplemental_media/udacityu/3532028970/P2TournamentResults-GettingStarted.pdf

http://www.postgresql.org/docs

http://initd.org/psycopg/docs

P2TournamentResults-GettingStarted.pdf provided by Udacity

https://en.wikipedia.org/wiki/Swiss-system_tournament
