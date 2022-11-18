

class Team:
    def __init__(self, group, country, fifa_rank=1):
        self.__country = country
        self.__group = group
        self.__roster = []
        self.__fifa_rank = fifa_rank

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
        return f'{self.__country},{self.matchday()},,,,\n'

    def add_to_roster(self, player):
        self.__roster.append(player)

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

    def show_full_roster(self, file=None):
        for p in self.__roster:
            if file:
                file.write(str(p))
            else:
                print(p)

    def set_fifa_score(self):
        pass


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
            return 110

    def play_match(self):
        return int((self.__form * self.influence()) // 1)

    def get_name(self):
        return self.__name

    def get_position(self):
        return self.__position
