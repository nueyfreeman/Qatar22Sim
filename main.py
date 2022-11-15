"""
Qatar 2022
World Cup model
"""

import random as rand
import squads

GROUPS = 'ABCDEFGH'
TEAM_POOL = {}


class Group:
    def __init__(self, team1, team2, team3, team4):
        self.__t1 = team1
        self.__t2 = team2
        self.__t3 = team3
        self.__t4 = team4
        self.__standings = [{'t1': 0}, {'t2': 0}, {'t3': 0}, {'t4': 0}]
        self.play_group()

    def play_group(self):
        pass


def build_team_pool():
    for i in GROUPS:
        TEAM_POOL[i] = []
    file = open('QatarSquads.csv')
    file.readline()

    i = file.readline()
    data = i.split(',')
    print(data)

    TEAM_POOL[data[0][6]] = {data[1]: squads.Team(data[1], rand.randint(0, 100))}
    TEAM_POOL[data[0][6]][data[1]].add_to_roster(squads.Player(1, data[3], data[2]))

    print(TEAM_POOL['A']['Ecuador'].matchday())
    print(TEAM_POOL['A']['Ecuador'].get_roster()[0].get_position())

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
    #third = match  # LOSERS GO HERE


# function to play one match, includes every outcome determined by stage in competition (taken as string)
    # returns a winner and eliminates loser in non-group matches, otherwise returns None and sends teams back to groups
        # ADD IMPLEMENTATION TO RETURN TO GROUPS
def match(t1, t2, stage):
    team1 = t1.matchday()
    team2 = t2.matchday()
    prob = team1 + team2

    def play():
        chance = rand.randint(0, prob)
        winner = None
        if chance > team1:  # team 2 wins
            t2.add_win()
            if stage == 'group':  # for group match send both teams back to group
                t2.add_points(3)
                #.append(t2)
                #.append(t1)
            else:  # for knockout match send loser to team pool and return winner
                t1.eliminated(stage, t2.get_country())
                TEAM_POOL.append(t1)
                winner = t2
        elif chance < team1:  # team 1 wins
            t1.add_win()
            if stage == 'group':
                t1.add_points(3)  # three points for winner and return both teams to group
                #.append(t1)
                #.append(t2)
            else:
                t2.eliminated(stage, t1.get_country())  # record exit stats including stage and opponent
                TEAM_POOL.append(t2)
                winner = t1
        elif chance == team1:  # tie
            if stage == 'group':
                t1.add_points(1)  # one point to each and return to group
                t2.add_points(1)
                #.append(t1)
                #.append(t2)
            else:
                play()  # recursively play for non-tie-able game
        return winner

    return play()


def main():
    build_team_pool()


if __name__ == '__main__':
    main()
