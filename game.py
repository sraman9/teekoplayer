import random
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.max_depth = 3 

    def run_challenge_test(self):
        """ Set to True if you would like to run gradescope against the challenge AI!
        Leave as False if you would like to run the gradescope tests faster for debugging.
        You can still get full credit with this set to False
        """ 
        return False

    def make_move(self, state):
        #Query: detect drop phase based on piece count
        drop_phase = sum([row.count('b') + row.count('r') for row in state]) < 8

        try:
            _, new_state = self.max_value(state, 0)
            move = self.get_move_diff(state, new_state)
        except Exception as e:      #DEBUG: Query - How to handle failed decision
            print("Fallback to random move due to error:", e)
            move = []

            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        move = [(i, j)]
                        break
                if move:
                    break
            return move

        if drop_phase:
            return [move[0]]  # Ensure correct format
        return move



    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def succ(self, state):
        successors = []
        count = sum(row.count(self.my_piece) + row.count(self.opp) for row in state)

        if count < 8:  # Drop phase
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_state = copy.deepcopy(state)
                        new_state[i][j] = self.my_piece if count % 2 == 0 else self.opp
                        successors.append(new_state)
        else:  # Move phase
            piece = self.my_piece if count % 2 == 0 else self.opp
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                if dx == 0 and dy == 0:
                                    continue
                                ni, nj = i + dx, j + dy
                                if 0 <= ni < 5 and 0 <= nj < 5 and state[ni][nj] == ' ':
                                    new_state = copy.deepcopy(state)
                                    new_state[i][j] = ' '
                                    new_state[ni][nj] = piece
                                    successors.append(new_state)

        return successors


    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
                
        def check_line(line):       #HELPER
            return all(cell == self.my_piece for cell in line), all(cell == self.opp for cell in line)

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2, 5):
                d1 = [state[i + k][j - k] for k in range(4)]
                my_d1, opp_d1 = check_line(d1)
                if my_d1:
                    return 1
                if opp_d1:
                    return -1
        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(2):
                d2 = [state[i + k][j + k] for k in range(4)]
                my_d2, opp_d2 = check_line(d2)
                if my_d2:
                    return 1
                if opp_d2:
                    return -1
        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                square = [state[i][j], state[i + 1][j], state[i][j + 1], state[i + 1][j + 1]]
                my_sq, opp_sq = check_line(square)
                if my_sq:
                    return 1
                if opp_sq:
                    return -1

        return 0 # no winner yet
    
    def get_move_diff(self, old_state, new_state):
        from_pos = None
        to_pos = None

        for i in range(5):
            for j in range(5):
                if old_state[i][j] != new_state[i][j]:
                    if old_state[i][j] == ' ' and new_state[i][j] == self.my_piece:
                        to_pos = (i, j)
                    elif old_state[i][j] == self.my_piece and new_state[i][j] == ' ':
                        from_pos = (i, j)

        if to_pos is None:      #LLM Suggestion: Catch invalid minimax output
            raise ValueError("ERROR: get_move_diff() could not determine destination")

        return [to_pos] if from_pos is None else [to_pos, from_pos]

    
    def max_value(self, state, depth):
        if depth == self.max_depth or self.game_value(state) != 0:
            return self.heuristic_game_value(state), state

        v = float('-inf')
        best_state = None

        for s in self.succ(state):
            val, _ = self.min_value(s, depth + 1)
            if val > v:
                v = val
                best_state = s

        return v, best_state
    
    def min_value(self, state, depth):
        if depth == self.max_depth or self.game_value(state) != 0:
            return self.heuristic_game_value(state), state

        v = float('inf')
        best_state = None

        for s in self.succ(state):
            val, _ = self.max_value(s, depth + 1)
            if val < v:
                v = val
                best_state = s

        return v, best_state
    
    def heuristic_game_value(self, state):
        terminal_val = self.game_value(state)
        if terminal_val != 0:
            return float(terminal_val)

        score = 0.0

        # Count how many pieces of each player are on the board
        def piece_count(p):
            return sum(row.count(p) for row in state)

        my_count = piece_count(self.my_piece)
        opp_count = piece_count(self.opp)

        score += 0.1 * (my_count - opp_count)

        # Reward for clustering
        def piece_positions(p):
            return [(i, j) for i in range(5) for j in range(5) if state[i][j] == p]

        def average_pairwise_distance(positions):       # LLM: Heuristic for clustering average distance between pieces
            if len(positions) < 2:
                return 5.0  # max spread
            total = 0
            count = 0
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    (x1, y1), (x2, y2) = positions[i], positions[j]
                    dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
                    total += dist
                    count += 1
            return total / count

        my_cluster = average_pairwise_distance(piece_positions(self.my_piece))
        opp_cluster = average_pairwise_distance(piece_positions(self.opp))

        score += 0.1 * (opp_cluster - my_cluster)  

        return max(min(score, 0.99), -0.99)


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
