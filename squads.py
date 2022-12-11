"""
Squads.py

Contains Team and Player classes to be used in main.py. Player influence metrics were calculated using spreadsheets
after cleaning the data. That method was chosen over making the calculation during data collection (harder to identify
errors in collection) and making the calculation during simulation (where it would be repeated every time the script
is run, which wasn't necessary or helpful in any way).
"""


# Team class used to store player objects and to record results for each simulation
class Team:

    def __init__(self, group, country, fifa_rank=1):
        # Country Data
        self.__country = country
        self.__group = group
        self.__roster = []
        self.__fifa_rank = fifa_rank  # used for debugging

        # Country Model-Relevant Values
        self.__tie_chance = 0
        self.__defense = 0

        # For tracking results in all simulations
        self.__points_in_group = []
        self.__lost_to = []
        self.__exit_stage = []
        self.__matches_won = []

        # For tracking results for one simulation
        self.__wins = 0
        self.__points = 0
        self.__ties = 0
        self.__lost = ''
        self.__exit = ''

    # used for debugging and writing result files
    def __str__(self):
        #return f'{self.__country}: {self.__wins}-W, {self.__ties}-T; {self.__exit}'
        return f'{self.__country},{self.matchday()},,,,\n'

    # calculates results of all simulations
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

        # returns string appropriate for writing to csv file
        return f'{self.get_country()},{avg_wins},{avg_points},{group},{ro16},{qtrs},{third},{rnup},{chmp}\n'

    # adds player object to roster
    def add_to_roster(self, player):
        self.__roster.append(player)

    # adds tie-chance value to object
    def add_tie_chance(self, num):
        self.__tie_chance = float(num)

    # adds defense value to object
    def add_defense(self, defense):
        self.__defense = float(defense)

    def add_win(self):
        self.__wins += 1

    def add_tie(self):
        self.__ties += 1

    def add_points(self, num):
        self.__points += num

    # returns a team strength value calculated using player data from the entire roster and defense value from object
    def matchday(self):
        def get_11():  # takes values from entire roster instead of choosing a starting eleven
            eleven = []
            for each in self.__roster:
                eleven.append(each)
            return eleven
        in_side = get_11()
        pform = self.__fifa_rank  # this value has a default of 1 which doesn't affect the model (order of magnitude)
        for p in in_side:
            if p.play_match():
                pform += p.play_match()  # adds a value derived from the data of each player object

        # CAN ADJUST DEFENSE INFLUENCE IN MODEL BY CHANGING MULTIPLIER BELOW
        pform += (self.__defense * 100) // 1  # floor division by 1 guarantees an int
        return pform

    # adds the results for a single simulation to the tabulation for all simulations
    def eliminated(self, exit_stage, beat_by=''):
        self.__exit = exit_stage
        self.__lost = beat_by
        self.__matches_won.append(self.__wins)
        self.__points_in_group.append(self.__points)
        self.__lost_to.append(beat_by)
        self.__exit_stage.append(exit_stage)

    # clears records for single simulation
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

    # prints roster or writes to file
    def show_full_roster(self, file=None):
        for p in self.__roster:
            if file:
                file.write(str(p))
            else:
                print(p)


# Player class used to store player data and return a value for their influence on a match
class Player:
    def __init__(self, eyed, name, position, gax90=0, csx90=0, matches=10):
        # Player Data
        self.__id = eyed
        self.__name = name
        self.__position = position

        # Player metrics calculated (in spreadsheet, not in Python) using scraped data
        self.__matches = int(matches)
        self.__gax90 = float(gax90)
        self.__csx90 = float(csx90)

        # Value for player influence on a match
        self.__form = self.calc_form()

    # used to debug and to write player influence in results
    def __str__(self):
        return f',,{self.play_match()},{self.__position},{self.__name},{self.__form}\n'

    # calculates a value to represent a players influence on the match, using data from csv
    def calc_form(self):
        # uses "Clean Sheets per 90" for Keepers, otherwise "Goal Involvements per 90"
        if self.__position == 'GK':
            form = self.__csx90
        else:
            form = self.__gax90

        # CAN ADJUST WEIGHTING OF GAMES PLAYED BELOW
        # lesser weighting for data based on less than 6 matches
        if self.__matches <= 3:
            return form * 0.5
        elif 3 < self.__matches <= 5:
            return form * 0.6
        else:
            return form

    # WEIGHTS PLAYER INFLUENCE VALUE DEPENDING ON POSITION - ADJUST BELOW
    def influence(self):
        if self.__position == 'GK':
            return 200
        elif self.__position == 'DF':
            return 200
        elif self.__position == 'MF':
            return 150
        elif self.__position == 'FW':
            return 130

    # returns final value for player influence based on data and relevant weighting
    def play_match(self):
        return int((self.__form * self.influence()) // 1)  # floor division by 1 guarantees int

    def get_name(self):
        return self.__name

    def get_position(self):
        return self.__position
