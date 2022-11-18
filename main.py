"""
Qatar 2022
World Cup model
"""

import time
import random as rand
import squads

GROUPS = 'ABCDEFGH'
TEAM_POOL = {}


# reads in scraped data from csv, creates team objects in nested dictionaries, and fills their rosters
def build_team_pool():
    for i in GROUPS:
        TEAM_POOL[i] = {}
    with open('QatarSquadsv2mod.csv') as file:
        i = 0
        for line in file:
            i += 1
            data = line.split(',')

            if not data[0] == 'Group':
                # expect exception if the team hasn't been made yet -- if error, then make team before adding player
                try:
                    TEAM_POOL[data[0][6]][data[1]].add_to_roster(squads.Player(i, data[3], data[2], data[11], data[12]))
                except (TypeError, KeyError):
                    TEAM_POOL[data[0][6]][data[1]] = squads.Team(data[0][6], data[1]) #, rand.randint(0, 100))
                    TEAM_POOL[data[0][6]][data[1]].add_to_roster(squads.Player(i, data[3], data[2], data[11], data[12]))

            """ UNCOMMENT TO DEBUG
            if i % 100 == 0:
                team = TEAM_POOL[data[0][6]][data[1]]
                print(team)
                print(team.get_roster()[rand.randint(0, len(team.get_roster())-1)])
                print()
            """


# play through tourney from group stage to championship
def play_tourney():
    winners = {g: [1, 2] for g in GROUPS}  # reinitialize group winners dict
    for g in TEAM_POOL:
        group = TEAM_POOL[g]  # each group
        gt = []
        for t in group.values():
            gt.append(t)  # place teams in list
        group_matches(gt)  # play matches
        gt.sort(key=lambda a: a.get_points(), reverse=True)  # sort list descending by points
        for t in range(len(gt)):  # place winners & eliminate losers
            if t == 0:
                winners[g][0] = gt[t]
            elif t == 1:
                winners[g][1] = gt[t]
            else:
                gt[t].eliminated('Group Stage')

    m49 = match(winners['A'][0], winners['B'][1], '16')  # place winners of group stage into knockout round
    m50 = match(winners['C'][0], winners['D'][1], '16')  # see official Fifa World Cup bracket for match-up structure
    m51 = match(winners['E'][0], winners['F'][1], '16')  # ('A' = Group A, 'B' = Group B, etc)
    m52 = match(winners['G'][0], winners['H'][1], '16')  # ( 0 = Winner; 1 = Runner-Up)
    m53 = match(winners['B'][0], winners['A'][1], '16')  # ex. ['A'][1] = Group A Runner-Up, ['F'][0] = Group F Winner
    m54 = match(winners['D'][0], winners['C'][1], '16')
    m55 = match(winners['F'][0], winners['E'][1], '16')
    m56 = match(winners['H'][0], winners['G'][1], '16')

    m57 = match(m49, m50, 'Quarterfinals')
    m58 = match(m51, m52, 'Quarterfinals')
    m59 = match(m53, m54, 'Quarterfinals')
    m60 = match(m55, m56, 'Quarterfinals')

    m61 = match(m57, m58, 'Semifinals')  # put the losers somewhere
    m62 = match(m59, m60, 'Semifinals')

    m64 = match(m61, m62, 'Final')

    print()
    print(f'The champion is {m64}')
    print()


# nested loops for group stage - each team meets one time
def group_matches(group_list):
    for i in range(len(group_list)):
        for j in range(len(group_list)-1-i):
            match(group_list[i], group_list[j + 1 + i], 'group')


# function to play one match, returns a winner and eliminates loser in non-group matches, otherwise returns None
def match(t1, t2, stage):
    team1 = t1.matchday()
    team2 = t2.matchday()
    prob = team1 + team2

    def play():
        chance = rand.randint(0, prob)
        winner = None
        if chance > team1:  # team 2 wins
            t2.add_win()
            if stage == 'group':  # for group match, only add points
                t2.add_points(3)
            else:  # for knockout match - eliminate loser & return winner
                t1.eliminated(stage, f'to {t2.get_country()}')
                winner = t2
        elif chance < team1:  # team 1 wins
            t1.add_win()
            if stage == 'group':
                t1.add_points(3)  # three points for winner
            else:
                t2.eliminated(stage, f'to {t1.get_country()}')  # record exit stats including stage and opponent
                winner = t1
        elif chance == team1:  # tie
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


# prints all team stats, mostly for debugging
def show_teams():
    for j in TEAM_POOL:
        print()
        print(j)
        for k in TEAM_POOL[j]:
            team = TEAM_POOL[j][k]
            print(team)
            #random_player = team.get_roster()[rand.randint(0, len(team.get_roster())-1)]
            #print(random_player)


def results():
    for j in TEAM_POOL:
        print()
        print(j)
        for k in TEAM_POOL[j]:
            team = TEAM_POOL[j][k]



def main():
    start_wall = time.time()
    start_cpu = time.process_time()

    build_team_pool()
    for i in range(1):
        play_tourney()
        clear_teams()



    end_wall = time.time()
    end_cpu = time.process_time()

    print()
    print(f'Wall time: {end_wall - start_wall}')
    print(f'CPU time: {end_cpu - start_cpu}')


if __name__ == '__main__':
    main()
