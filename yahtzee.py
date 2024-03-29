"""
Yahtzee implementation by Radosław Herman 
"""

import random
import time
import os
from dice_images import dice_img
import re


class Player:
    def __init__(self, name):
        self.name = name
        self.dice_number = 0
        self.bonus = False

    # number of dice to roll getter and setter
    @property
    def dice_number(self):
        return self._dice_number

    @dice_number.setter
    def dice_number(self, n):
        self._dice_number = n

    # create players function
    def get_players(no_players):
        players_names = []
        for player in range(1, no_players + 1):
            name = input(f"Please enter player no. {player} name.: ")
            while True:
                if name in players_names:
                    print("This name has been already taken by another player.")
                    name = input(
                        f"Please enter another name for player no. {player}.: "
                    )
                    continue
                else:
                    break
            players_names.append(name)

        # create player instances and keep them in players_objs
        players_objs = [Player(i) for i in players_names]

        return players_objs

    # select dice from roll result function
    def select_dice(self, roll_result, selected=None):
        if selected == None:
            selected = []
        print(f"Please select dice you want to keep, use comma: {roll_result}")
        selected_string = input("..: ").strip()
        # select only from those that have been rolled, ignore other inputs
        for x in selected_string.split(","):
            if x.strip() in ["1", "2", "3", "4", "5", "6"]:
                x = int(x.strip())
                if x in roll_result:
                    roll_result.remove(x)
                    selected.append(x)
            else:
                pass
        # update dice number for next roll
        self.dice_number = self.dice_number - len(selected)
        # print(self.dice_number, "liczba pozostałych")
        return selected

    def put_back_dice(self, roll_result, selected=None):
        #     return "All dice ready to roll"
        print(
            f"Please select dice you want to put back for the next roll, use comma: {selected}"
        )
        put_back_string = input("..: ").strip()
        # select only from those that are currently to keep, ignore other inputs
        for x in put_back_string.split(","):
            if x.strip() in ["1", "2", "3", "4", "5", "6"]:
                x = int(x.strip())
                if x in selected:
                    selected.remove(x)
                    roll_result.append(x)
            else:
                pass
        # update dice number for next roll
        self.dice_number = 5 - len(selected)
        return selected

    # dice roll, number of dice
    def get_roll(self, dice_number):
        roll = []
        for dice in range(dice_number):
            dice = random.randint(1, 6)
            time.sleep(random.uniform(0.05, 0.2))
            roll.append(dice)
        return roll


class Game:
    def __init__(self, data_dictionary):
        self.data_dictionary = data_dictionary

    def create_data_dictionary(self, players_objs):

        names = [players_objs[x].name for x in range(len(players_objs))]

        self.data_dictionary = {
            "Category": [],
            "Aces": [],
            "Twos": [],
            "Threes": [],
            "Fours": [],
            "Fives": [],
            "Sixes": [],
            "Sum": [],
            "Bonus": [],
            "Three Of A Kind": [],
            "Four Of A Kind": [],
            "Full House": [],
            "Small Straight": [],
            "Large Straight": [],
            "Yahtzee": [],
            "Chance": [],
            "TOTAL SUM": [],
        }

        for name in names:
            self.data_dictionary["Category"].append(name)
            self.data_dictionary["Aces"].append("-")
            self.data_dictionary["Twos"].append("-")
            self.data_dictionary["Threes"].append("-")
            self.data_dictionary["Fours"].append("-")
            self.data_dictionary["Fives"].append("-")
            self.data_dictionary["Sixes"].append("-")
            self.data_dictionary["Sum"].append(" ")
            self.data_dictionary["Bonus"].append(" ")
            self.data_dictionary["Three Of A Kind"].append("-")
            self.data_dictionary["Four Of A Kind"].append("-")
            self.data_dictionary["Full House"].append("-")
            self.data_dictionary["Small Straight"].append("-")
            self.data_dictionary["Large Straight"].append("-")
            self.data_dictionary["Yahtzee"].append("-")
            self.data_dictionary["Chance"].append("-")
            self.data_dictionary["TOTAL SUM"].append(" ")

        return self.data_dictionary

    def print_table(self, no_players, data_dictionary):
        table = []
        row_format = "{:>15}" * (no_players + 1)
        table.append("-" * ((no_players * 17) + 20))
        for key, value in data_dictionary.items():
            table.append(row_format.format(key, *value))
            table.append("-" * ((no_players * 17) + 20))
        return "\n".join(table)

    def update_table(self, player_name, key, value):
        # update data
        # check index of the player
        index_name = self.data_dictionary["Category"].index(player_name)
        # use index to update data
        self.data_dictionary[key][index_name] = value

    def check_upper_section(self, player_name):
        upper_category = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes"]
        upper_sum = 0
        scored_category = []
        # if upper sum >= 63
        upper_bonus = 35
        index_name = self.data_dictionary["Category"].index(player_name)
        for category in upper_category:
            if self.data_dictionary[category][index_name] != "-":
                upper_sum += self.data_dictionary[category][index_name]
                scored_category.append(category)

        if len(scored_category) == 6:
            self.update_table(player_name, "Sum", upper_sum)
            if upper_sum >= 63:
                self.update_table(player_name, "Bonus", upper_bonus)
            else:
                self.update_table(player_name, "Bonus", 0)
            return True
        return False

    def sum_up_total(self, player_name):
        lower_sum = 0
        index_name = self.data_dictionary["Category"].index(player_name)
        upper_sum = self.data_dictionary["Sum"][index_name]
        bonus = self.data_dictionary["Bonus"][index_name]
        lower_category = [
            "Three Of A Kind",
            "Four Of A Kind",
            "Full House",
            "Small Straight",
            "Large Straight",
            "Yahtzee",
            "Chance",
        ]
        for category in lower_category:
            lower_sum += self.data_dictionary[category][index_name]

        total_sum = upper_sum + bonus + lower_sum
        self.update_table(player_name, "TOTAL SUM", total_sum)
        return upper_sum + bonus + lower_sum

    def check_table_if_no_score(self, player_name):
        player_table_values = []
        index_name = self.data_dictionary["Category"].index(player_name)
        for key, value in self.data_dictionary.items():
            if value[index_name] == "-":
                player_table_values.append(key)

        return player_table_values

    def check_winner(self, no_players, players_objs):
        players_total_score = {}
        for x in range(no_players):
            index_name = self.data_dictionary["Category"].index(players_objs[x].name)
            players_total_score[players_objs[x].name] = self.data_dictionary[
                "TOTAL SUM"
            ][index_name]

        top_score = max(players_total_score.values())
        top_player = max(players_total_score, key=players_total_score.get)

        return f"\nThe Winner is: {top_player} with the score {top_score} points."

    def check_current_scoring(self, player_name, all_current_dice):

        player_table_values = self.check_table_if_no_score(player_name)

        # check the possible scoring from the current roll result
        current_scoring = []
        if 1 in all_current_dice:
            score = 1 * all_current_dice.count(1)
            if "Aces" in player_table_values:
                current_scoring.append(f"Aces: {score} points")

        if 2 in all_current_dice:
            score = 2 * all_current_dice.count(2)
            if "Twos" in player_table_values:
                current_scoring.append(f"Twos: {score} points")

        if 3 in all_current_dice:
            score = 3 * all_current_dice.count(3)
            if "Threes" in player_table_values:
                current_scoring.append(f"Threes: {score} points")

        if 4 in all_current_dice:
            score = 4 * all_current_dice.count(4)
            if "Fours" in player_table_values:
                current_scoring.append(f"Fours: {score} points")

        if 5 in all_current_dice:
            score = 5 * all_current_dice.count(5)
            if "Fives" in player_table_values:
                current_scoring.append(f"Fives: {score} points")

        if 6 in all_current_dice:
            score = 6 * all_current_dice.count(6)
            if "Sixes" in player_table_values:
                current_scoring.append(f"Sixes: {score} points")

        # Three Of A Kind
        for x in all_current_dice:
            if all_current_dice.count(x) >= 3:
                if "Three Of A Kind" in player_table_values:
                    current_scoring.append(
                        f"Three Of A Kind: {sum(all_current_dice)} points"
                    )
                    break

        # Four Of A Kind
        for x in all_current_dice:
            if all_current_dice.count(x) >= 4:
                if "Four Of A Kind" in player_table_values:
                    current_scoring.append(
                        f"Four Of A Kind: {sum(all_current_dice)} points"
                    )
                    break

        # Full House
        full_house = []
        full_house_check = all_current_dice.copy()
        for x in full_house_check:
            if full_house_check.count(x) == 3:
                full_house.append(x)
                for y in range(3):
                    full_house_check.remove(x)
                for x in full_house_check:
                    if full_house_check.count(x) == 2:
                        full_house.append(x)
                        for y in range(2):
                            full_house_check.remove(x)
        if len(full_house) == 2:
            if "Full House" in player_table_values:
                current_scoring.append(f"Full House: 25 points")

        # Small Straight
        # (1-2-3-4, 2-3-4-5, or 3-4-5-6)
        if (
            (all(x in all_current_dice for x in [1, 2, 3, 4]))
            or (all(x in all_current_dice for x in [2, 3, 4, 5]))
            or (all(x in all_current_dice for x in [3, 4, 5, 6]))
        ):
            if "Small Straight" in player_table_values:
                current_scoring.append(f"Small Straight: 30 points")
                # print(f"Small Straight: 30 score")

        # Large Straight
        # (1-2-3-4-5 or 2-3-4-5-6)
        if (all(x in all_current_dice for x in [1, 2, 3, 4, 5])) or (
            all(x in all_current_dice for x in [2, 3, 4, 5, 6])
        ):
            if "Large Straight" in player_table_values:
                current_scoring.append(f"Large Straight: 40 points")

        # Yahtzee
        for x in all_current_dice:
            if all_current_dice.count(x) == 5:
                if "Yahtzee" in player_table_values:
                    current_scoring.append(f"Yahtzee: 50 points")
                    break

        # Chance
        if "Chance" in player_table_values:
            current_scoring.append(f"Chance: {sum(all_current_dice)} points")

        # return list of available score options
        if len(current_scoring) >= 1:
            return current_scoring
        # if you don't have any available category from the roll you have to choose other with 0 points.
        else:
            for x in player_table_values:
                current_scoring.append(f"{x}: 0 points")

            return current_scoring


class Terminal:
    # class will print results in terminal
    result_header = " ROLL RESULT / DICE TO ROLL ".center(60, "~") + "\n"
    selection_header = "\n" + " SELECTED DICE TO KEEP ".center(60, "~") + "\n"
    current_scoring_header = "\n" + " CURRENT SCORING ".center(60, "~") + "\n"

    @classmethod
    # create view of dice in terminal
    def dice_output(cls, dice_numbers_for_print):
        # import selected images form dice.py into list
        dice_list_for_print = []
        for dice in dice_numbers_for_print:
            dice_list_for_print.append(dice_img[dice])
        # create rows for proper print in terminal
        rows = []
        for row in range(5):
            row_components = []
            for d in dice_list_for_print:
                row_components.append(d[row])
            row_string = "  ".join(row_components)
            rows.append(row_string)
        return "\n".join(rows)

    # terminal output
    @classmethod
    def output(cls, roll, selected_dice=None):
        if selected_dice == None:
            selected_dice = []
        # create dice view of result
        roll_row = cls.dice_output(roll)
        # create dice view of selected dice
        selected_row = cls.dice_output(selected_dice)
        return (
            cls.result_header
            + roll_row
            + cls.selection_header
            + selected_row
            + cls.current_scoring_header
        )

    @staticmethod
    def whats_next():
        whats_next = [
            "1. Select dice to keep.",
            "2. Put back dice for next roll.",
            "3. Choose the score from available.",
            "4. Show the current scoring table.",
            "5. Roll the dice.\n",
        ]
        return "\n".join(whats_next)


def play():
    os.system("clear")
    # create the players
    print("Welcome to Yahtzee.\n")
    while True:
        try:
            no_players = int(input("Please enter the number of players (1-6): "))
        except ValueError:
            print("It is not a number. Please try again.")
            continue
        else:
            if no_players >= 1 and no_players <= 6:
                break
            else:
                print("Number should be between 1 and 6")

    players_objs = Player.get_players(no_players)
    # create game
    data_dictionary = {}
    game = Game(data_dictionary)
    # create dictionary for table scores input
    game.data_dictionary = game.create_data_dictionary(players_objs)
    game_round = 1

    # game
    while game_round <= 13:
        for x in range(no_players):
            selected = []
            # number of dive to roll
            players_objs[x].dice_number = 5
            # FIRST ROLL
            rolls = 1
            os.system("clear")
            print(f"Round: {game_round}")
            print(f"{players_objs[x].name}'s turn")
            input(f"To roll the dice, press any key.")
            roll_result = players_objs[x].get_roll(players_objs[x].dice_number)

            while rolls < 3:
                while True:
                    os.system("clear")
                    print(f"Round: {game_round}")
                    print(f"{players_objs[x].name}'s turn")
                    print(Terminal.output(roll_result, selected))
                    # check current scoring based on all current dice
                    all_current_dice = roll_result + selected
                    # current scoring print/select
                    current_scoring = game.check_current_scoring(
                        players_objs[x].name, all_current_dice
                    )
                    for index, scoring in enumerate(current_scoring, start=1):
                        print(f"{index}. {scoring}")
                    print("\n" + " SELECT YOUR NEXT MOVE  ".center(60, "~") + "\n")
                    print(Terminal.whats_next())
                    what_next = input(
                        "Please choose a number (1) Keep, (2) Put Back, (3) Score, (4) Table or (5) Roll: "
                    )

                    if what_next == "1":
                        # select dice to keep from the roll
                        selected += players_objs[x].select_dice(roll_result)
                        pass

                    elif what_next == "2":
                        # put back dice for next roll
                        if selected == []:
                            print(
                                "\n---------->>> All dice ready to roll! <<<----------"
                                + "\n"
                            )
                            input("\nPress any key to continue.")
                        else:
                            selected = players_objs[x].put_back_dice(
                                roll_result, selected
                            )
                        pass

                    elif what_next == "3":
                        # choose the score
                        rolls = 3
                        break
                    elif what_next == "4":
                        # show table
                        os.system("clear")
                        print(game.print_table(no_players, game.data_dictionary))
                        input("Press any key to continue.")
                        pass
                    elif what_next == "5":
                        # roll
                        roll_result = players_objs[x].get_roll(
                            players_objs[x].dice_number
                        )
                        break
                    else:
                        pass
                rolls += 1

            # input fo tables
            while True:
                os.system("clear")
                print(f"Round: {game_round}")
                print(f"{players_objs[x].name}'s turn")
                print(Terminal.output(roll_result, selected))
                all_current_dice = roll_result + selected
                current_scoring = game.check_current_scoring(
                    players_objs[x].name, all_current_dice
                )
                for index, scoring in enumerate(current_scoring, start=1):
                    print(f"{index}. {scoring}")
                try:
                    score_selection = (
                        int(
                            input(
                                "\n"
                                + "Please choose your scoring (use index number).: "
                            )
                        )
                        - 1
                    )
                except ValueError:
                    continue
                else:
                    if score_selection >= 0 and score_selection < len(current_scoring):
                        break
                    continue

            print(
                f"\nYour choice >>>> {current_scoring[score_selection]} <<<< will be put in the table.\n"
            )
            input("Press any key to continue.")
            os.system("clear")
            print(f"Round: {game_round}")
            print(f"{players_objs[x].name}'s turn")

            # get key and value for table
            key_value_for_table = re.match(
                r"(^.+)(:\s)(\d+)(\s.*)$", current_scoring[score_selection]
            )
            key = key_value_for_table.group(1)
            value = int(key_value_for_table.group(3))

            game.update_table(players_objs[x].name, key, value)
            # check bonus
            if players_objs[x].bonus == False:
                players_objs[x].bonus = game.check_upper_section(players_objs[x].name)

            if game_round == 13:
                game.sum_up_total(players_objs[x].name)

            print(game.print_table(no_players, game.data_dictionary))
            input("Press any key to continue.")

        game_round += 1

    os.system("clear")
    print(game.print_table(no_players, game.data_dictionary))
    print(game.check_winner(no_players, players_objs))

    play_again = input("(Y) to play again.:").upper()
    if play_again == "Y":
        play()


if __name__ == "__main__":
    play()