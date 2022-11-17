"""
Qatar 2022
World Cup model
"""

import random as rand
import squads

GROUPS = 'ABCDEFGH'
WINNERS = {g: [1, 2] for g in GROUPS}
TEAM_POOL = {}


# reads in scraped data from csv, creates team objects in nested dictionaries, and fills their rosters
def build_team_pool():
    for i in GROUPS:
        TEAM_POOL[i] = {}
    file = open('QatarSquads.csv')
    i = 0

    for line in file:
        i += 1
        data = line.split(',')

        if not data[0] == 'Group':
            # expect exception if the team hasn't been made yet -- if error, then make team before adding player
            try:
                TEAM_POOL[data[0][6]][data[1]].add_to_roster(squads.Player(i, data[3], data[2]))
            except (TypeError, KeyError):
                TEAM_POOL[data[0][6]][data[1]] = squads.Team(data[0][6], data[1], rand.randint(0, 100))
                TEAM_POOL[data[0][6]][data[1]].add_to_roster(squads.Player(i, data[3], data[2]))

        """ UNCOMMENT TO DEBUG
        if i % 100 == 0:
            team = TEAM_POOL[data[0][6]][data[1]]
            print(team)
            print(team.get_roster()[rand.randint(0, len(team.get_roster())-1)])
            print()
        """
    file.close()


# bracket logic for group stage
def play_knockouts(aa, ab, ba, bb, ca, cb, da, db, ea, eb, fa, fb, ga, gb, ha, hb):
    m49 = match(aa, bb, '16')
    m50 = match(ca, db, '16')  # see official Fifa World Cup bracket for match-up structure
    m51 = match(ea, fb, '16')  # (a_ = Group A, b_ = Group B, etc)
    m52 = match(ga, hb, '16')  # (_a = Winner; _b = Runner-Up)
    m53 = match(ba, ab, '16')  # i.e. ab = Group A Runner-Up, fa = Group F Winner, etc
    m54 = match(da, cb, '16')
    m55 = match(fa, eb, '16')
    m56 = match(ha, gb, '16')

    m57 = match(m49, m50, 'quarters')
    m58 = match(m51, m52, 'quarters')
    m59 = match(m53, m54, 'quarters')
    m60 = match(m55, m56, 'quarters')

    m61 = match(m57, m58, 'semis')  # put the losers somewhere
    m62 = match(m59, m60, 'semis')

    champion = match(m61, m62, 'final')
    print(champion.get_country())


def play_groups():
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
                gt[t].eliminated('Group stage')




# nested loops -- each team meets one time
def group_matches(g_list):
    for i in range(len(g_list)):
        for j in range(len(g_list)-1-i):
            match(g_list[i], g_list[j + 1 + i], 'group')


# function to play one match, includes every outcome determined by stage in competition (taken as string)
    # returns a winner and eliminates loser in non-group matches, otherwise returns None
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
                t1.eliminated(stage, t2.get_country())
                winner = t2
        elif chance < team1:  # team 1 wins
            t1.add_win()
            if stage == 'group':
                t1.add_points(3)  # three points for winner
            else:
                t2.eliminated(stage, t1.get_country())  # record exit stats including stage and opponent
                winner = t1
        elif chance == team1:  # tie
            if stage == 'group':
                t1.add_points(1)  # one point to each
                t2.add_points(1)
                t1.add_tie()
                t2.add_tie()
            else:
                winner = play()  # recursively play for non-tie-able game
        return winner

    return play()


def main():
    build_team_pool()
    """
    play_knockouts(TEAM_POOL['A']['Ecuador'], TEAM_POOL['B']['Iran'], TEAM_POOL['B']['Wales'], TEAM_POOL['A']['Qatar'],
                   TEAM_POOL['C']['Mexico'], TEAM_POOL['D']['France'], TEAM_POOL['D']['Tunisia'],
                   TEAM_POOL['C']['Poland'], TEAM_POOL['E']['Japan'], TEAM_POOL['F']['Canada'],
                   TEAM_POOL['F']['Croatia'], TEAM_POOL['E']['Spain'], TEAM_POOL['G']['Brazil'],
                   TEAM_POOL['H']['Ghana'], TEAM_POOL['H']['Portugal'], TEAM_POOL['G']['Serbia'])
    """
    play_groups()
    show_teams()


def show_teams():
    for j in TEAM_POOL:
        print()
        print(j)
        for k in TEAM_POOL[j]:
            team = TEAM_POOL[j][k]
            print(team)
            #print(team.get_roster()[rand.randint(0, len(team.get_roster())-1)])


if __name__ == '__main__':
    main()
