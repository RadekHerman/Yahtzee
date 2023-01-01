import random
import time
import os
from dice_images import dice_img

class Player():
    def __init__(self, name):
        self.name = name
        self.dice_number = 0

    # number of dice to roll getter and setter
    @property
    def dice_number(self):
        return self._dice_number

    @dice_number.setter
    def dice_number(self, n):
        self._dice_number = n

    # create players function
    # nazwy graczy powinny być różne <<<<<<<<<<<<<<<<<< to do
    def get_players(no_players):
        players_names=[]    
        for player in range(no_players):
            name = input("name")
            players_names.append(name)
        players_objs = []
        # create player instances and keep them in players_objs
        for i in players_names:
            players_objs.append(Player(i))
        return players_objs

    # select dice from roll result function
    def select_dice(self, roll_result, selected=None):
        if selected == None:
            selected = []
        print(f"please select dice you want to keep, use comma: {roll_result}")
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
        # if selected == None or selected == selected == []:
        #     return "All dice ready to roll" 

        print(f"please select dice you want to put back for next roll, use comma: {selected}")
        put_back_string = input("..: ").strip()
        # select only from those that are currently to keep, ignore other inputs
        put_back_list = []
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

    
    # dice roll, number of dices
    def get_roll(self, dice_number):
        # self.dice_number = dice_number
        roll = []
        for dice in range(dice_number):
            dice = random.randint(1, 6)
            time.sleep(0.2)
            roll.append(dice)        
        return roll
                

class Game():
    def __init__(self, data_dictionary):
        # number of rounds (będzie potrzebny update)
        self.round = 1
        self.data_dictionary = data_dictionary
    
    def create_data_dictionary(self, players_objs):
        names = []
        for x in range(len(players_objs)):
            names.append(players_objs[x].name)

        self.data_dictionary = {"Category": [], "Aces":[], "Twos":[], "Threes":[], 
        "Fours":[], "Fives":[], "Sixes":[], "Three Of A Kind":[], 
        "Four Of A Kind":[], "Full House":[], "Small Straight":[], 
        "Large Straight":[], "Yahtzee":[], "Chance":[]}

        for name in names:
            self.data_dictionary["Category"].append(name)
            self.data_dictionary["Aces"].append("-")
            self.data_dictionary["Twos"].append("-")
            self.data_dictionary["Threes"].append("-")
            self.data_dictionary["Fours"].append("-")
            self.data_dictionary["Fives"].append("-")
            self.data_dictionary["Sixes"].append("-")
            self.data_dictionary["Three Of A Kind"].append("-")
            self.data_dictionary["Four Of A Kind"].append("-")
            self.data_dictionary["Full House"].append("-")
            self.data_dictionary["Small Straight"].append("-")
            self.data_dictionary["Large Straight"].append("-")
            self.data_dictionary["Yahtzee"].append("-")
            self.data_dictionary["Chance"].append("-")

        return self.data_dictionary

    def print_table(self,no_players, data_dictionary):
        table = []     
        row_format ="{:>15}" * (no_players + 1)
        table.append("-"*((no_players * 17)+ 20))
        for key, value in data_dictionary.items():
            table.append(row_format.format(key, *value))
            table.append("-"*((no_players * 17)+ 20))
        return "\n".join(table)

        
    def update_table(self, player_name, key, value):
        # update data
        # check index of the player
        index_name = self.data_dictionary["Category"].index(player_name)
        print(index_name)
        #print(self.data_dictionary[key][index_name])
        # print(self.data_dictionary["Aces"][index_name])
        # use index to update data
        self.data_dictionary[key][index_name] = value
        print(self.data_dictionary[key][index_name])
                

    def check_table_if_no_score(self, player_name):
        print(player_name, "player name form check")
        player_table_values=[]
        index_name = self.data_dictionary["Category"].index(player_name)
        #print(self.data_dictionary.keys())
        for key, value in self.data_dictionary.items():
            #print(value[index_name])
            if value[index_name] == "-":
                player_table_values.append(key)
        
        return player_table_values
        

    def check_current_scoring(self, player_name, all_current_dice):
        
        player_table_values = self.check_table_if_no_score(player_name)
        print(player_table_values, "player values")

        current_scoring = []
        if 1 in all_current_dice:
            score = 1 * all_current_dice.count(1)
            if "Aces" in player_table_values:
                current_scoring.append(f"Aces score: {score}")
                print(f"Aces score: {score}")
            
        if 2 in all_current_dice:
            score = 2 * all_current_dice.count(2)
            if "Twos" in player_table_values:
                current_scoring.append(f"Twos score: {score}")            
                print(f"Twos score: {score}")
        if 3 in all_current_dice:
            score = 3 * all_current_dice.count(3)
            if "Threes" in player_table_values:
                current_scoring.append(f"Threes score: {score}")            
                print(f"Threes score: {score}")
        if 4 in all_current_dice:
            score = 4 * all_current_dice.count(4)
            if "Fours" in player_table_values:
                current_scoring.append(f"Fours score: {score}")            
                print(f"Fours score: {score}")
        if 5 in all_current_dice:
            score = 5 * all_current_dice.count(5)
            if "Fives" in player_table_values:
                current_scoring.append(f"Fives score: {score}")            
                print(f"Fives score: {score}")
        if 6 in all_current_dice:
            score = 6 * all_current_dice.count(6)
            if "Sixes" in player_table_values:
                current_scoring.append(f"Sixes score: {score}")                
                print(f"Sixes score: {score}")

        # Three Of A Kind
        for x in all_current_dice:
            if all_current_dice.count(x) >= 3:
                if "Three Of A Kind" in player_table_values:
                    current_scoring.append(f"Three Of A Kind: {sum(all_current_dice)}")
                    print(f"Three of kind: {sum(all_current_dice)}")
                    break

        # Four Of A Kind
        for x in all_current_dice:
            if all_current_dice.count(x) >= 4:
                if "Four Of A Kind" in player_table_values:
                    current_scoring.append(f"Four Of A Kind: {sum(all_current_dice)}")
                    print(f"Four of kind: {sum(all_current_dice)}")
                    break

        # Full House
        full_house=[]
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
                current_scoring.append(f"Full House: 25 score")
                print(f"Full House: 25 score")


        # Small Straight
        # (1-2-3-4, 2-3-4-5, or 3-4-5-6)
        if(all(x in all_current_dice for x in [1,2,3,4])) or (all(x in all_current_dice for x in [2,3,4,5])) or (all(x in all_current_dice for x in [3,4,5,6])):
            if "Small Straight" in player_table_values:
                current_scoring.append(f"Small Straight: 30 score")
                print(f"Small Straight: 30 score")

        # Large Straight
        # (1-2-3-4-5 or 2-3-4-5-6)
        if(all(x in all_current_dice for x in [1,2,3,4,5])) or (all(x in all_current_dice for x in [2,3,4,5,6])):
            if "Large Straight" in player_table_values:
                current_scoring.append(f"Large Straight: 40 score")
                print(f"Large Straight: 40 score")

        # Yahtzee
        for x in all_current_dice:
            if all_current_dice.count(x) == 5:
                if "Yahtzee" in player_table_values:
                    current_scoring.append(f"Yahtzee: 50 points")
                    print(f"Yahtzee: 50 points")
                    break

        # Chance
        if "Chance" in player_table_values:
            current_scoring.append(f"Chance: {sum(all_current_dice)}")
            print(f"Chance: {sum(all_current_dice)}")

        #print(current_scoring, "current_scoring list")
        return "\n".join(current_scoring)

        
class Terminal():
    # class will print all results in terminal
    result_header = " ROLL RESULT / DICE TO ROLL".center(60, "~") + "\n"
    selection_header = "\n" + " SELECTED DICE ".center(60, "~") + "\n"

    @classmethod
    # create view of dices in terminal
    def dice_output(cls, dice_numbers_for_print):
        # import selected images form dices.py into list
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
        

    # full terminal output
    @classmethod
    def output(cls, roll, selected_dice=None):
        if selected_dice == None:
            selected_dice = []
        # create dice view of result 
        roll_row = cls.dice_output(roll)
        # create dice view of selected dice
        selected_row = cls.dice_output(selected_dice)
        # all_current_dice = roll + selected_dice
        # current_scoring = game.check_current_scoring(all_current_dice)
        # print(roll, "ROLL", selected_dice, "SELECTED DICE")
        # return full terminal output
        return cls.result_header + roll_row + cls.selection_header + selected_row 


def play():
    os.system('clear') #<<<<<<<<<<<<<<< to do - w innych miejscach <<<<<<<<<<<<
    # create the players
    #określić maksymalną liczbę ze względu na terminal, chyba 1-6 <<<<<<<<<<<< to do
    no_players = int(input("Please enter the number of players: "))
    players_objs = Player.get_players(no_players)
    # create game
    data_dictionary = {}
    game = Game(data_dictionary)
    # create dictionary for table scores input
    # data_dictionary = game.create_dictionary_data(players_objs)
    game.data_dictionary = game.create_data_dictionary(players_objs)
    print(game.data_dictionary, "game.data_dictionary when game created")

    print(f"Round: {game.round}")
    # game 
        # get roll
    for x in range(no_players):
        selected = []
        # number of dive to roll
        players_objs[x].dice_number = 5
        # FIRST ROLL
        rolls = 1
        print(f"{players_objs[x].name} Turn")
        input(f"To roll dice, press any key.")
        roll_result = players_objs[x].get_roll(players_objs[x].dice_number)
        # print roll results
        print(Terminal.output(roll_result))
        # check current scoring based on all current dice
        all_current_dice = roll_result + selected
        print(game.check_current_scoring(players_objs[x].name, all_current_dice))
        # what you want to do next
        while rolls < 3:
            while True:
                what_next = input("Select dice to keep (1) or put back dice for next roll(2) or choose the score(3) or print current table(4) or roll the dice(5): ") 
                if what_next == "1":
                    # select dice to keep from the roll    
                    selected += players_objs[x].select_dice(roll_result)
                    print(f"{selected} selected {roll_result} roll result # after select_dice function in play()")
                    # print in terminal dice to roll and selected ones
                    print(Terminal.output(roll_result, selected))
                    # check current scoring based on all current dice
                    all_current_dice = roll_result + selected
                    print("current scoring from play()")
                    print(game.check_current_scoring(players_objs[x].name, all_current_dice))
                    pass

                elif what_next == "2":
                    # put back dice for next roll
                    if selected == []:
                        print(Terminal.output(roll_result, selected))
                        print("---------->>> All dice ready to roll! <<<----------" +"\n")
                        
                    else:
                        selected = players_objs[x].put_back_dice(roll_result, selected)
                        print(f"{selected} selected {roll_result} roll result # after put_back function in play()")
                        print(Terminal.output(roll_result, selected))

                    pass
                elif what_next == "3":
                    # choose the score(3)
                    rolls = 3
                    break
                elif what_next == '4':
                    #print(game.print_table(no_players, data_dictionary))
                    print(game.print_table(no_players, game.data_dictionary))
                    pass
                elif what_next == "5":
                    # roll
                    # enter for next roll
                    input(f"To roll dice, press any key.")
                    roll_result = players_objs[x].get_roll(players_objs[x].dice_number)
                    print(Terminal.output(roll_result, selected))
                    all_current_dice = roll_result + selected
                    print(game.check_current_scoring(players_objs[x].name, all_current_dice))
                    print(all_current_dice, "TOTAL")
                    break
                else:
                    pass
            rolls += 1
        
        print("Choose score for the table")
        key = input("input key")
        value = input("value")
        game.update_table(players_objs[x].name, key, value)
        print(game.print_table(no_players, game.data_dictionary))



        # dice selecton or table choice

            #if dice selection get another roll
            
                # dice selecton or table choice

            # if table, update table 


if __name__ == '__main__':
    play()



