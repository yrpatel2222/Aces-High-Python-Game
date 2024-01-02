import cards  # required !!!
import random
    ###########################################################
    #  Computer Project #10
    #  Define a function to create a deck of cards
    #    Define a function to shuffle the deck of cards and define a function to deal cards to players
    #    Define a function to check if the move from the tableau was valid or not. 
    #    loop while column is in range for length of tableau
    #       Define display function that displays the stock, tableau, and foundation. 
    #       inside get_option() do the error checking as required for plays such as choosing an invalid command. 
    #       inside main() function initialize the game and call the respective functions done previously as necessary 
    #       restart the game if the input was "R" by calling the initialize game function again     
    #    display closing message if user input "Q" or display game winning message if user wins game. 
    ###########################################################

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    ''' This function initializes a new game. It creates a new deck of cards, shuffles it, and deals four cards to the tableau, one to each column. It also initializes an empty foundation. Function returns a tuple containing the deck, tableau, and foundation. '''
    deck = cards.Deck()
    deck.shuffle()
    
    # Deal four cards to the tableau, one to each column
    tableau = [[], [], [], []]
    for i in range(4):
        tableau[i].append(deck.deal())
    
    # Initialize an empty foundation
    foundation = []
    
    # Return the starting state of the game
    return deck, tableau, foundation
    
    
def deal_to_tableau( tableau, stock):
    ''' Deals four cards from the stock pile to the tableau. If the stock pile is not empty, the function appends one card to each of the four tableau columns. The function returns nothing. '''
    if len(stock) > 0:  
        tableau[0].append(stock.deal())    
        tableau[1].append(stock.deal())
        tableau[2].append(stock.deal())
        tableau[3].append(stock.deal())

           
def validate_move_to_foundation( tableau, from_col ):
    ''' This function validate_move_to_foundation() checks if a move from tableau to foundation is valid or not. It returns a boolean value indicating whether the move is valid or not. It checks if the column from which the move is being made is not empty. If it is empty, then it returns False. Otherwise, it gets the top card from the column and checks if there is a higher card of the same suit in a different column.'''
    if len(tableau[from_col]) == 0:
        return False

    #move card
    card = tableau[from_col][-1]
    suit = card.suit()
    rank = card.rank()

    if rank == 1:
        rank = 14

    # Check to see if there is a higher card of the same suit in a diff column
    for col in range(len(tableau)):
        if len(tableau[col]) == 0:
            continue

        colcard = tableau[col][-1]
        column_rank = colcard.rank()

        if column_rank == 1:
            column_rank = 14

        if colcard.suit() == suit:
            if column_rank > rank:
                return True

    print(f"\nError, cannot move {card}.")
    return False
    
def move_to_foundation( tableau, foundation, from_col ):
    ''' This function moves a card from a tableau column to the foundation pile if the move is valid. If the move is valid, it removes the card from the tableau column and appends it to the foundation pile. If the move is invalid, nothing happens. The function calls validate_move_to_foundation to check whether the move is valid or not. '''
    if validate_move_to_foundation(tableau, from_col):
        card = tableau[from_col].pop()
        foundation.append(card)


#ask if this will have any errors in main function
def validate_move_within_tableau( tableau, from_col, to_col ):
    ''' This function validates whether it's possible to move a card within a tableau. If the move is valid, it returns True. If the move is invalid, it prints an error message and returns False. Specifically, it checks if the source column is not empty, and the target column is empty. '''
    if tableau[from_col] == [] and len(tableau[to_col]) == 0:
        print("\nError, no card in column: {}".format(from_col+1))
        return False
    if len(tableau[to_col]) == 0:
        return True
    if tableau[to_col]:
        print("\nError, target column is not empty: {}".format(to_col+1))
        return False
    else:
        return False

def move_within_tableau( tableau, from_col, to_col ):
    ''' This function simply moves a card from one column to another column within the tableau if the move is valid. If the move is valid, it removes the card from the tableau column and appends it to the foundation pile. If the move is invalid, nothing happens. The function calls validate_move_to_foundation.'''
    if validate_move_within_tableau(tableau, from_col, to_col):
        card = tableau[from_col].pop()
        tableau[to_col].append(card)


def check_for_win( tableau, stock ):
    ''' Looks for if the game has been won by checking if all cards have been moved to the foundation piles. Returns True if game has been won, False otherwise. '''
    counter = 0
    empty_list = []
    if len(stock) != 0:
        return False
    for col in tableau:
        for card in col:
            empty_list.append(card)
    if len(empty_list) == 4:
        for card in empty_list:
            if card.rank() == 1:
                counter += 1 

    if counter == 4:
        return True
    else:
        return False
    pass
           
def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    ''' Returns a list containing the selected option and its parameters, if any. The valid columns for the 'F' and 'T' commands are '1', '2', '3', and '4'. If user enters an invalid option or an option with invalid parameters, it will print an error message and return an empty list.'''
    valid_commands = ['D', 'F', 'T', 'R', 'H', 'Q']
    valid_cols = ['1', '2', '3', '4']
    option_input = input("\nInput an option (DFTRHQ): ")
    #print(option)
    option = option_input.strip().upper().split()
    #print(option)
    if option[0] not in valid_commands:
        print("\nError in option: "+option_input)
        return []
    if option[0] == 'D' and len(option) == 1:
        return ['D']
    elif option[0] == 'R' and len(option) == 1:
        return ['R']
    elif option[0] == 'H' and len(option) == 1:
        return ['H']
    elif option[0] == 'Q' and len(option) == 1:
        return ['Q']
    elif option[0] == 'F' and len(option) == 2 and option[1] in valid_cols: #checks if the length of the option list is 2 and if the second value is a valid column value.
        return ['F', int(option[1])-1]
    elif option[0] == 'T' and len(option) == 3 and option[1] in valid_cols and option[2] in valid_cols: #checks if the length of the option list is 3 and if the second and third values are valid column values
        return ['T', int(option[1])-1, int(option[2])-1]
    else:
        print("\nError in option: "+option_input)
        return []

        
def main():
    stock, tableau, foundation = init_game() #initializing the game
    print(RULES)
    print(MENU)
    display( stock, tableau, foundation ) #display the current state of the game
    while True: #loop until the player quits or has won
        option = get_option() #get player's option
        if not option: #if option is invalid continue the loop
            continue
        #run the respective command based on the option 
        elif option[0] == 'D':
            deal_to_tableau(tableau, stock)
        elif option[0] == 'Q':
            print("\nYou have chosen to quit.")
            break
        elif option[0] == "H":
            print(MENU)
        elif option[0] == "F":
            move_to_foundation(tableau, foundation, option[1])
        elif option[0] == 'T':
            move_within_tableau(tableau, option[1], option[2])
        
        
        elif option[0] == 'R':    #restarts the game
            print("\n=========== Restarting: new game ============")
            stock, tableau, foundation = init_game()
            print(RULES)
            print(MENU)
        
        if check_for_win(tableau, stock): #check if you win game
            print("\nYou won!")
            break
        display( stock, tableau, foundation ) #display current state of the game 

if __name__ == '__main__':
    main()
