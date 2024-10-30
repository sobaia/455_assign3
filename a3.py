# CMPUT 455 Assignment 3 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a3.html

import sys
import random

class CommandInterface:

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner,
            "loadpatterns" : self.loadpatterns,
            "policy_moves" : self.policy_moves
        }
        self.board = [[None]]
        self.player = 1
        self.pattern = []
    
    #===============================================================================================
    # VVVVVVVVVV START of PREDEFINED FUNCTIONS. DO NOT MODIFY. VVVVVVVVVV
    #===============================================================================================

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Every command will print '= 1' or '= -1' at the end of execution to indicate success or failure respectively
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # Will make sure there are enough arguments, and that they are valid numbers
    # Not necessary for commands without arguments
    def arg_check(self, args, template):
        converted_args = []
        if len(args) < len(template.split(" ")):
            print("Not enough arguments.\nExpected arguments:", template, file=sys.stderr)
            print("Recieved arguments: ", end="", file=sys.stderr)
            for a in args:
                print(a, end=" ", file=sys.stderr)
            print(file=sys.stderr)
            return False
        for i, arg in enumerate(args):
            try:
                converted_args.append(int(arg))
            except ValueError:
                print("Argument '" + arg + "' cannot be interpreted as a number.\nExpected arguments:", template, file=sys.stderr)
                return False
        args = converted_args
        return True

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ END OF PREDEFINED FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    #===============================================================================================

    #===============================================================================================
    # VVVVVVVVVV START OF ASSIGNMENT 3 FUNCTIONS. ADD/REMOVE/MODIFY AS NEEDED. VVVVVVVV
    #===============================================================================================

    def game(self, args):
        if not self.arg_check(args, "n m"):
            return False
        n, m = [int(x) for x in args]
        if n < 0 or m < 0:
            print("Invalid board size:", n, m, file=sys.stderr)
            return False
        
        self.board = []
        for i in range(m):
            self.board.append([None]*n)
        self.player = 1
        return True
    
    def show(self, args):
        for row in self.board:
            for x in row:
                if x is None:
                    print(".", end="")
                else:
                    print(x, end="")
            print()                    
        return True

    def is_legal_reason(self, x, y, num):
        if self.board[y][x] is not None:
            return False, "occupied"
        
        consecutive = 0
        count = 0
        self.board[y][x] = num
        for row in range(len(self.board)):
            if self.board[row][x] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False, "three in a row"
            else:
                consecutive = 0
        too_many = count > len(self.board) // 2 + len(self.board) % 2
        
        consecutive = 0
        count = 0
        for col in range(len(self.board[0])):
            if self.board[y][col] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False, "three in a row"
            else:
                consecutive = 0
        if too_many or count > len(self.board[0]) // 2 + len(self.board[0]) % 2:
            self.board[y][x] = None
            return False, "too many " + str(num)

        self.board[y][x] = None
        return True, ""
    
    def is_legal(self, x, y, num):
        if self.board[y][x] is not None:
            return False
        
        consecutive = 0
        count = 0
        self.board[y][x] = num
        for row in range(len(self.board)):
            if self.board[row][x] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False
            else:
                consecutive = 0
        if count > len(self.board) // 2 + len(self.board) % 2:
            self.board[y][x] = None
            return False
        
        consecutive = 0
        count = 0
        for col in range(len(self.board[0])):
            if self.board[y][col] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False
            else:
                consecutive = 0
        if count > len(self.board[0]) // 2 + len(self.board[0]) % 2:
            self.board[y][x] = None
            return False

        self.board[y][x] = None
        return True
    
    def valid_move(self, x, y, num):
        return  x >= 0 and x < len(self.board[0]) and\
                y >= 0 and y < len(self.board) and\
                (num == 0 or num == 1) and\
                self.is_legal(x, y, num)

    def play(self, args):
        err = ""
        if len(args) != 3:
            print("= illegal move: " + " ".join(args) + " wrong number of arguments\n")
            return False
        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            print("= illegal move: " + " ".join(args) + " wrong coordinate\n")
            return False
        if  x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board):
            print("= illegal move: " + " ".join(args) + " wrong coordinate\n")
            return False
        if args[2] != '0' and args[2] != '1':
            print("= illegal move: " + " ".join(args) + " wrong number\n")
            return False
        num = int(args[2])
        legal, reason = self.is_legal_reason(x, y, num)
        if not legal:
            print("= illegal move: " + " ".join(args) + " " + reason + "\n")
            return False
        self.board[y][x] = num
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
        return True
    
    def legal(self, args):
        if not self.arg_check(args, "x y number"):
            return False
        x, y, num = [int(x) for x in args]
        if self.valid_move(x, y, num):
            print("yes")
        else:
            print("no")
        return True
    
    def get_legal_moves(self):
        moves = []
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                for num in range(2):
                    if self.is_legal(x, y, num):
                        moves.append([str(x), str(y), str(num)])
        return moves

    def genmove(self, args):
        moves = self.get_legal_moves()
        if len(moves) == 0:
            print("resign")
        else:
            rand_move = moves[random.randint(0, len(moves)-1)]
            self.play(rand_move)
            print(" ".join(rand_move))
        return True
    
    def winner(self, args):
        if len(self.get_legal_moves()) == 0:
            if self.player == 1:
                print(2)
            else:
                print(1)
        else:
            print("unfinished")
        return True
    
    # new function to be implemented for assignment 3
    def loadpatterns(self, args):
        with open(args[0], 'r') as file:
            self.pattern = [line.strip().split() for line in file]

        print(self.pattern)
    
        # Delete previously loaded patterns
        # Load pattern in format: "loadpatterns xpattern.txt"
        return True
    
    # new function to be implemented for assignment 3
    def policy_moves(self, args):
        # Compare loaded pattern to current board
        # Weigh each move according to pattern
        # show all moves and weights
        # -- Numerically sorted in increasing order by x-coord first, then y-coord, then by digit

        final_move = ""
        rows = [''.join(str(x) if x is not None else '.' for x in row) for row in self.board]
        cols = [''.join(str(x) if x is not None else '.' for x in col) for col in zip(*self.board)]
        pattern_rows = []
        pattern_cols = []
        full_patterns = self.pattern

        # I first want to add the flipped versions of the patterns so I can implement 180 flips
        for entry in self.pattern:
            pattern_entry = [entry[0][::-1], entry[1], entry[2]]
            full_patterns.append(pattern_entry)
        
        print(full_patterns)


        # legal_moves = self.get_legal_moves()
        # # If there are legal moves
        # if legal_moves != []:
        #     # Sort the Legal Moves
        #     sorted_legal = sorted(legal_moves, key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
        #     # If there are no patterns to be looked at
        #     if self.pattern == []:
        #         # Calculate the final output based on basic math
        #         for i in range(len(sorted_legal)):
        #             final_move += sorted_legal[i][0] + " " + sorted_legal[i][1] + " " + sorted_legal[i][2] + " " + str(round(1/len(sorted_legal), 3)) + " "
        #         # Make sure to get rid of the last space in the final output
        #         final_move = final_move[:-1]
        #     # If there are patterns to be looked at
        #     else:
        #         # For every pattern there is to look at
        #         for p, pattern in enumerate(self.pattern):
        #             # If there is out of bounds in the pattern
        #             if "X" in pattern[0]:
        #                 # Get the relevant part of the pattern (remove the Xs)
        #                 in_board = self.get_non_x_positions(pattern[0])
        #                 out_board = self.get_x_positions(pattern[0])
        #                 check = "".join(pattern[i] for i in in_board)
                        
        #                 # For every row I want to check if the pattern exists
        #                 for r, row in enumerate(rows):
        #                     # Make sure row is long enough to even consider a pattern
        #                     if (len(row) - len(check) + 1) > 1:
        #                         # Then now check for pattern
        #                         for i in range(len(row) - len(check) + 1):
        #                             # Check for the X out of bounds positions
        #                             if row[i:i+len(check)] == check:
        #                                 difference = i - in_board[0]
        #                                 range_check = [x + difference for x in out_board]
        #                                 all_out_of_bounds = all(value > (len(row)-1) or value < 0 for value in range_check)
        #                                 # If the pattern exists with the out of bounds positions
        #                                 if all_out_of_bounds:
        #                                     pattern_rows.append([r, pattern])
        #                 # For every col I want to check if the pattern exists          
        #                 for c, col in enumerate(cols):
        #                     # Make sure col is long enough to even consider a pattern
        #                     if (len(col) - len(check) + 1) > 1:
        #                         # Then now check for pattern
        #                         for i in range(len(col) - len(check) + 1):
        #                             # Check for the X out of bounds positions
        #                             if row[i:i+len(col)] == col:
        #                                 difference = i - in_board[0]
        #                                 range_check = [x + difference for x in out_board]
        #                                 all_out_of_bounds = all(value > (len(col)-1) or value < 0 for value in range_check)
        #                                 # If the pattern exists with the out of bounds positions
        #                                 if all_out_of_bounds:
        #                                     pattern_cols.append([c, pattern])

                    






                
        
        # print(final_move)

        # pattern = "1..XX"
        # pattern2 = "XX..1"
        # board = "101101.1.."
        # board2 = "..1001001."
        # in_board = []
        # pattern_found = False


        # if "X" in pattern:
        #     in_board = self.get_non_x_positions(pattern)
        #     out_board = self.get_x_positions(pattern)
        #     check = "".join(pattern[i] for i in in_board)

        #     for i in range(len(board) - len(check) + 1):
        #         if board[i:i+len(check)] == check:
        #             difference = i - in_board[0]
        #             range_check = [x + difference for x in out_board]
        #             all_out_of_bounds = all(value > (len(board)-1) or value < 0 for value in range_check)
        #             if all_out_of_bounds:
        #                 pattern_found = True
        #                 break
            
            

            

        return True
    
    def get_x_positions(self, pattern):
        positions = [i for i, c in enumerate(pattern) if c == "X"]
        return positions
    def get_non_x_positions(self, pattern):
        positions = [i for i, c in enumerate(pattern) if c != "X"]
        return positions
    
    #===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ END OF ASSIGNMENT 3 FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    #===============================================================================================
    
if __name__ == "__main__":#
    interface = CommandInterface()
    interface.main_loop()