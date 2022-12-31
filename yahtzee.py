import random
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
        return(selected)

    # dice roll, number of dices
    def get_roll(self, dice_number):
        # self.dice_number = dice_number
        roll = []
        for dice in range(dice_number):
            dice = random.randint(1, 6)
            roll.append(dice)        
        return roll
                


class Game():
    def __init__(self):
        # number of rounds (będzie potrzebny update)
        self.round = 1
    
    def create_data_dictionary(self, players_objs):
        names = []
        for x in range(len(players_objs)):
            names.append(players_objs[x].name)

        data = {"Category": [], "Aces":[], "Twos":[], "Threes":[], 
        "Fours":[], "Fives":[], "Sixes":[], "Three Of A Kind":[], 
        "Four Of A Kind":[], "Full House":[], "Small Straight":[], 
        "Large Straight":[], "Yahtzee":[], "Chance":[]}

        for name in names:
            data["Category"].append(name)
            data["Aces"].append("-")
            data["Twos"].append("-")
            data["Threes"].append("-")
            data["Fours"].append("-")
            data["Fives"].append("-")
            data["Sixes"].append("-")
            data["Three Of A Kind"].append("-")
            data["Four Of A Kind"].append("-")
            data["Full House"].append("-")
            data["Small Straight"].append("-")
            data["Large Straight"].append("-")
            data["Yahtzee"].append("-")
            data["Chance"].append("-")

        return data

    def print_table(self,no_players, data_dictionary):
        table = []
        
        row_format ="{:>15}" * (no_players + 1)
        table.append("-"*((no_players * 17)+ 20))
        for key, value in data_dictionary.items():
            table.append(row_format.format(key, *value))
            table.append("-"*((no_players * 17)+ 20))

        return "\n".join(table)

        
    def update_table(self):
        
        pass

    def check_table(self):
        pass
    
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

        # return full terminal output
        return cls.result_header + roll_row + cls.selection_header + selected_row 


def play():
    # create the players
    no_players = int(input("number of players"))
    players_objs = Player.get_players(no_players)
    # create game
    game = Game()
    data_dictionary = game.create_data_dictionary(players_objs)

    print(f"Round: {game.round}")
    # game 
        # get roll
    for x in range(no_players):
        selected = []
        players_objs[x].dice_number = 5
        # FIRST ROLL
        rolls = 1
        print(f"{players_objs[x].name} Turn")
        input(f"To roll dice, press any key.")
        roll_result = players_objs[x].get_roll(players_objs[x].dice_number)
        # print roll results
        print(Terminal.output(roll_result))
        # what you want to do next
        while rolls < 3:
            while True:
                what_next = input("Select dice to keep & roll(1) or choose the score(2) or print current table(3): ") 
                if what_next == "1":
                    # select dice to keep from the roll    
                        selected += players_objs[x].select_dice(roll_result)
                        print(Terminal.output(roll_result, selected))
                        input(f"To roll dice, press any key.")
                        roll_result = players_objs[x].get_roll(players_objs[x].dice_number)
                        print(Terminal.output(roll_result, selected))
                        break
                elif what_next == "2":
                    rolls = 3
                    break
                elif what_next == '3':
                    print(game.print_table(no_players, data_dictionary))
                    pass
                else:
                    pass
            rolls += 1
        
        print("Choose score for the table")
        



        # dice selecton or table choice

            #if dice selection get another roll
            
                # dice selecton or table choice

            # if table, update table 


if __name__ == '__main__':
    play()



