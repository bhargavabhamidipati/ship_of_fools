import random

class Die:
    '''
    Responsible for handling randomly generated
    integer values between 1 and 6.
    '''

    def __init__(self):
        '''
        constructor
        '''
        self.roll()

    def get_value(self):
        '''
        a method to get the current value of a die
        '''
        return self._value

    def roll(self):
        '''
        a method to generate a random number for a die
        '''
        self._value=random.randint(1,6)


class DiceCup:
    '''
    Handles five objects (dice) of class Die.
    Has the ability to bank and release dice individually.
    Can also roll dice that are not banked.
    '''

    def __init__(self,no_dice=5):
        '''
        constructor
        '''
        self._no_dice=no_dice
        self._dice=[]
        self._die_status=[]
        for i in range(0,self._no_dice):
            d=Die()
            (self._dice).append(d)
            (self._die_status).append(False)

    def roll(self):
        '''
        a method for rolling all the set of dice
        '''
        count = 0
        for obj in self._dice:
            if self.is_banked(count) == False:
                obj.roll()
            count += 1

    def value(self,index):
        '''
        a method for obtaining a value of a die
        '''
        return self._dice[index].get_value()

    def search(self,value):
        '''
        a method to search for a value among the dice
        '''
        value_to_find = value
        found = False
        for obj in self._dice:
            if obj.get_value() == value_to_find:
                found = True
                break
        return found

    def find_and_bank(self,value):
        '''
        a method to check if a value is availabe and then bank it
        '''
        for i in range(len(self._dice)):
            if (self._dice[i]).get_value() == value and not self.is_banked(i):
                self.bank(i)
                break

    def accumulate(self):
        '''
        a method to find sum of the dice
        '''
        sum_of_dice_values=0
        for obj in self._dice:
            sum_of_dice_values += obj.get_value()
        return sum_of_dice_values

    def bank(self,value):
        '''
        a method to bank a die
        '''
        self._die_status[value] = True

    def is_banked(self,value):
        '''
        a method to check if a die id banked or not
        '''
        return self._die_status[value]

    def release(self,value):
        '''
        a method to unbank a the die
        '''
        self._die_status[value] = False

    def release_all(self):
        '''
        a method to unbank all the dice
        '''
        for i in range(0,self._no_dice):
            self._die_status[i] = False


class ShipOfFoolsGame:
    '''
    Responsible for the game logic and has the ability
    to play a round of the game resulting in a score.
    Also has a property that tells what accumulated
    score results in a winning state.
    '''

    def __init__(self):
        '''
        constructor
        '''
        self._cup=DiceCup()
        self.winning_score=21

    def display_roll(self):
        '''
        a method to print a roll
        '''
        for i in (self._cup)._dice:
            print(i.get_value(),end=" ")
        print("\n")

    def round(self):
        '''
        implementing method round()
        '''
        has_ship = False
        has_captain = False
        has_crew = False
        self._cup.release_all()
        cargo=0
        for round in range(3):
            (self._cup).roll()
            self.display_roll()
            # finding captain,ship,crew and cargo.
            if not has_ship and (self._cup).search(6):
                (self._cup).find_and_bank(6)
                has_ship=True
            if has_ship and not has_captain and (self._cup).search(5):
                (self._cup).find_and_bank(5)
                has_captain=True
            if has_captain and not has_crew and (self._cup).search(4):
                (self._cup).find_and_bank(4)
                has_crew=True
            # when all ship,captain and crew are all found
            if has_ship and has_captain and has_crew and round<2:
                print("options \n1.roll the dice\n2.roll one and bank other\n3.bank all dice")
                choice=int(input("enter the your choice:"))
                if choice==1:
                    continue
                elif choice==2:
                    die_value=int(input("enter the value on the die to bank"))
                    self._cup.find_and_bank(die_value)
                elif choice==3:
                    for i in range((self._cup)._no_dice):
                        (self._cup)._die_status[i]=True
                    cargo = (self._cup).accumulate() - 15
                    break
            # calculating the cargo
            if has_ship and has_captain and has_crew:
                cargo = (self._cup).accumulate() - 15
        return cargo


class Player:
    '''
    Responsible for the score of the individual player.
    Has the ability, given a game logic, play a round of a game.
    The gained score is accumulated in the attribute score.
    '''

    def __init__(self,name):
        '''
        constructor
        '''
        self._name=name
        self._score=0
        self._prev=0

    def set_name(self,name):
        '''
        a method to set the name of the player
        '''
        self._name=name

    def current_score(self):
        '''
        a method to obtain current score
        '''
        return self._prev

    def reset_score(self):
        '''
        a method to reset the score to 0
        '''
        self._prev=0
        self._score=0

    def play_round(self,game):
        '''
        a method to play rounds
        '''
        print("\n",self._name," is throwing")
        self._score=game.round()
        self._prev += self._score


class PlayRoom:
    '''
    Responsible for handling a number of players and a game.
    Every round the room lets each player play, and afterwards
    check if any player have reached the winning score.
    '''

    def __init__(self):
        '''
        constructor
        '''
        self._game=ShipOfFoolsGame()
        self._players=[]

    def set_game(self,game):
        '''
        method to begin a reset game
        '''
        self._game=game

    def add_player(self,player):
        '''
        method to add player's in the game
        '''
        (self._players).append(player)

    def reset_scores(self):
        '''
        method to reset all scores in the game
        '''
        for obj in self._players:
            obj.reset_score()

    def play_round(self):
        '''
        method to play rounds for each player
        '''
        for obj in self._players:
            obj.play_round(self._game)
            if self.game_finished():
                break

    def game_finished(self):
        '''
        method to check if the game is finished or not
        '''
        for obj in self._players:
            if obj.current_score() >= (self._game).winning_score:
                return True
        else:
            return False

    def print_scores(self):
        '''
        method to display the scores of players
        '''
        c=1
        for obj in self._players:
            print(obj._name,":",obj.current_score())
            c+=1

    def print_winner(self):
        '''
        method to display the winner
        '''
        for obj in self._players:
            if obj.current_score() >= (self._game).winning_score:
                print("player ",obj._name,"with",obj.current_score(),"is a winner")


# main function
if __name__ == "__main__":
    print("creating room for players.................")
    room = PlayRoom()
    print("setting the game for players......")
    print("please wait...")
    # setting the game to play
    room.set_game(ShipOfFoolsGame())
    print("____________________________________________________________")
    print("Welcome to Ship Of Fools..")
    print("____________________________________________________________")
    # creating player's objects
    players_no=int(input("please enter the number of player's"))
    for i in range(players_no):
        print("please enter the name of the player ",i+1,":")
        player_name=input()
        room.add_player(Player(player_name))
    room.reset_scores()
    round_count=0
    # playing the game
    while not room.game_finished():
        print("playing round ",round_count)
        print("________________________________________________________")
        room.play_round()
        print("Scores")
        print("---------------------------------")
        room.print_scores()
        print("---------------------------------")
        round_count+=1
    # displaying the final winner
    room.print_winner()