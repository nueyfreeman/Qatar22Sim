"""
Qatar 2022

A mathematically simple model of the 2022 Fifa World Cup in Qatar, with randomized results based on player
and team data scraped for educational purposes only. Results are written to csv files. Works with squads.py,
qatarsquadscraper.py, and player and team data in csv files (QatarSquadsv2mod.csv & team_stats_v1.csv).
"""

import time
import random as rand
import squads

GROUPS = 'ABCDEFGH'
TEAM_POOL = {}


# reads in scraped data from csv, creates team objects in nested dictionaries, and fills their rosters
def build_team_pool():
    for i in GROUPS:
        TEAM_POOL[i] = {}  # key for each group is a single letter A through H

    # reads in scraped and cleaned player data, while creating corresponding teams if necessary
    with open('QatarSquadsv2mod.csv') as file:
        i = 0
        for line in file:
            i += 1  # gives each player a unique id number for debugging
            data = line.split(',')  # converts line of csv file to a list where data in each index is known

            # see QatarSquads.csv to verify what player data corresponds to which index when initializing player objects

            index = TEAM_POOL[data[0][6]]  # selects proper group using key derived from string data -- ex. 'Group A'

            # expect exception if the team hasn't been made yet -- if error, then make team before adding player
            try:
                index[data[1]].add_to_roster(squads.Player(i, data[3], data[2], data[11], data[12], data[6]))
            except (TypeError, KeyError):
                index[data[1]] = squads.Team(data[0][6], data[1])  # to make the team object first
                index[data[1]].add_to_roster(squads.Player(i, data[3], data[2], data[11], data[12], data[6]))

            """ UNCOMMENT TO DEBUG DATA LOADING
            if i % 100 == 0:
                team = TEAM_POOL[data[0][6]][data[1]]
                print(team)
                print(team.get_roster()[rand.randint(0, len(team.get_roster())-1)])
                print()
            """

    # add team data (manually collected) to team objects
    with open('team_stats_v1.csv') as team_data:
        for line in team_data:
            data = line.split(',')

            try:
                TEAM_POOL[data[0]][data[1]].add_tie_chance(data[8])
                TEAM_POOL[data[0]][data[1]].add_defense(data[7])
            except KeyError:
                print('No data for this line')


# play through tourney from group stage to championship
def play_tourney():
    winners = {g: [1, 2] for g in GROUPS}  # reinitialize group winners dict
    for g in TEAM_POOL:
        group = TEAM_POOL[g]  # each group
        gt = []
        for t in group.values():
            gt.append(t)  # place teams objects in list
        group_matches(gt)  # play matches
        gt.sort(key=lambda a: a.get_points(), reverse=True)  # sort list descending by points
        for t in range(len(gt)):  # place winners & eliminate losers
            if t == 0:
                winners[g][0] = gt[t]  # first in list after sorting added to winner dict as top finisher
            elif t == 1:
                winners[g][1] = gt[t]  # second in list
            else:
                gt[t].eliminated('Group Stage')  # eliminate others

    m49 = match(winners['A'][0], winners['B'][1], '16')  # place winners of group stage into knockout round
    m50 = match(winners['C'][0], winners['D'][1], '16')  # see official Fifa World Cup bracket for match-up structure
    m51 = match(winners['E'][0], winners['F'][1], '16')  # ('A' = Group A, 'B' = Group B, etc)
    m52 = match(winners['G'][0], winners['H'][1], '16')  # ( 0 = Winner; 1 = Runner-Up)
    m53 = match(winners['B'][0], winners['A'][1], '16')  # ex. ['A'][1] = Group A Runner-Up, ['F'][0] = Group F Winner
    m54 = match(winners['D'][0], winners['C'][1], '16')
    m55 = match(winners['F'][0], winners['E'][1], '16')
    m56 = match(winners['H'][0], winners['G'][1], '16')

    m57 = match(m49, m50, 'Quarterfinals')  # winner of match 49 plays winner of match 50, etc
    m58 = match(m51, m52, 'Quarterfinals')
    m59 = match(m53, m54, 'Quarterfinals')
    m60 = match(m55, m56, 'Quarterfinals')

    m61 = match(m57, m58, 'Semifinals')  # not modeling third place game
    m62 = match(m59, m60, 'Semifinals')

    m64 = match(m61, m62, 'Final')
    m64.eliminated('Champion', 'Nobody')  # must eliminate winner to return them to the TEAMPOOL and record result

    print(f'The champion is {m64}')


# nested loops for group stage - each team meets one time
def group_matches(group_list):
    for i in range(len(group_list)):
        for j in range(len(group_list) - 1 - i):
            match(group_list[i], group_list[j + 1 + i], 'group')  # this algorithm creates one meeting between each team


# function to play one match, returns a winner and eliminates loser in non-group matches, otherwise returns None
def match(t1, t2, stage):
    tie1 = t1.get_tie_chance()
    tie2 = t2.get_tie_chance()
    tie = (tie1 + tie2) / 2  # finds average of tie probability

    team1 = t1.matchday()  # gets an int to represent strength of each team
    team2 = t2.matchday()

    draw = int((team1 + team2) * tie)  # gets an int to represent probability of draw in proportion to team strength
    prob = team1 + team2 + draw  # an int to represent the match

    """
    A mathematically simple model for simulating matches:
    
    The result is randomly generated based on the strength score calculated for each team (based on data) and the
    proportional probability of a tie. A random number is chosen in the range of zero to `prob`. If it is in the
    subrange corresponding to Team 1 - Team 1 wins, if in subrange corresponding to Team2 - Team 2 wins, and if in the
    subrange corresponding to a draw - a draw is the result. If a draw happens in the case of a knockout round game,
    the randomization is simply run again until a winner is drawn. 
    """

    def play():
        chance = rand.randint(0, prob)
        winner = None
        if chance <= team2:  # team 2 wins
            t2.add_win()
            if stage == 'group':  # for group match, only add points
                t2.add_points(3)
            else:  # for knockout match - eliminate loser & return winner
                t1.eliminated(stage, f'to {t2.get_country()}')
                winner = t2
        elif (team1 + team2) >= chance > team2:  # team 1 wins
            t1.add_win()
            if stage == 'group':
                t1.add_points(3)  # three points for winner
            else:
                t2.eliminated(stage, f'to {t1.get_country()}')  # record exit stats including stage and opponent
                winner = t1
        else:  # tie
            if stage == 'group':
                t1.add_points(1)  # one point for tie
                t2.add_points(1)
                t1.add_tie()
                t2.add_tie()
            else:
                winner = play()  # recursively play for non-tie-able game
        return winner

    return play()


# clear the stats of all teams
def clear_teams():
    for j in TEAM_POOL:
        for k in TEAM_POOL[j]:
            TEAM_POOL[j][k].clear()


# prints all teams, mostly for debugging (WILL HAVE TO EDIT __str__ in Team and Player classes of squads.py
def show_teams():
    for j in TEAM_POOL:
        print()
        print(j)
        for k in TEAM_POOL[j]:
            team = TEAM_POOL[j][k]
            print(team)
            #random_player = team.get_roster()[rand.randint(0, len(team.get_roster())-1)]
            #print(random_player)


# create csv containing player and team influences for sim, allows user to add comment in file
def static_team_analysis():
    # allows user to name save file in console while creating it
    with open(str(input('Enter filename for team analysis: ') + '.csv'), 'w') as file:
        file.write(str(input('Any notes for this sim? ') + '\n'))
        for j in TEAM_POOL:
            for k in TEAM_POOL[j]:
                team = TEAM_POOL[j][k]
                file.write(str(f'{team.get_group()},{team.get_country()}\n'))

                # EDIT __str__ function in Team class of squads.py to adjust what data is saved in the file
                file.write(str(team))

                # EDIT __str__ function in Player class to adjust what player data is saved (mostly to debug)
                team.show_full_roster(file)


# create csv containing the results of the given round of simulations
def results():
    # allows user to name the save file in the console as it is created
    with open(str(input('Enter filename for results: ') + '.csv'), 'w') as rslt:
        rslt.write(str(input('Any notes for this sim? ') + '\n'))
        for j in TEAM_POOL:
            for k in TEAM_POOL[j]:
                team = TEAM_POOL[j][k]
                rslt.write(str(team.calc_results()))  # see Team class in squads.py


def main():
    # track run times
    start_wall = time.time()
    start_cpu = time.process_time()

    build_team_pool()  # build objects from imported data

    for i in range(1000):  # run simulations
        play_tourney()
        clear_teams()

    static_team_analysis()  # record team strength during this iteration
    results()  # record results of simulations

    end_wall = time.time()
    end_cpu = time.process_time()

    print()
    print(f'Wall time: {end_wall - start_wall}')
    print(f'CPU time: {end_cpu - start_cpu}')


if __name__ == '__main__':
    main()
