

class Team:
    def __init__(self, group, country, fifa_rank):
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

    def __str__(self):
        return f'{self.__country}: ' \
               f'{self.__wins}-wins, {self.__ties}-ties, {self.__points}-points, ' \
               f'lost to {self.__lost_to} in {self.__exit_stage}'

    def add_to_roster(self, player):
        self.__roster.append(player)

    def add_win(self):
        self.__wins += 1

    def add_tie(self):
        self.__ties += 1

    def add_points(self, num):
        self.__points += num

    def eliminated(self, exit_stage, beat_by='Lost in group'):
        self.__exit_stage = exit_stage
        self.__lost_to = beat_by
        self.__matches_won.append(self.__wins)
        self.__points_in_group.append(self.__points)

    def clear_sim(self):
        self.__wins = 0
        self.__points = 0

    def get_country(self):
        return self.__country

    def get_group(self):
        return self.__group

    def get_roster(self):
        return self.__roster

    def get_points(self):
        return self.__points

    def set_fifa_score(self):
        pass

    def matchday(self):
        def get_11():
            return self.__roster
        in_side = get_11()
        pform = self.__fifa_rank
        for p in in_side:
            if p.play_match():
                pform += p.play_match()
        return pform


class Player:
    def __init__(self, eyed, name, position):
        self.__id = eyed
        self.__name = name
        self.__position = position
        self.__gx90 = float(0)
        self.__ax90 = float(0)
        self.__csx90 = float(0)

    def __str__(self):
        return f'#{self.__id} {self.__position} {self.__name}'

    def play_match(self):
        pass

    def get_position(self):
        return self.__position
