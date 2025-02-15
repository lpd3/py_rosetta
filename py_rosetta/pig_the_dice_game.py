#! /usr/bin/python

# pig_the_dice_game.py

'''Pig the Dice Game

The game of Pig is a multiplayer game played with a single six-sided die.
The object of the game is to reach 100 points or more. Play is taken in
turns. On each person's turn that person has the option of either:

    1. Rolling the dice: where a roll of two to six is added to their score
       for that turn and the player's turn continues as the player is given
       the same choice again; or a roll of 1 loses the player's total points
       for that turn and their turn finishes with play passing to the next
       player.
   
    2. Holding: the player's score for that round is added to their total and
       becomes safe from the effects of throwing a 1 (one). The player's turn
       finishes with play passing to the next player.

Task

Create a program to score for, and simulate dice throws for, a two-person game.
'''
from random import randrange
from time import sleep


def display_opening_banner():
    '''Displays the opening banner.
       Takes no args. Returns None.'''
    print("{:^36}".format("***PIG***"))
    print()
    print()
    sleep(2)

def pig_roll():
    '''Simulates a roll of a single 6-sided die.
       Takes no args. Returns a random int from 1 to 6 inclusive'''
    return randrange(1, 7)

    
def query_opponent():
    '''Asks the player if he/she would rather play the computer or a human player.
       Takes no args. Returns True if the user elects to play against the 
       computer and False if not. Repeatedly queries until a sensical response is entered.'''
    while True:
        print("Play against the computer? (y/n)")
        response = input()[0]
        match response:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print("\nPlease enter y or n\n")


def human_round(player, score):
    '''Runs a turn of the game in which the player is a human. 
    Takes two args:
        `player` (string)
        `score` (number).
     Returns a number.

     Announces a new turn.
     Simulates a roll of the die. If the result is 1, 
     announces this fact and the fact that the player will
     receive no new points from this round. Returns 0.
     Otherwise, the result of the roll is considered possible 
     additional points. Announces the roll and the updated additional points.
     If additional points + score >= 100, announces that the turn is finished, 
     and returns the additional points. Otherwise, queries the user to see if he/she
     wants to continue the turn. If so, the process is repeated. Otherwise,
     announces that the turn is finished and returns the additional points.
     The query is repeated until the user enters a sensical response.
     '''
    new_points = 0
    print(f"\n{player} turn.\n")
    input("Press ENTER to continue")
    while True:
        print("Rolling...")
        sleep(1)
        roll = pig_roll()
        if roll == 1:
            print(f"Player rolled 1. Turn finished. Score: {score}.")
            sleep(1)
            return 0
        new_points += roll
        print(f"Player rolled {roll}. {new_points} new points so far.")
        if score + new_points >= 100:
            print(f"Turn finished. Score: {score + new_points}.")
            sleep(1)
            return new_points
        print(f"If the round stops now, {player} score will be {score + new_points}.")
        while True:
            print("Roll again? (y/n)")
            response = input()[0]
            match response:
                case 'y':
                    break
                case 'n':
                    print("Turn finished.")
                    return new_points
                case _:
                    print("Please enter y or n")

# To determine whether or not the computer will
# continue its turn, a random integer between 1 and
# CONTINUE_THRESHOLD (inclusive) is generated. If the result is
# CONTINUE_THRESHOLD, the turn will end. Otherwise, the turn
# will continue.

CONTINUE_THRESHOLD = 4


def random_continue_round():
    '''Randomly determines whether or not the computer
       should continue its turn. Takes no args. Returns a Boolean.'''
    continue_score = randrange(1, CONTINUE_THRESHOLD+1)
    return continue_score < CONTINUE_THRESHOLD
                    

def computer_round(score):
    '''Simulates a turn of the game in which the player is the computer.
       Takes one arg: `score` (number).
       Returns a number.
       Operation is similar to that of `human_round`, except
       the decision to continue the turn is made randomly.'''
    new_points = 0
    print("My turn.\n")
    while True:
        print("Rolling...")
        sleep(1)
        roll = pig_roll()
        if roll == 1:
            print(f"I rolled 1. Turn finished. Score: {score}.")
            sleep(1)
            return 0
        new_points += roll
        print(f"I rolled {roll}. {new_points} new points so far.")
        if score + new_points >= 100:
            print(f"Turn finished. Score: {score + new_points}")
            sleep(1)
            return new_points
        print(f"If the round stops now, my score will be {score + new_points}.")
        will_keep_going = random_continue_round()
        if will_keep_going:
            print("I will roll again")
        else:
            print("I will stop here.")
            print("Turn finished")
            sleep(1)
            return new_points
                    

def play_computer_game():
    '''Runs a complete game in which one player is the computer.
       Takes no args. Returns a 3-tuple (string, number, number).
       Lets the human go first. Alternately runs `human_round` and
       `computer_round` until one of the scores >= 100. At that time,
       returns a tuple of three values: winner (string), winner_score
       (number) and loser_score (number)'''
    human_score = 0
    computer_score = 0
    while True:
        human_score += human_round("Your", human_score)
        if human_score >= 100:
            return "You", human_score, computer_score
        computer_score += computer_round(computer_score)
        if computer_score >= 100:
            return "I", computer_score, human_score


def play_human_game():
    '''Simulates a complete game in which both players are humans.
       Takes no args. Returns a 3-tuple (string, number, number).
       Repeatedly calls `human_round` alternately for player 1 and 
       player 2. When one of the scores >= 100, returns a tuple of 
       winner (string), winner_score (number) and loser_score (number).'''
    player_1_score = 0
    player_2_score = 0
    while True:
        player_1_score += human_round("Player 1's", player_1_score)
        if player_1_score >= 100:
            return "Player 1", player_1_score, player_2_score
        player_2_score += human_round("Player 2's", player_2_score)
        if player_2_score >= 100:
            return "Player 2", player_2_score, player_1_score


def display_results(winner, winner_score, loser_score):
    '''Displays the results of a single game.
    Takes 3 args:
        `winner` (string)
        `winner_score` (number)
        `loser_score` (number)
    Returns None.'''
    print(f"\n\n{winner} won!")
    print(f"{winner_score} to {loser_score}")


def query_new_game():
    '''Queries the user to see if he/she wants to play
     another game.
     Takes no args.
     Returns a Boolean.
     Repeatedly queries until a sensical answer is supplied.'''
    while True:
        print("Play again? (y/n)")
        response = input()[0]
        match response:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print("Please enter y or n")


def display_closing_banner():
    '''Displays the closing banner.
       Takes no args.
       Returns None.'''
    print("{:^36}".format("BYE!!!"))
    
    
def pig_main():
    '''Game of PIG. 
    Takes no args.
    Returns None.
    Displays an opening banner. 
    Enters a continuous loop.
    Queries the user whether there will be a computer or 
    human opponent. Runs the chosen game. Reports the results.
    Queries the user if there will be another game. If not, 
    closing banner is displayed and program terminates.
    '''
    keep_going = True
    winner = None
    winner_score = None
    loser_score = None

    display_opening_banner()
    
    while keep_going:
        is_computer_opponent = query_opponent()

        if is_computer_opponent:
            winner, winner_score, loser_score = play_computer_game()
        else:
            winner, winner_score, loser_score = play_human_game()

        display_results(winner, winner_score, loser_score)
        sleep(2)
        keep_going = query_new_game()

    display_closing_banner()
    

if __name__ == "__main__":
    pig_main()
