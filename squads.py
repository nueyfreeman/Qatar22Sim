

class Team:
    def __init__(self, group, country, fifa_rank=1):
        self.__country = country
        self.__group = group
        self.__roster = []
        self.__fifa_rank = fifa_rank

        self.__tie_chance = 0
        self.__defense = 0

        self.__points_in_group = []
        self.__lost_to = []
        self.__exit_stage = []
        self.__matches_won = []

        self.__wins = 0
        self.__points = 0
        self.__ties = 0
        self.__lost = ''
        self.__exit = ''

    def __str__(self):
        #return f'{self.__country}: {self.__wins}-W, {self.__ties}-T; {self.__exit}'
        return f'{self.__country},{self.matchday()},,,,\n'

    def calc_results(self):
        num_sims = len(self.__matches_won)

        # Average Matches Won
        matches = 0
        for i in self.__matches_won:
            matches += i
        avg_wins = matches / num_sims

        # Average Points in Group Stage
        points = 0
        for j in self.__points_in_group:
            points += j
        avg_points = points / num_sims

        # Exit Stage Distribution
        gs = 'Group Stage'
        group = (self.__exit_stage.count(gs) / num_sims) * 100
        six = '16'
        ro16 = (self.__exit_stage.count(six) / num_sims) * 100
        eight = 'Quarterfinals'
        qtrs = (self.__exit_stage.count(eight) / num_sims) * 100
        four = 'Semifinals'
        third = (self.__exit_stage.count(four) / num_sims) * 100
        two = 'Final'
        rnup = (self.__exit_stage.count(two) / num_sims) * 100
        one = 'Champion'
        chmp = (self.__exit_stage.count(one) / num_sims) * 100

        return f'{self.get_country()},{avg_wins},{avg_points},{group},{ro16},{qtrs},{third},{rnup},{chmp}\n'

    def add_to_roster(self, player):
        self.__roster.append(player)

    def add_tie_chance(self, num):
        self.__tie_chance = float(num)

    def add_defense(self, defense):
        self.__defense = float(defense)

    def add_win(self):
        self.__wins += 1

    def add_tie(self):
        self.__ties += 1

    def add_points(self, num):
        self.__points += num

    def matchday(self):
        def get_11():
            eleven = []
            for each in self.__roster:
                eleven.append(each)
            return eleven
        in_side = get_11()
        pform = self.__fifa_rank
        for p in in_side:
            if p.play_match():
                pform += p.play_match()
        pform += (self.__defense * 100) // 1
        return pform

    def eliminated(self, exit_stage, beat_by=''):
        self.__exit = exit_stage
        self.__lost = beat_by
        self.__matches_won.append(self.__wins)
        self.__points_in_group.append(self.__points)
        self.__lost_to.append(beat_by)
        self.__exit_stage.append(exit_stage)

    def clear(self):
        self.__wins = 0
        self.__points = 0
        self.__ties = 0
        self.__lost = ''
        self.__exit = ''

    def get_country(self):
        return self.__country

    def get_group(self):
        return self.__group

    def get_roster(self):
        return self.__roster

    def get_points(self):
        return self.__points

    def get_tie_chance(self):
        return self.__tie_chance

    def show_full_roster(self, file=None):
        for p in self.__roster:
            if file:
                file.write(str(p))
            else:
                print(p)


class Player:
    def __init__(self, eyed, name, position, gax90=0, csx90=0, matches=10):
        self.__id = eyed
        self.__name = name
        self.__position = position
        self.__matches = int(matches)
        self.__gax90 = float(gax90)
        self.__csx90 = float(csx90)
        self.__form = self.calc_form()

    def __str__(self):
        return f',,{self.play_match()},{self.__position},{self.__name},{self.__form}\n'

    def calc_form(self):
        if self.__position == 'GK':
            form = self.__csx90
        else:
            form = self.__gax90
        if self.__matches <= 3:
            return form * 0.5
        elif 3 < self.__matches <= 5:
            return form * 0.6
        else:
            return form

    def influence(self):
        if self.__position == 'GK':
            return 200
        elif self.__position == 'DF':
            return 200
        elif self.__position == 'MF':
            return 150
        elif self.__position == 'FW':
            return 130

    def play_match(self):
        return int((self.__form * self.influence()) // 1)

    def get_name(self):
        return self.__name

    def get_position(self):
        return self.__position
