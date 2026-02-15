# Author: Timothy Birmingham
# GitHub username: TimBirmingham
# Date: 5/21/2023
# Description:
#

class Player:
    """
    Represents a player class
    """
    def __init__(self, name, color):
        """
        Initializes a player class with a given name and piece color
        """
        self._player_name = name
        self._piece_color = color

    def get_players_name(self):
        """
        Returns the player's name
        """
        return self._player_name

    def get_piece_color(self):
        """
        Returns the player's piece color
        """
        return self._piece_color


class Othello:
    """
    Represents the Othello class
    """
    def __init__(self):
        self._players = []
        self._board = [["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", "O", "X", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", "X", "O", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                       ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]]

    def print_board(self):
        """
        Prints the current 2D board
        """
        for row in range(0, 10):
            for column in range(0, 10):
                print(self._board[row][column], end=" ")
            print()

    def create_player(self, player_name, color):
        """
        Creates a player for the Othello game with a given name and color
        """
        if len(self._players) == 0:
            if color.lower() == "black" or color.lower() == "white":
                self._players.append(Player(player_name, color.lower()))
            else:
                print("Please select a black or white piece color")
        elif len(self._players) == 1:
            if color.lower() == "black" or color.lower() == "white":
                selected_color = self._players[0].get_piece_color()
                if selected_color != color:
                    self._players.append(Player(player_name, color.lower()))
                else:
                    print("This color has already been selected")
            else:
                print("Please select a black or white piece color")
        else:
            print("There can only be two players")

    def return_winner(self):
        """
        Reads the board and prints the winning player's name and piece color.
        If the game ends in a tie, the method prints "It's a tie".
        """
        white_points = 0
        black_points = 0
        if self._players[0].get_piece_color() == "black":
            black_piece_player = 0          # Determine which player is the black pieces
            white_piece_player = 1
        else:
            black_piece_player = 1          # Or white pieces
            white_piece_player = 0
        for row in range(0, 10):               # Iterate through the board and count the pieces
            for column in range(0, 10):
                if self._board[row][column] == "O":
                    white_points += 1
                if self._board[row][column] == "X":
                    black_points += 1
        if white_points > black_points:         # Determine winner or tie
            return "Winner is white player: " + str(self._players[white_piece_player].get_players_name())
        elif white_points < black_points:
            return "Winner is black player: " + str(self._players[black_piece_player].get_players_name())
        else:
            return "It's a tie"

    def check_board_segment(self, board_segment, piece, opponents_piece):
        """
        Checks a given segment of the board to see if pieces can be taken. It then returns a list of the
        indexes that can be taken by the given piece.
        """
        capture_list = []
        index = 0
        while board_segment[index] == opponents_piece:     # mark the indexes where pieces are taken
            if board_segment[index + 1] == piece:
                capture_list.append(index)
            elif board_segment[index + 1] == opponents_piece:
                capture_list.append(index)
            else:                                   # If the end of the board is reached and no pieces
                capture_list = []               # are taken then reset the taken list
            index += 1
        return capture_list

    def check_vertical_up(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks up, vertically, for pieces the player would take from
        a given position. The method returns a copy of that segment of the board. It also returns a list of
        the indexes, in that segment, that the player would take with the proposed move.
        """
        list_up = []
        for row in range(0, position_row):          # Create a list looking up from given position
            list_up.append(self._board[row][position_column])
        list_up = list_up[::-1]                     # Reverse the list to iterate through
        check_capture = self.check_board_segment(list_up, piece, opponents_piece)
        return [check_capture, list_up]

    def capture_pieces_up(self, vertical_up_capture, position_row, position_column, piece):
        """
        This method captures pieces up, vertically. It is passed a segment of the board, the indexes that will be
        captured on that segment and the piece doing the capturing. It then updates the board accordingly.
        """
        captured_list_up = vertical_up_capture[0]
        list_up = vertical_up_capture[1]
        for row in captured_list_up:  # Update the up list with taken pieces
            list_up[row] = piece
        list_up = list_up[::-1]  # Reverse the list back
        for row in range(0, position_row):  # Iterate the pieces back onto the board
            self._board[row][position_column] = list_up[row]

    def check_vertical_down(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks down, vertically, for pieces the player would take from
        a given position. The method returns a copy of that segment of the board. It also returns a list of
        the indexes, in that segment, that the player would take with the proposed move.
        """
        list_down = []
        for row in range(position_row + 1, 10):         # Create a list looking down from given position
            list_down.append(self._board[row][position_column])
        check_capture = self.check_board_segment(list_down, piece, opponents_piece)
        return [check_capture, list_down]

    def capture_pieces_down(self, vertical_down_capture, position_row, position_column, piece):
        """
        This method captures pieces down, vertically. It is passed a segment of the board, the indexes that will be
        captured on that segment and the piece doing the capturing. It then updates the board accordingly.
        """
        captured_list_down = vertical_down_capture[0]
        list_down = vertical_down_capture[1]
        for row in captured_list_down:  # Update the down list with taken pieces
            list_down[row] = piece
        for row in range(position_row + 1, 9):  # Iterate the pieces back onto the board
            self._board[row][position_column] = list_down[row - position_row - 1]

    def check_horizontal_right(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks right, horizontally, for pieces the player would take from
        a given position. The method returns a copy of that segment of the board. It also returns a list of
        the indexes, in that segment, that the player would take with the proposed move.
        """
        list_right = []
        for column in range(position_column + 1, 10):  # Create a list looking left from given position
            list_right.append(self._board[position_row][column])
        check_capture = self.check_board_segment(list_right, piece, opponents_piece)
        return [check_capture, list_right]

    def capture_pieces_horizontal_right(self, horizontal_right_capture, position_row, position_column, piece):
        """
        This method captures pieces right, horizontally. It is passed a segment of the board, the indexes that will be
        captured on that segment and the piece doing the capturing. It then updates the board accordingly.
        """
        captured_list_right = horizontal_right_capture[0]
        list_right = horizontal_right_capture[1]
        for column in captured_list_right:  # Update the right list with taken pieces
            list_right[column] = piece
        for column in range(position_column + 1, 9):  # Iterate the pieces back onto the board
            self._board[position_row][column] = list_right[column - position_column - 1]

    def check_horizontal_left(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks left, horizontally, for pieces the player would take from
        a given position. The method returns a copy of that segment of the board. It also returns a list of
        the indexes, in that segment, that the player would take with the proposed move.
        """
        list_left = []
        for column in range(0, position_column):  # Create a list looking up from given position
            list_left.append(self._board[position_row][column])
        list_left = list_left[::-1]  # Reverse the list to iterate through
        check_capture = self.check_board_segment(list_left, piece, opponents_piece)
        return [check_capture, list_left]

    def capture_pieces_horizontal_left(self, horizontal_left_capture, position_row, position_column, piece):
        """
        This method captures pieces left, horizontally. It is passed a segment of the board, the indexes that will be
        captured on that segment and the piece doing the capturing. It then updates the board accordingly.
        """
        captured_list_left = horizontal_left_capture[0]
        list_left = horizontal_left_capture[1]
        for column in captured_list_left:  # Update the left list with taken pieces
            list_left[column] = piece
        list_left = list_left[::-1]  # Reverse the list back
        for column in range(0, position_column):  # Iterate the pieces back onto the board
            self._board[position_row][column] = list_left[column]

    def check_down_right(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks down and right, diagonally, for pieces the player would
        take from a given position. The method returns a copy of that segment of the board. It also returns
        a list of the indexes, in that segment, that the player would take with the proposed move.
        """
        list_down_right = []
        column = position_column
        row = position_row
        while column < 9 and row < 9:  # Create a list looking down right from given position
            column += 1
            row += 1
            list_down_right.append(self._board[row][column])
        check_capture = self.check_board_segment(list_down_right, piece, opponents_piece)
        return [check_capture, list_down_right]

    def capture_pieces_down_right(self, down_right_capture, position_row, position_column, piece):
        """
        This method captures pieces down and left, diagonally. It is passed a segment of the board, the indexes
        that will be captured on that segment and the piece doing the capturing.
        It then updates the board accordingly.
        """
        captured_list_down_right = down_right_capture[0]
        list_down_right = down_right_capture[1]
        for position in captured_list_down_right:  # Update the down right list with taken pieces
            list_down_right[position] = piece
        index = 0
        column = position_column
        row = position_row
        while column < 9 and row < 9:  # Iterate the pieces back onto the board
            column += 1
            row += 1
            self._board[row][column] = list_down_right[index]
            index += 1

    def check_up_right(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks up and right, diagonally, for pieces the player would
        take from a given position. The method returns a copy of that segment of the board. It also returns
        a list of the indexes, in that segment, that the player would take with the proposed move.
        """
        list_up_right = []
        column = position_column
        row = position_row
        while column < 9 and row > 0:  # Create a list looking up right from given position
            column += 1
            row -= 1
            list_up_right.append(self._board[row][column])
        check_capture = self.check_board_segment(list_up_right, piece, opponents_piece)
        return [check_capture, list_up_right]

    def capture_pieces_up_right(self, up_right_capture, position_row, position_column, piece):
        """
        This method captures pieces up and right, diagonally. It is passed a segment of the board, the indexes
        that will be captured on that segment and the piece doing the capturing.
        It then updates the board accordingly.
        """
        captured_list_up_right = up_right_capture[0]
        list_up_right = up_right_capture[1]
        for position in captured_list_up_right:  # Update the up right list with taken pieces
            list_up_right[position] = piece
        index = 0
        column = position_column
        row = position_row
        while column < 9 and row > 0:  # Iterate the pieces back onto the board
            column += 1
            row -= 1
            self._board[row][column] = list_up_right[index]
            index += 1

    def check_down_left(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks down and left, diagonally, for pieces the player would
        take from a given position. The method returns a copy of that segment of the board. It also returns
        a list of the indexes, in that segment, that the player would take with the proposed move.
        """
        list_down_left = []
        column = position_column
        row = position_row
        while column > 0 and row < 9:  # Create a list looking down left from given position
            column -= 1
            row += 1
            list_down_left.append(self._board[row][column])
        check_capture = self.check_board_segment(list_down_left, piece, opponents_piece)
        return [check_capture, list_down_left]

    def capture_pieces_down_left(self, down_left_capture, position_row, position_column, piece):
        """
        This method captures pieces down and left, diagonally. It is passed a segment of the board, the indexes
        that will be captured on that segment and the piece doing the capturing.
        It then updates the board accordingly.
        """
        captured_list_down_left = down_left_capture[0]
        list_down_left = down_left_capture[1]
        for position in captured_list_down_left:  # Update the down left list with taken pieces
            list_down_left[position] = piece
        index = 0
        column = position_column
        row = position_row
        while column > 0 and row < 9:  # Iterate the pieces back onto the board
            column -= 1
            row += 1
            self._board[row][column] = list_down_left[index]
            index += 1

    def check_up_left(self, position_row, position_column, piece, opponents_piece):
        """
        Given a player's piece color, the methods checks up and left, diagonally, for pieces the player would
        take from a given position. The method returns a copy of that segment of the board. It also returns
        a list of the indexes, in that segment, that the player would take with the proposed move.
        """
        list_up_left = []
        column = position_column
        row = position_row
        while column > 0 and row > 0:  # Create a list looking down left from given position
            column -= 1
            row -= 1
            list_up_left.append(self._board[row][column])
        check_capture = self.check_board_segment(list_up_left, piece, opponents_piece)
        return [check_capture, list_up_left]

    def capture_pieces_up_left(self, up_left_capture, position_row, position_column, piece):
        """
        This method captures pieces up and left, diagonally. It is passed a segment of the board, the indexes
        that will be captured on that segment and the piece doing the capturing.
        It then updates the board accordingly.
        """
        captured_list_down_left = up_left_capture[0]
        list_up_left = up_left_capture[1]
        for position in captured_list_down_left:  # Update the down left list with taken pieces
            list_up_left[position] = piece
        index = 0
        column = position_column
        row = position_row
        while column > 0 and row > 0:  # Iterate the pieces back onto the board
            column -= 1
            row -= 1
            self._board[row][column] = list_up_left[index]
            index += 1

    def return_available_positions(self, color):
        """
        Returns a list of the valid moves for the given color
        """
        color = color.lower()
        moves_list = []
        if color == "white":                        # Determine which pieces are moving
            piece = "O"
            opponents_piece = "X"
        elif color == "black":
            piece = "X"
            opponents_piece = "O"
        else:
            return print("Please enter a valid color")
        for row in range(0, 10):
            for column in range(0, 10):
                if self._board[row][column] == ".":
                    if len(self.check_vertical_down(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_vertical_up(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_horizontal_right(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_horizontal_left(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_horizontal_left(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_down_right(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_up_right(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_down_left(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
                    elif len(self.check_up_left(row, column, piece, opponents_piece)[0]) > 0:
                        moves_list.append((row, column))
        return moves_list

    def make_move(self, color, piece_position):
        """
        Places a piece for the given color in the given position and captures pieces on the board accordingly
        """
        color = color.lower()
        if color == "white":                        # Determine which pieces are moving
            piece = "O"
            opponents_piece = "X"
        elif color == "black":
            piece = "X"
            opponents_piece = "O"
        else:
            return print("Please enter a valid color")
        position_row = piece_position[0]      # Mark given rows and columns
        position_column = piece_position[1]
        self._board[position_row][position_column] = piece
        vertical_down_check = self.check_vertical_down(position_row, position_column, piece, opponents_piece)  # Check Down
        if len(vertical_down_check[0]) > 0:                                   # If pieces are taken down
            self.capture_pieces_down(vertical_down_check, position_row, position_column, piece)    # Capture pieces
        vertical_up_check = self.check_vertical_up(position_row, position_column, piece, opponents_piece)  # Check Up
        if len(vertical_up_check[0]) > 0:                                     # If pieces are taken up
            self.capture_pieces_up(vertical_up_check, position_row, position_column, piece)        # Capture pieces
        horizontal_right_check = self.check_horizontal_right(position_row, position_column, piece, opponents_piece)
        if len(horizontal_right_check[0]) > 0:
            self.capture_pieces_horizontal_right(horizontal_right_check, position_row, position_column, piece)
        horizontal_left_check = self.check_horizontal_left(position_row, position_column, piece, opponents_piece)
        if len(horizontal_left_check[0]) > 0:
            self.capture_pieces_horizontal_left(horizontal_left_check, position_row, position_column, piece)
        down_right_check = self.check_down_right(position_row, position_column, piece, opponents_piece)
        if len(down_right_check[0]) > 0:
            self.capture_pieces_down_right(down_right_check, position_row, position_column, piece)
        up_right_check = self.check_up_right(position_row, position_column, piece, opponents_piece)
        if len(up_right_check[0]) > 0:
            self.capture_pieces_up_right(up_right_check, position_row, position_column, piece)
        down_left_check = self.check_down_left(position_row, position_column, piece, opponents_piece)
        if len(down_left_check[0]) > 0:
            self.capture_pieces_down_left(down_left_check, position_row, position_column, piece)
        up_left_check = self.check_up_left(position_row, position_column, piece, opponents_piece)
        if len(up_left_check[0]) > 0:
            self.capture_pieces_up_left(up_left_check, position_row, position_column, piece)
        return self._board

    def play_game(self, player_color, piece_position):
        """
        Checks if the given position is a valid move for the given player. If it is a valid move it calls the
        make move function to place the piece on the board. Play_game also determines and declares the winner of
        the game and returns the final score.
        """
        position_row = piece_position[0]      # Mark given rows and columns
        position_column = piece_position[1]
        if position_row > 9 or position_row < 1:        # Check if the move is on the board
            print("Here are the valid moves:", self.return_available_positions(player_color))
            return "Invalid move"
        if position_column > 9 or position_column < 1:
            print("Here are the valid moves:", self.return_available_positions(player_color))
            return "Invalid move"
        if len(self.return_available_positions(player_color)) == 0:     # If the player has no valid moves
            print("Here are the valid moves:", self.return_available_positions(player_color))
            return "Invalid move"
        if self._board[position_row][position_column] != ".":   # Check if the location is open
            print("Here are the valid moves:", self.return_available_positions(player_color))
            return "Invalid move"
        if piece_position in self.return_available_positions(player_color):
            self.make_move(player_color, piece_position)
        else:
            print("Here are the valid moves:", self.return_available_positions(player_color))
            return "Invalid move"
        white_points = 0
        black_points = 0
        for row in range(0, 10):               # Iterate through the board and count the pieces
            for column in range(0, 10):
                if self._board[row][column] == "O":
                    white_points += 1
                if self._board[row][column] == "X":
                    black_points += 1
        if not self.return_available_positions("white"):
            if not self.return_available_positions("black"):
                print("Game is ended. White piece:", white_points, " Black Piece:", black_points)
                print(self.return_winner())
