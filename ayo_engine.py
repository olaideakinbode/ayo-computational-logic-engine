import random

#______________________________________________
def create_board():
    """Initializes a 14-slot array representing 12 cups and 2 scoring holes."""
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return board

#______________________________________________
def initialize(play_board):
    """Sets the initial game state with 4 seeds in each of the 12 playing cups."""
    for cup in range(12):
        play_board[cup] = 4
    return play_board

#______________________________________________
def configure(play_board):
    """Allows for custom board state configuration for testing specific scenarios."""
    play_board = [4, 4, 4, 4, 4, 4, 3, 2, 1, 2, 4, 4, 0, 0]
    return play_board

#______________________________________________
def display(play_board):
    """Renders the board state in a top-down view for user interface."""
    # Display the opponent's side (cups 11 to 6) and their score holes (13)
    for cup in range(11, 5, -1):
        print(play_board[cup], end=' ')
    print('  Score Opponent: ' + str(play_board[13]))
    
    # Display the player's side (cups 0 to 5) and their score hole (12)
    for cup in range(6):
        print(play_board[cup], end=' ')
    print('  Score Player: ' + str(play_board[12]))
    print("-" * 20)

#______________________________________________
def det_play_cup(play_board, side):
    """Determines which cup the current player can select based on their side."""
    range_start = 6 * side
    range_end = range_start + 6
    
    # Logic for selecting a valid cup within the player's range
    while True:
        try:
            cup = int(input(f"Player {side}, choose a cup ({range_start + 1}-{range_end}): ")) - 1
            if cup in range(range_start, range_end) and play_board[cup] > 0:
                return cup
            print("Invalid choice. Select a non-empty cup on your side.")
        except ValueError:
            print("Please enter a valid number.")

#______________________________________________
def play_cup(play_board, cup):
    """Implements the sowing algorithm: seeds are distributed one by one in a circular array."""
    hand = play_board[cup]
    play_board[cup] = 0
    current_cup = cup
    
    while hand > 0:
        current_cup += 1
        if current_cup > 11:  # Wraps around the 12-cup board (circular logic)
            current_cup = 0
        play_board[current_cup] += 1
        hand -= 1
    
    return play_board, current_cup
    
#______________________________________________    
def seeds_left(play_board):
    """Calculates total seeds remaining on the board to check for end-game conditions."""
    return sum(play_board[:12])

#______________________________________________
def capture_seeds(play_board, side, end_cup):
    """Handles the capture logic: seeds are collected if the last cup has 2 or 3 seeds on the opponent's side."""
    hand = 0
    # Recursive-style capture: checks if previous cups also meet capture criteria
    while (play_board[end_cup] in [2, 3]) and (the_side(end_cup) != side):
       hand += play_board[end_cup]
       play_board[end_cup] = 0
       end_cup -= 1
       if end_cup < 0: break # Boundary check

    if side == 0:
        play_board[12] += hand # Player 0 score pit
    else:
        play_board[13] += hand # Player 1 score pit
        
    return play_board

#______________________________________________
def opposite_sides(start_cup, end_cup):
    """Validates if the sowing ended on the opponent's side, a requirement for capture."""
    if (start_cup in range(6) and end_cup in range(6, 12)) or \
       (start_cup in range(6, 12) and end_cup in range(6)):
        return 1
    return 0

#______________________________________________
def the_side(cup):
    """Helper function to map a cup index to a specific player's side."""
    return 0 if cup in range(6) else 1
        
#________MAIN EXECUTION___________________________
if __name__ == "__main__":
    ayo = create_board()
    ayo = initialize(ayo)
    display(ayo)

    current_side = 0 # 0 for Player 1, 1 for Player 2
    
    # Game loop continues as long as there are enough seeds for meaningful play
    while seeds_left(ayo) > 5:
        print(f"Current Turn: Player {current_side}")
        chosen_cup = det_play_cup(ayo, current_side)
        ayo, last_cup = play_cup(ayo, chosen_cup)
        
        # Check for capture conditions
        if opposite_sides(chosen_cup, last_cup) and (ayo[last_cup] in [2, 3]):
            ayo = capture_seeds(ayo, current_side, last_cup)
            
        display(ayo)
        current_side = 1 - current_side # Toggle player turn
