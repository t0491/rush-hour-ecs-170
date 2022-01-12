import sys

'''
////////////////////////////////////////////////////////////////////////////
/// Program is incomplete as I did not understand                        ///
/// the node expansion part of the algorithm for rush hour. I            ///
/// understand how it works in graphs or trees, but for a board with     ///
/// different kinds of vehicles located across, I don't get how to       ///
/// "connect" them as neighbors. How do I determine which order          ///
/// to move which cars in which direction? My program has fully          ///
/// functional independent functions, e.g. I can move the cars           ///
/// around the board, parse the board to see the direction of the cars,  ///
/// and much more. You could modify the program as needed to test if my  ///
/// helper functions do work or not. Essentially, I have all the         ///
/// ingredients to cook a dish, but no instructions on how to use them.  ///                                                                    ///
////////////////////////////////////////////////////////////////////////////
'''

'''
////////////////
/// NODE OBJ ///
////////////////
'''
class Node:
    def __init__(this, h_value, board):
        this.h_value = h_value
        this.board = board

'''
///////////////////////////////
/// VEHICLE OBJ + OPERATORS ///
///////////////////////////////
'''
class Vehicle:
    # Initialize the object with its personalized data.
    def __init__ (this, vehicle_id, cardinality):
        this.vehicle_id = vehicle_id
        this.cardinality = cardinality

# Horizontal Move Left; Only usable for horizontal vehicles.
def move_left(vehicle_id, bd_state):
    # Check if the vehicle is able to move horizontally, if not then don't move.
    if find_cardinality(vehicle_id, bd_state) != "Horizontal":
        return bd_state
    
    index_row = 0
    for row in bd_state:
        # Initialize index to the beginning col/index every time we start a new row.
        index_col = 0
        for i in row:
            if i == vehicle_id:
                # If the vehicle is at the very left end of the board it cannot move.
                if index_col == 0:
                    return bd_state
                elif index_col > 0:
                    # If the tile directly left of the vehicle is not empty, stop.
                    if row[index_col-1] != "-":
                        return bd_state
                    # Else, move left, and empty out current tile's spot.
                    else:
                        bd_state[index_row][index_col-1] = i
                        bd_state[index_row][index_col] = "-"
            index_col += 1
        index_row += 1
    return bd_state
        
# Horizontal Move Right; Only usable for horizontal vehicles.
def move_right(vehicle_id, bd_state):
    # Check if the vehicle is able to move horizontally, if not then don't move.
    if find_cardinality(vehicle_id, bd_state) != "Horizontal":
        return bd_state
    
    index_row = 0
    for row in bd_state:
        index_col = len(bd_state)-1
        # Iterating right to left to make moving to the right easier.
        # Solves case of BBB having to deal with B->BB ? (Can't move since B is in front of itself).
        for i in reversed(row):
            if i == vehicle_id:
                # If the vehicle is at the very right end of the board it cannot move.
                if index_col == len(bd_state)-1:
                    return
                elif index_col < len(bd_state)-1:
                    # If the tile directly right of the vehicle is not empty, stop.
                    if bd_state[index_row][index_col+1] != "-":
                        return
                    # Else, move right, and empty out current tile's spot.
                    else:
                        bd_state[index_row][index_col+1] = i
                        bd_state[index_row][index_col] = "-"
            index_col -= 1
        index_row += 1
    return

# Vertical Move Up; Only usable for vertical vehicles.
def move_up(vehicle_id, bd_state):
    # Check if the vehicle is able to move vertically, if not then don't move.
    if find_cardinality(vehicle_id, bd_state) != "Vertical":
        return bd_state
    
    index_row = 0
    for row in bd_state:
        # Initialize col to 0 for every new row.
        index_col = 0
        for i in row:
            if i == vehicle_id:
                # If the vehicle is at the very top of the board it cannot move.
                if index_row == 0:
                    return
                elif index_row > 0:
                    # If the tile directly above the vehicle is not empty, stop.
                    if bd_state[index_row-1][index_col] != "-":
                        return
                    # Else, move up, and empty out current tile's spot.
                    else:
                        bd_state[index_row-1][index_col] = i
                        bd_state[index_row][index_col] = "-"
            index_col += 1
        index_row += 1
    return

#Vertical Move Down; Only usable for vertical vehicles.
def move_down(vehicle_id, bd_state):
    # Check if the vehicle is able to move vertically, if not then don't move.
    if find_cardinality(vehicle_id, bd_state) != "Vertical":
        return bd_state
    
    index_row = len(bd_state)-1
    for row in reversed(bd_state):
        ## Initialize col to 0 for every new row.
        index_col = 0
        for i in row:
            if i == vehicle_id:
                # If the vehicle is at the very bottom of the board it cannot move.
                if index_row == len(bd_state)-1:
                    return
                elif index_row < len(bd_state)-1:
                    # If the tile directly below the vehicle is not empty, stop.
                    if bd_state[index_row+1][index_col] != "-":
                        return
                    # Else, move down, and empty out current tile's spot.
                    else:
                        bd_state[index_row+1][index_col] = i
                        bd_state[index_row][index_col] = "-"
            index_col += 1
        index_row -= 1
    
    return

'''
///////////////////////////////////
/////// PARSING THE BOARD /////////
///////////////////////////////////
'''

# Converts the rows (strings) in our board to lists so that they can become mutable.
def str_to_list(board):
    new_board = []
    for row in board:
        temp = []
        temp[:0] = row
        new_board.append(temp)
    return new_board

# Converts list back into strings so printing the board looks cleaner/readable.
def list_to_str(board):
    new_board = []
    for row in board:
        temp = ''
        for i in row:
            temp += i
        new_board.append(temp)
    return new_board

'''
///////////////////////////
/// HEURISTIC FUNCTIONS ///
///////////////////////////
'''

# Our default heuristic that we'll be running.
def blocking_heuristic(board):
    # If the last two slots on the 3rd row are X's then we've reached the goal.
    if board[2][len(board)-2] == 'X' and board[2][len(board)-1] == 'X':
        # h(n) returns 0 for the goal state.
        return 0
    else:
        index = 0
        x_location = -1
        for i in board[2]:
            # Determine the location of X car.
            if index < len(board)-1 and i == 'X' and board[2][index+1] != 'X':
                x_location = index
                break
            index += 1
        index = 0
        blocking_vehicles = 0
        for j in board[2]:
            # Check for any vehicle past X and count them as blocking.
            if index > x_location and j != 'X' and j != '-':
                blocking_vehicles += 1
            index += 1

        # h(n) = 1 + # of vehicles blocking X's path.
        return 1+blocking_vehicles
    
    # If no conditions were met, return -1 as an "error" heuristic value.
    return -1

def get_h_value(heuristic, board):
    # Taking the heuristic argument in the rushhour func call, determine which one to use.
    if heuristic == 0:
        h_value = blocking_heuristic(board)
        #print("Blocking h(n): " + str(h_value))
        return h_value
    elif heuristic == 1:
        #h_value = my_heuristic(board)
        #print("My h(n): " + str(h_value))
        return -1
    else:
        print("Invalid heuristic argument.")
        return -1
    
'''
///////////////////////////////
/// MAIN RUSHHOUR PROG/FUNC ///
///////////////////////////////
'''

# Find cardinality of a vehicle to determine how it can move.
def find_cardinality(vehicle_id, board):
    index_row = 0
    for row in board:
        index_col = 0
        for col in row:
            if col == vehicle_id:
                # Check to make sure we're not going out of bounds.
                # Checking neighbors to determine cardinality.
                if index_row < len(board)-1 and index_col < len(board)-1:
                    if board[index_row][index_col+1] == vehicle_id:
                        return "Horizontal"
                    elif board[index_row+1][index_col] == vehicle_id:
                        return "Vertical"
    
            index_col += 1
        index_row += 1

    # Return an error if we somehow can't find a vehicle's cardinality, e.g. 1x1
    return "No specific cardinality, it's 1x1."

# Read through the board and create a Vehicle object for every unique vehicle.
def create_vehicles(vehicle_list, board):
    # Iterates through the board and if a Vehicle isn't already existing, create it.
    for row in board:
        for vehicle in row:
            already_exists = True

            # Check if the vehicle's ID is already within our list.
            # If it isn't then append it to the list.
            for exists in vehicle_list:
                if vehicle != '-' and vehicle != 'X' and vehicle != exists.vehicle_id:
                    already_exists = False
                else:
                    already_exists = True
                
            if not already_exists:
                cardinality = find_cardinality(vehicle, board)
                vehicle_list.append(Vehicle(vehicle, cardinality))
    return vehicle_list

    
def find_solution(heuristic, board, frontier, v_list):
    # Checking if frontier is empty. Terminate w/ failure if it is.
    if frontier == []:
        print("Failure along the way. Obtained an empty frontier somehwere.")
        exit
    # Grab the first node in the frontier to check + expand upon otherwise.
    else:
        chosen_node = frontier.pop(0)

    # Print the next board state here for every step we get to the solution.
    board = list_to_str(board)
    for row in board:
        print(row)
    board = str_to_list(board)
    
    # Check if the chosen node has reached *any* goal state.
    if chosen_node.board[2][len(board)-2] == "X" and chosen_node.board[2][len(board-1)] == "X":
        print("We've found a solution!")
        ## TODO: FIND A WAY TO PRINT ALL THE STEPS TO GET TO THIS SOLUTION ##
        
        ## TEST VARIABLES FOR PRINTING REMOVE LATER ##
        num_moves = 4
        total_states = 2
        ## TEST VARIABLES FOR PRINTING REMOVE LATER ##
        
        print("Total moves: " + str(num_moves))
        print("Total states explored: " + str(total_states))
        return
    
    # Expand upon the chosen node further by attempting to move it and checking h(n)
    else:
       ## TODO: EXPAND THE NODES. ADD TO FRONTIER. CONTINUE SEARCHING. RECURSE.
       #find_solution(heuristic, board, frontier)
       return
    return

'''
Our main function to be called by the user. rushhour(int, list).
Finds a way to move X car towards the exit with the least # of moves.
'''

def rushhour(heuristic, board):
    '''
    Initialize starting variables before beginning recursion. Change init value
    so that it doesn't overwrite the values with 0 again.
    '''
    init = 0
    if init == 0:
        num_moves = 0
        total_states = 0
        init = 1
        
    board = str_to_list(board)
    frontier = [board]

    # Obtain the starting heuristic value of our starting board. Add to frontier.
    h_value = get_h_value(heuristic, board)
    start_node = Node(h_value, board)
    frontier = [start_node]

    # Initialize a list of all vehicles with our targeted X vehicle first.
    vehicle_list = [Vehicle('X', "Horizontal")]

    # Search through the board and add all the vehicles into this.
    vehicle_list = create_vehicles(vehicle_list, board)
         
    # Find the solution. Has its own function so that it can recurse itself.
    find_solution(heuristic, board, frontier, vehicle_list)
    return
