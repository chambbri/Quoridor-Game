# Name: Brian Chamberlain
# Date: 8/9/2021
# Description: Code for the Quoridor game. See docstrings below for code description

from pprint import pprint


class QuoridorGame:
    """Class QuoridorGame represents a game with two players on a 9x9 board where the goal of the game is to reach
    the opponents baseline on the opposite side of the board. A player can move their pawn one space to adjacent
    spaces or place a fence to block the path of their opponent. A player can only move diagonally if their opponent
    is in a space adjacent to them. A player can hop over the opposing player to move two spaces if the opponent
    is in the square adjacent to them. The class handles all aspects of the game, including creating the board,
    updating the board, creating the two players pawns, moving the pawns in a valid manner, and placing fences"""

    def __init__(self):
        """The init method initializes the board with the pawns placed in their starting positions along with other
        private data members to initialize whose turn it is, the starting amount of fences each player has and
        a dictionary that contains vertical and horizontal fence locations that have been placed"""

        # the game board will be stored in a list containing 9 lists with 9 elements. Player 1 starts at (4,0) and
        # player 2 starts at (4,8)
        self._game_board = [
            [' ', ' ', ' ', ' ', 'P1', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'P2', ' ', ' ', ' ', ' ']
        ]
        self._player_turn = 1  # player 1 starts the game
        self._p1_fences = 10  # each player starts with 10 fences
        self._p2_fences = 10
        # the fence locations dictionary keeps track of vertical and horizontal fences placed
        self._fence_locations = {'v': [], 'h': []}

    def print_board(self):
        """Prints the board with the location of each pawn"""
        pprint(self._game_board)
        print('\n')

    def get_player_position(self, player):
        """Returns the current position on the board of the requested player.
        The player parameter will be which player the position is requested of
        The player position will be returned in a tuple with the x and y position"""
        row_num = 0
        element_num = 0

        # loop through all rows (lists) of the game board
        for row in self._game_board:

            # loop through each element in each row (list)
            for element in row:
                if player == 1:
                    if element == 'P1':
                        return element_num, row_num
                elif player == 2:
                    if element == 'P2':
                        return element_num, row_num
                element_num += 1
            row_num += 1
            element_num = 0

    def set_player_position(self, player, current_pos, new_pos):
        """Method set_player_position will update the board of the player when a valid move has been made.
        player parameter is the player whose position will be updated.
        current_pos is a tuple of the current (x,y) position of the player so it can be set to a blank space
        new_pos is a tuple of the new (x,y) position of the player"""

        if player == 1:
            self._game_board[new_pos[1]][new_pos[0]] = 'P1'
            self._game_board[current_pos[1]][current_pos[0]] = ' '
        elif player == 2:
            self._game_board[new_pos[1]][new_pos[0]] = 'P2'
            self._game_board[current_pos[1]][current_pos[0]] = ' '

    def get_fence_locations(self):
        """Returns the dictionary of vertically and horizontally placed fences"""
        return self._fence_locations

    def move_pawn(self, player, move_coordinates):
        """Moves the pawn of the player whose turn it is. Calls the valid_pawn_move method to determine if the
        move that the player is proposing is valid
        The player parameter is the player whose pawn is being attempted to be moved
        The move_coordinates parameter is a tuple of the position (x,y) the player would like to move to
        Returns True if the move was successful and False if it was not"""

        player_loc = self.get_player_position(player)
        # obtain the location of the opponent to pass to valid_pawn_move method
        if player == 1:
            opp_player_loc = self.get_player_position(2)
        else:
            opp_player_loc = self.get_player_position(1)
        # call valid_pawn_move method to determine if the move is valid and within the rules
        valid_move = self.valid_pawn_move(player, move_coordinates, player_loc, opp_player_loc)
        if not valid_move:
            return False
        elif self.is_winner(1) or self.is_winner(2):
            return False
        # if the move is valid, set the new player position and change the turn
        else:
            self.set_player_position(player, player_loc, move_coordinates)
            if player == 1:
                self._player_turn = 2
            else:
                self._player_turn = 1
            # return true if there is a winner or the move was valid
            if self.is_winner(player):
                return True
            return True

    def valid_pawn_move(self, player, move_coordinates, player_loc, opp_player_loc):
        """Determines if the move proposed by the player whose turn it is is valid and within the rules of the game
        player is the parameter who is making the move
        move_coordinates is a tuple of the position (x,y) the player is moving to
        player_loc is a tuple of the players current position (x,y)
        opp_player_loc is a tuple of the opponents current position (x,y)
        Returns True if the move is valid and false if it was not"""

        # return False if the move is outside of the board boundaries
        if 0 > move_coordinates[0] > 8 or 0 > move_coordinates[1] > 8:
            return False
        elif player != self._player_turn:  # return False if it is not the players turn making the move
            return False
        # return False if the player is moving to a location occupied by the opponent
        elif move_coordinates == opp_player_loc:
            return False
        x_move = move_coordinates[0] - player_loc[0]
        y_move = move_coordinates[1] - player_loc[1]
        if abs(x_move) > 2 or abs(y_move) > 2:  # a move cannot be greater than 2 in any direction
            return False
        elif not self.fence_block(x_move, y_move, move_coordinates, player_loc, opp_player_loc):  # determine if the move is blocked by a fence
            return False
        elif x_move != 0 and y_move != 0:  # determine if a diagonal move is valid
            return self.diagonal_move(x_move, y_move, player_loc, opp_player_loc)
        # determine if the player can hop the opponent
        elif abs(x_move) == 2 and y_move == 0 or x_move == 0 and abs(y_move) == 2:
            return self.hop_over(x_move, y_move, player_loc, opp_player_loc)
        # if all conditions passed, the move is a single space move that is valid
        else:
            return True

    def hop_over(self, x_move, y_move, player_loc, opp_player_loc):
        """Method hop_over will determine if a player attempting to hop over the opponent (i.e. move two spaces)
        is a valid move. This is a helper method to valid_pawn_move
        x_move will determine how far the proposed move is in the x-direction
        y_move will determine how far the proposed move is in the y-direction
        player_loc is a tuple of the players current position (x,y)
        opp_player_loc is a tuple of the opponents current position (x,y)
        Returns True if the move is valid and false if it was not"""
        # check for a horizontal jump in both directions
        if abs(x_move) != 0:
            if x_move < 0:
                # verify that the player is hopping over the opponent
                if opp_player_loc != (player_loc[0] - 1, player_loc[1]):
                    return False
                else:
                    return True
            elif x_move > 0:
                if opp_player_loc != (player_loc[0] + 1, player_loc[1]):
                    return False
                else:
                    return True
        else:
            # perform the same checks for vertical jumps
            if y_move < 0:
                if opp_player_loc != (player_loc[0], player_loc[1] - 1):
                    return False
                else:
                    return True
            elif y_move > 0:
                if opp_player_loc != (player_loc[0], player_loc[1] + 1):
                    return False
                else:
                    return True

    def diagonal_move(self, x_move, y_move, p_loc, opp_player_loc):
        """Method diagonal_move will determine if a player trying to move diagonally is a valid move. This is
        a helper method to valid_pawn_move.
        x_move will determine how far the proposed move is in the x-direction
        y_move will determine how far the proposed move is in the y-direction
        p_loc is a tuple of the players current position (x,y)
        opp_player_loc is a tuple of the opponents current position (x,y)
        Returns True if the move is valid and false if it was not"""

        if y_move > 0:
            # verify that there is not a fence between the players
            if opp_player_loc in self._fence_locations['h']:
                return False
            # verify that a fence is behind the opponent. Per ed threads, diagonal moves only can be done vertically
            elif (opp_player_loc[0], opp_player_loc[1] + 1) not in self._fence_locations['h']:
                return False
        elif y_move < 0:
            # verify there is not a fence between the players
            if p_loc in self._fence_locations['h']:
                return False
            # verify that a fence is behind the opponent. Per ed threads, diagonal moves only can be done vertically
            elif opp_player_loc not in self._fence_locations['h']:
                return False
        # the code will check diagonal moves of all direction (4 possible) and verify that the opponent is in front of
        # the player attempting the move
        if x_move == 1 and y_move == 1:
            if opp_player_loc == (p_loc[0], p_loc[1] + 1):
                return True
            else:
                return False
        elif x_move == 1 and y_move == -1:
            if opp_player_loc == (p_loc[0], p_loc[1] - 1):
                return True
            else:
                return False
        elif x_move == -1 and y_move == 1:
            if opp_player_loc == (p_loc[0], p_loc[1] + 1):
                return True
            else:
                return False
        elif x_move == -1 and y_move == -1:
            if opp_player_loc == (p_loc[0], p_loc[1] - 1):
                return True
            else:
                return False
        # the else will handle cases when a diagonal move of more than 2 spaces is attempted in any direction
        else:
            return False

    def fence_block(self, x_move, y_move, move_coordinates, p_loc, opp_player_loc):
        """Method fence_block will determine if the move a player is attempting to make is blocked by a fence,
        This is a helper method to valid_pawn_move.
        x_move will determine how far the proposed move is in the x-direction
        y_move will determine how far the proposed move is in the y-direction
        move_coordinates is a tuple of the position (x,y) the player is moving to
        p_loc is a tuple of the players current position (x,y)
        opp_player_loc is a tuple of the opponents current position (x,y)
        Returns True if the move is valid and False if it was not"""

        # handle if the move is in the x-direction and not the y
        if x_move != 0 and y_move == 0:
            if x_move > 0:
                # determine if there is a vertical fence at the location
                if move_coordinates in self._fence_locations['v']:
                    return False
                # when jumping an opponent, determine if there is a fence between the opponents
                elif x_move > 1 and opp_player_loc in self._fence_locations['v']:
                    return False
                else:
                    return True
            else:
                # if the move is in the negative x-direction 1 needs to be added to the x-coordinate of the move
                # to determine if a fence is at that location
                if p_loc in self._fence_locations['v']:
                    return False
                # this will cover if a player is attempting to hop the opponent, but there is a fence
                # between the players
                elif abs(x_move) > 1 and opp_player_loc in self._fence_locations['v']:
                    return False
                else:
                    return True
        # perform the same checks for the y-direction, except the horizontal fence locations will be checked
        elif x_move == 0 and y_move != 0:
            if y_move > 0:
                if move_coordinates in self._fence_locations['h']:
                    return False
                elif y_move > 1 and opp_player_loc in self._fence_locations['h']:
                    return False
                else:
                    return True
            else:
                if p_loc in self._fence_locations['h']:
                    return False
                elif abs(y_move) > 1 and opp_player_loc in self._fence_locations['h']:
                    return False
                else:
                    return True
        else:
            return True

    def place_fence(self, player, fence_dir, fence_loc):
        """place_fence method will place a fence at the desired location of the player whose turn it is
        player represents the player attempting to place the fence
        fence_dir is a string containing 'v' or 'h' indicating a vertical or horizontal fence
        fence_loc is a tuple of the position (x,y) a player desires to place the fence at
        Will return True if the fence placement was valid and False if not"""

        # call the helper function to determine if the placement was valid
        valid_placement = self.valid_place_fence(player, fence_dir, fence_loc)
        if not valid_placement:
            return False
        elif self.is_winner(1) or self.is_winner(2):
            return False
        # if it was valid, add the fence to the fence locations dictionary and returns True
        else:
            self._fence_locations[fence_dir].append(fence_loc)
            if player == 1:
                self._p1_fences -= 1  # decrease the amount of fences the player has by 1
                self._player_turn = 2  # change the turn to the other player
            else:
                self._p2_fences -= 1
                self._player_turn = 1
            return True

    def valid_place_fence(self, player, fence_dir, fence_loc):
        """Method valid_place_fence will determine if the location the player is proposing to place a fence is
        valid. This is a helper function to the place_fence method.
        player represents the player attempting to place the fence
        fence_dir is a string containing 'v' or 'h' indicating a vertical or horizontal fence
        fence_loc is a tuple of the position (x,y) a player desires to place the fence at
        Will return True if the fence placement was valid and False if not"""

        if player != self._player_turn:
            return False
        # if the fence already exists in the dictionary, return False
        elif fence_dir in self._fence_locations and fence_loc in self._fence_locations[fence_dir]:
            return False
        # if the fence is outside of the board, return false
        elif 0 > fence_loc[0] > 8 or 0 > fence_loc[1] > 8:
            return False
        # a fence cannot be placed on the boarder
        elif fence_dir == 'v' and fence_loc[0] == 0 or fence_dir == 'h' and fence_loc[1] == 0:
            return False
        # if the player does not have a fence left to place return False
        elif self._player_turn == 1 and self._p1_fences == 0 or self._player_turn == 2 and self._p2_fences == 0:
            return False
        else:
            return True

    def is_winner(self, player):
        """Method is_winner will determine if a player has won the game. A winner occurs when the player reaches
        the opposing players baseline
        player is the player we are checking to see who won
        Returns true if player has won or False if not"""

        player_pos = self.get_player_position(player)
        # player 1 wins when their y-position is at 8
        if player == 1 and player_pos[1] == 8:
            print("player 1")
            return True
        # player 2 wins when their y-position is at 0
        elif player == 2 and player_pos[1] == 0:
            return True
        else:
            return False

