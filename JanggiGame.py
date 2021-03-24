# Author: Ryan Bharat
# Description: This program will simulate a Janggi, a Korean version of chess.
# SO: Soldier, CH: Chariot, HO: Horse, EL: Elephant, CA: Cannon, GU: Guards, GE: General


class JanggiGame:
    """ Class containing representing the game board and the logic. It is the 'brain' of the game. Communicates
    with the Move and Piece class to obtain information about the movements of pieces and piece attributes. """

    def __init__(self):
        """ Initializes an 10 row by 9 column board with _game_state, _player_turn, _fortress_coordinates, and _in_check
        , and _call_move as data members. Will then call a method _place_pieces. """
        self._janggi_board = [[[]] * 9 for i in range(10)]
        self._game_state = 'UNFINISHED'
        self._player_turn = 'BLUE'
        self._call_move = {'SO': self.get_soldier_moves, 'CH': self.get_chariot_moves, 'HO': self.get_horse_moves,
                           'EL': self.get_elephant_moves, 'CA': self.get_cannon_moves, 'GU': self.get_guard_moves,
                           'GE': self.get_general_moves}
        self._fortress_coordinates = [(7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5), (9, 3), (9, 4), (9, 5),
                                      (2, 3), (2, 4), (2, 5), (1, 3), (1, 4), (1, 5), (0, 3), (0, 4), (0, 5)]
        self._in_check = {'BLUE': False, 'RED': False}
        self.place_pieces()

    def show_janggi_board(self):
        """ Displays a console view of the board board with Red player on the top end and Blue on the bottom """
        print('    a , b , c , d , e , f , g , h , i ,')
        i = 1
        for row in self.get_janggi_board():
            print(i, end= '  ')
            i += 1
            for place in row:
                if place:
                    print(place.get_name(), end=" ,")
                else:
                    print(place, end=" ,")
            print()

    def get_janggi_board(self):
        """ Getter for _janggi_board """
        return self._janggi_board

    def set_janggi_board(self, row, column, element):
        """ Setter method for _janggi_board that takes a row, column, and element and substitutes that into the board """
        self._janggi_board[row][column] = element

    def get_game_state(self):
        """ Getter for game state """
        return self._game_state

    def set_game_state(self, state):
        """ Setter method for _game_state. Takes a string and sets it as game_state """
        self._game_state = state

    def get_player_turn(self):
        """ Getter for _player_turn """
        return self._player_turn

    def set_player_turn(self, player):
        """ Setter for _player_turn """
        self._player_turn = player

    def get_call_move(self):
        """ Getter method for _call_moves """
        return self._call_move

    def set_call_move(self, dict):
        """ Setter method for _call_moves"""
        self._call_move = dict

    def get_fortress_coordinates(self):
        """ Getter method for fortress coordinates """
        return self._fortress_coordinates

    def set_fortress_coordinates(self, coordinates):
        """ Setter method for fortress coordinates """
        self._fortress_coordinates = coordinates

    def set_in_check(self, player, value):
        """ Setter method of _in_check """
        self._in_check[player] = value

    def get_in_check(self, player):
        """ Getter method for _in_check """
        return self._in_check[player]

    def get_tile_occupant(self, coordinate):
        """ Takes a list (row,column) and returns the current piece at tile"""
        return self.get_janggi_board()[coordinate[0]][coordinate[1]]

    def place_pieces(self):
        """ Initializes the pieces on the board """
        # Place Soldiers
        for i in range(0, 9, 2):
            self.set_janggi_board(6, i, Soldier('BLUE'))
        for i in range(0, 9, 2):
            self.set_janggi_board(3, i, Soldier('RED'))
        # Place Cannons
        self.set_janggi_board(7, 1, Cannon('BLUE'))
        self.set_janggi_board(7, 7, Cannon('BLUE'))
        self.set_janggi_board(2, 1, Cannon('RED'))
        self.set_janggi_board(2, 7, Cannon('RED'))
        # Place Generals
        self.set_janggi_board(8, 4, General('BLUE'))
        self.set_janggi_board(1, 4, General('RED'))
        # Place Chariots
        self.set_janggi_board(9, 0, Chariot('BLUE'))
        self.set_janggi_board(9, 8, Chariot('BLUE'))
        self.set_janggi_board(0, 0, Chariot('RED'))
        self.set_janggi_board(0, 8, Chariot('RED'))
        # Place Elephants
        self.set_janggi_board(9, 1, Elephant('BLUE'))
        self.set_janggi_board(9, 6, Elephant('BLUE'))
        self.set_janggi_board(0, 1, Elephant('RED'))
        self.set_janggi_board(0, 6, Elephant('RED'))
        # Place Horses
        self.set_janggi_board(9, 2, Horse('BLUE'))
        self.set_janggi_board(9, 7, Horse('BLUE'))
        self.set_janggi_board(0, 2, Horse('RED'))
        self.set_janggi_board(0, 7, Horse('RED'))
        # Place Guards
        self.set_janggi_board(9, 3, Guard('BLUE'))
        self.set_janggi_board(9, 5, Guard('BLUE'))
        self.set_janggi_board(0, 3, Guard('RED'))
        self.set_janggi_board(0, 5, Guard('RED'))

    def is_in_check(self, player):
        "Takes 'red' or 'blue' as a parameter and returns True if that player is in check, but False otherwise"
        player = player.upper()
        if self.get_in_check(player) == True:
            return True
        else:
            return False

    def check_in_check(self, player):
        """ After Player A makes a move but before the turn is switched, this method will run a check to see
          if Player B's General's coordinates are within the moveset for Player A. If they are, Player B is put into
          check """
        enemy = 'RED' if player == 'BLUE' else 'BLUE'
        enemy_general = self.get_general_location(enemy)
        player_moves = self.get_all_valid_moves()
        for player_move in player_moves:
            dst_row = player_move.get_dst_row()
            dst_col = player_move.get_dst_col()
            if (dst_row, dst_col) == enemy_general:
                self.set_in_check(enemy, True)  # If general is in moveset of player, put enemy in check
                self.change_turns()  # make enemy the player
                enemy_moves = self.get_all_valid_moves()
                if enemy_moves == []:  # If enemy has no moves, player has won. This list is still returning moves. Will need to check.
                    self.set_game_state(player + '_WON')
                    self.change_turns()  # Return to intial turn
                    break
                self.change_turns()  # restore initial turn

    def make_move(self, source, destination):
        """ Takes two board string parameters, converts them to board coordinates, and executes the move """
        if self.get_game_state() == 'UNFINISHED':
            move = Move(self.convert_location(source), self.convert_location(destination), self.get_janggi_board())
            player = self.get_player_turn()
            valid_moves = self.get_all_valid_moves()
            if move in valid_moves:  # Valid moves will pull valid moves for the current player's turn
                if move.get_src_row() == move.get_dst_row() and move.get_src_col() == move.get_dst_col():
                    pass
                else:
                    self.set_janggi_board(move.get_dst_row(), move.get_dst_col(),
                                      move.get_src_object())  # Change board tile at dst to reflect src object
                    self.set_janggi_board(move.get_src_row(), move.get_src_col(), [])  # Set src tile to empty
                if self.is_in_check(player) == True:  # Player removes themself from being in check
                    self.set_in_check(player, False)
                self.check_in_check(player)  # Checks if the valid move puts the enemy player in check/checkmate
                self.change_turns()
                return True
        return False

    def convert_location(self, location):
        """ Converts the location string (e3, a0, etc.) to index reference """
        row_to_index = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}
        column_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        # If you take input of 'e9' in column,row you should get (8,4) in row, column format
        try:
            column = column_to_index[location[0]]
            row = row_to_index[location[1::]]
            return (row, column)
        except IndexError:
            return False
        except KeyError:
            return False

    def change_turns(self):
        """ Changes the player turn """
        if self.get_player_turn() == 'RED':
            self.set_player_turn('BLUE')
        elif self.get_player_turn() == 'BLUE':
            self.set_player_turn('RED')

    def get_general_location(self, player):
        """ Takes a player parameter and returns the location of their general in (row,column) format """
        fortress_coords = self.get_fortress_coordinates()
        for coord in fortress_coords:
            tile = self.get_tile_occupant(coord)
            if tile != []:
                if tile.get_name() == 'GE' and tile.get_player() == player:
                    return coord

    def get_all_valid_moves(self):
        """ Takes a list of all possible moves and checks to see if it is a valid move. This method handles
         the checking for the current player making a move that would put their General in check. """
        valid_moves = []
        possible_moves = self.get_all_possible_moves()
        player = self.get_player_turn()
        enemy = 'RED' if player == 'BLUE' else 'BLUE'
        for move in possible_moves:
            self.set_janggi_board(move.get_dst_row(), move.get_dst_col(),
                                  move.get_src_object())  # Change board tile at dst to reflect src object
            self.set_janggi_board(move.get_src_row(), move.get_src_col(), [])  # Set src tile to empty
            self.change_turns()
            enemy_moves = self.get_all_possible_moves()
            player_general = self.get_general_location(player)
            attacked = False
            while attacked == False:
                for enemy_move in enemy_moves:
                    dst_row = enemy_move.get_dst_row()
                    dst_col = enemy_move.get_dst_col()
                    if player_general == (
                    dst_row, dst_col):  # Check if player's general is in an enemy move's destination coordinate
                        attacked = True
                        break
                break
            if attacked == False:
                valid_moves.append(move)  # Append move if it doesn't expose player's general to enemy_move
            self.set_janggi_board(move.get_src_row(), move.get_src_col(), move.get_src_object())  # Restore board state
            self.set_janggi_board(move.get_dst_row(), move.get_dst_col(), move.get_dst_object())
            self.change_turns()  # Restore turn
        return valid_moves

    def get_all_possible_moves(self):
        """ Gets all possible moves without considering checks """
        moves = []
        for row in range(len(self.get_janggi_board())):
            for column in range(len(self.get_janggi_board()[row])):
                tile = self.get_janggi_board()[row][column]
                if isinstance(tile, Piece) and tile.get_player() == self.get_player_turn():
                    self.get_call_move()[tile.get_name()](row, column, moves)  # Calls the appropriate method based on class of Tile
        return moves

    def get_soldier_moves(self, row, column, moves):
        """ Get all soldier moves for the soldier at a specified row,column and add to list of moves"""
        turn = self.get_player_turn()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        board = self.get_janggi_board()
        possible_directions = {'RED': [(1, 0), (0, -1), (0, 1)], 'BLUE': [(-1, 0), (0, -1), (0, 1)]}
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        if self.check_in_fortress(row, column):
            offset = (-1, 1)
            row_offset = {'RED': 1,'BLUE': -1}
            for r in row_offset:
                if r == turn:
                    for c in offset:  # Left or right on board
                        for d in range(1, 2):  # Possible range to move diagonally for a soldier
                            target_row = row + row_offset[r] * d
                            target_col = column + c * d
                            if self.check_in_fortress(target_row, target_col):
                                tile = self.get_tile_occupant((target_row, target_col))
                                if tile == [] or tile.get_player() == enemy:
                                    moves.append(Move((row, column), (target_row, target_col), board))
        for k in possible_directions:
            if k == turn:
                movements = possible_directions[k]
                for m in movements:
                    dst_row = row + m[0]
                    dst_col = column + m[1]
                    if self.check_in_board(dst_row, dst_col):
                        tile = self.get_tile_occupant((dst_row, dst_col))
                        if tile == [] or tile.get_player() == enemy:
                            moves.append(Move((row, column), (dst_row, dst_col), board))

    def check_in_fortress(self, row, column):
        """ Takes row and column coordinates and returns True if it is within one of the fortress coordinates """
        return True if (row, column) in self.get_fortress_coordinates() else False

    def check_in_board(self, row, column):
        """ Takes a row and column coordinates and returns True if it is within board parameters, else False """
        return True if (0 <= row <= 9 and 0 <= column <= 8) else False

    def get_chariot_moves(self, row, column, moves):
        """ Takes position of a chariot piece and returns all possible movements to a list """
        turn = self.get_player_turn()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        board = self.get_janggi_board()
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        if self.check_in_fortress(row, column):  # Check if in fortress
            offset = (-1, 1)
            for r in offset:  # Up or down board
                for c in offset:  # Left or right on board
                    for d in range(1, 3):  # Possible range to move diagonally for a chariot
                        target_row = row + r * d
                        target_col = column + c * d
                        if self.check_in_fortress(target_row, target_col):
                            tile = self.get_tile_occupant((target_row, target_col))
                            if tile == []:
                                moves.append(Move((row, column), (target_row, target_col), board))
                            elif tile.get_player() == enemy:
                                moves.append(Move((row, column), (target_row, target_col), board))
                                break
                            else:
                                break
        for k in possible_directions:  # For row directions then column directions
            for l in range(1, 10):  # Highest possible index is 9
                dst_row = row + k[0] * l
                dst_col = column + k[1] * l
                if self.check_in_board(dst_row, dst_col):  # Check if the destination is in board
                    tile = self.get_tile_occupant((dst_row, dst_col))
                    if tile == []:
                        moves.append(Move((row, column), (dst_row, dst_col), board))
                    elif tile.get_player() == enemy:
                        moves.append(Move((row, column), (dst_row, dst_col), board))
                        break
                    else:
                        break

    def get_horse_moves(self, row, column, moves):
        """ Takes the position of a horse piece and appends all its possible moves to a list"""
        turn = self.get_player_turn()
        board = self.get_janggi_board()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        adjacent = {(-1, 0): [(-2, -1), (-2, 1)], (1, 0): [(2, -1), (2, 1)], (0, -1): [(-1, -2), (1, -2)],
                    (0, 1): [(-1, 2), (1, 2)]}
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        for a in adjacent:
            adj_row = row + a[0]
            adj_col = column + a[1]
            if self.check_in_board(adj_row, adj_col) and self.get_tile_occupant(
                    (adj_row, adj_col)) == []:  # Check if adjacent tile in board and free
                end_tiles = adjacent[a]
                for end in end_tiles:
                    end_row = end[0] + row
                    end_col = end[1] + column
                    if self.check_in_board(end_row, end_col):  # Check if end tile is in the board
                        tile = self.get_tile_occupant((end_row, end_col))
                        if tile == [] or tile.get_player() == enemy:
                            moves.append(Move((row, column), (end_row, end_col), board))

    def get_elephant_moves(self, row, column, moves):
        """ Takes the position of an elephant piece and appends all its possible moves to a list"""
        turn = self.get_player_turn()
        board = self.get_janggi_board()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        adjacent = {(-1, 0): [{(-2, -1): (-3, -2)}, {(-2, 1): (-3, 2)}], (1, 0): [{(2, -1): (3, -2)}, {(2, 1): (3, 2)}],
                    (0, -1): [{(-1, -2): (-2, -3)}, {(1, -2): (2, -3)}], (0, 1): [{(-1, 2): (-2, 3)}, {(1, 2): (2, 3)}]}
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        for a in adjacent:
            adj_row = row + a[0]
            adj_col = column + a[1]
            if self.check_in_board(adj_row, adj_col) and self.get_tile_occupant(
                    (adj_row, adj_col)) == []:  # Check if adjacent tile in board and free
                diag = adjacent[a]
                for d in range(len(diag)):
                    for i in diag[d]:
                        diag_row = row + i[0]
                        diag_col = column + i[1]
                        if self.check_in_board(diag_row, diag_col) and self.get_tile_occupant(
                                (diag_row, diag_col)) == []:  # Check if diagonal tile from adjacent is clear for move
                            end_row = row + diag[d][i][0]
                            end_col = column + diag[d][i][1]
                            if self.check_in_board(end_row,
                                                   end_col):  # Check if end tile is within board confines and not occupied by friendly
                                if self.get_tile_occupant((end_row, end_col)) == [] or self.get_tile_occupant(
                                        (end_row, end_col)) == enemy:
                                    moves.append(Move((row, column), (end_row, end_col), board))

    def get_cannon_moves(self, row, column, moves):
        """ Takes the position of a cannon piece and appends all possible movements to a list """
        turn = self.get_player_turn()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        board = self.get_janggi_board()
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        friendly, checked = False, False
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        if self.check_in_fortress(row, column):  # Check if in fortress
            offset = (-1, 1)
            for r in offset:  # Up or down board
                for c in offset:  # Left or right on board
                    checked = False
                    for d in range(1, 3):  # Possible range to move diagonally for a cannon
                        while friendly == True:  # Block executes when a 'jump' piece is identified
                            for b in range(d, 3):  # Generates the next diagonal
                                fort_row = row + r * b
                                fort_col = column + c * b
                                if self.check_in_fortress(fort_row, fort_col):  # checks if next diagonal is in fortress
                                    fort_tile = self.get_tile_occupant((fort_row, fort_col))
                                    if fort_tile == []:
                                        moves.append(Move((row, column), (fort_row, fort_tile), board))
                                    elif fort_tile.get_player() == enemy:
                                        if fort_tile.get_name() == 'CA':
                                            break
                                        else:
                                            moves.append(Move((row, column), (fort_row, fort_tile), board))
                                            break
                                    else:
                                        break
                            friendly = False
                            checked = True
                        if checked == True:
                            break
                        target_row = row + r * d
                        target_col = column + c * d
                        if self.check_in_fortress(target_row, target_col):
                            tile = self.get_tile_occupant((target_row, target_col))
                            if tile == []:
                                break  # If no intervening piece, break
                            elif tile.get_player() == turn and tile.get_name() != 'CA':
                                friendly = True
                            else:
                                break
        for k in possible_directions:  # For row directions then column directions
            checked = False
            for l in range(1, 10):  # Highest possible index is 9
                while friendly == True:
                    for j in range(l, 10):  # Pick up where friendly piece was found
                        target_row = row + k[0] * j
                        target_col = column + k[1] * j
                        if self.check_in_board(target_row, target_col):
                            tile = self.get_tile_occupant((target_row, target_col))
                            if tile == []:
                                moves.append(Move((row, column), (target_row, target_col), board))
                            elif tile.get_player() == enemy:
                                if tile.get_name() == 'CA':
                                    break  # Cannot capture enemy cannons
                                else:
                                    moves.append(Move((row, column), (target_row, target_col), board))
                                    break  # Cannot capture past enemy tiles
                            else:
                                break  # Encountered another friendly, so stop checking direction
                    friendly = False
                    checked = True
                if checked == True:
                    break
                dst_row = row + k[0] * l
                dst_col = column + k[1] * l
                if self.check_in_board(dst_row, dst_col):  # Check if the destination is in board
                    tile = self.get_tile_occupant((dst_row, dst_col))
                    if tile != []:
                        if tile.get_name() == 'CA':
                            break
                        else: # Intervening non-cannon piece has been found
                            friendly = True


    def get_guard_moves(self, row, column, moves):
        """ Takes the position of Guard piece and appends all its possible movements to a list """
        turn = self.get_player_turn()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        board = self.get_janggi_board()
        possible_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        for p in possible_directions:
            end_row = row + p[0]
            end_col = column + p[1]
            if self.check_in_fortress(end_row, end_col):
                end_tile = self.get_tile_occupant((end_row, end_col))
                if end_tile == [] or end_tile.get_player() == enemy:
                    moves.append(Move((row, column), (end_row, end_col), board))

    def get_general_moves(self, row, column, moves):
        """ Takes the position of a General piece and appends all its possible movements to a list """
        turn = self.get_player_turn()
        enemy = 'BLUE' if turn == 'RED' else 'RED'
        board = self.get_janggi_board()
        possible_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if self.is_in_check(turn) == False:
            moves.append(Move((row, column), (row, column), board))  # Equivalent of a pass. Piece does not move.
        for p in possible_directions:
            end_row = row + p[0]
            end_col = column + p[1]
            if self.check_in_fortress(end_row, end_col):
                end_tile = self.get_tile_occupant((end_row, end_col))
                if end_tile == [] or end_tile.get_player() == enemy:
                    moves.append(Move((row, column), (end_row, end_col), board))


class Move:
    """ Contains all data relevant to the player actions at a particular state in the game. The board will interpret data from this class and
     apply it to its own logic in order to process moves. Move objects are not used or accessed beyond the current player's turn. It communicates
     with the JanggiGame class to provide choices for the player. """

    def __init__(self, source, destination, board):
        """ Initializes a move object with a source and destination tile, and an instance of JanggiGame """
        self._src_row = source[0]
        self._src_col = source[1]
        self._dst_row = destination[0]
        self._dst_col = destination[1]
        self._src_object = board[self._src_row][self._src_col]
        self._dst_object = board[self._dst_row][self._dst_col]
        self._move_id = (self._src_row, self._src_col, self._dst_row, self._dst_col)

    def __eq__(self, other):
        """ Overrides the equals method to allow for comparing between Move objects. """
        if isinstance(other, Move):
            return self.get_move_id() == other.get_move_id()
        return False

    def get_move_id(self):
        """ Getter for the _move_id data member """
        return self._move_id

    def set_move_id(self):
        """ Setter for the _move_id data member """

    def get_src_row(self):
        """ Getter for _src_row data member """
        return self._src_row

    def set_src_row(self, row):
        """ Setter for _src_row """
        self._src_row = row

    def get_src_col(self):
        """ Getter for _src_col """
        return self._src_col

    def set_src_col(self, col):
        """ Setter for _src_col """
        self._src_col = col

    def get_dst_row(self):
        """ Getter for _dst_row """
        return self._dst_row

    def set_dst_row(self, row):
        """ Setter for _dst_row """
        self._dst_row = row

    def get_dst_col(self):
        """ Getter for _dst_col """
        return self._dst_col

    def set_dst_col(self, col):
        """ Setter for _dst_col """
        self._dst_col = col

    def get_src_object(self):
        """ Getter for _src_object """
        return self._src_object

    def set_src_object(self, object):
        """ Setter for _src_object """
        self._src_object = object

    def get_dst_object(self):
        """ Getter for dst_object """
        return self._dst_object

    def set_dst_object(self, object):
        """ Setter for _dst_object """
        self._dst_object = object


class Piece:
    """ Parent class for the different Janggi pieces. Communicates with the JanggiGame
     class to initialize piece types and various data members. """

    def __init__(self, player):
        """ Initializes a Piece object with a player and name data member"""
        self._player = player
        self._name = None

    def get_player(self):
        """ Returns the player who controls the piece """
        return self._player

    def set_player(self, player):
        """ Setter method for the _player data member"""
        self._player = player

    def get_name(self):
        """ Getter method for the _name data member """
        return self._name

    def set_name(self, name):
        """ Setter method for the _name data member """
        self._name = name


class Soldier(Piece):
    """ Soldier subclass for soldier pieces """

    def __init__(self, player):
        super().__init__(player)
        self._name = 'SO'


class Cannon(Piece):
    """ Cannon subclass for cannon pieces """

    def __init__(self, player):
        super().__init__(player)
        self._name = 'CA'


class General(Piece):
    """ General subclass for general piece"""

    def __init__(self, player):
        super().__init__(player)
        self._name = 'GE'


class Chariot(Piece):
    """ Chariot subclass for chariot pieces """

    def __init__(self, player):
        super().__init__(player)
        self._name = 'CH'


class Horse(Piece):
    """ Horse subclass for horse/knight pieces """

    def __init__(self, player):
        super().__init__(player)
        self._name = 'HO'


class Elephant(Piece):
    """ Elephant subclass for elephant pieces """

    def __init__(self, player):
        super().__init__(player)
        self._name = 'EL'


class Guard(Piece):
    """ Guard subclass for guard pieces"""

    def __init__(self, player):
        super().__init__(player)
        self._name = 'GU'

