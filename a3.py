from board import Board

class Solver:

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self,filename):
        self.board = Board(filename)
        self.solve()

    ##########################################
    ####   Solver
    ##########################################

    #recursively selects the most constrained unsolved space and attempts
    #to assign a value to it
    #
    #upon completion, it will leave the board in the solved state (or original
    #state if a solution does not exist)
    def solve(self):
        solved = self.solveRecurse(self.board.getMostConstrainedUnsolvedSpace())
        if (solved):
            print("solution found!")
        else:
            print("no solution found...")
        self.board.print()
        

    def solveRecurse(self, move):
        #given a tuple move and:
        #--finds possible values
        #--forward checks a chosen value, then assigns it (assuming it works)
        #--finds next most constrained unsolved spot, recurses with it
        #If the given spot cannot be assigned a value...
        #--given spot is absolutely constrained
        #--none of the moves pass a forward checking
        #... then backtrack.  do this by returning false.
        #if solve is given false, then the board can't be solved.
        possible = self.board.possibleValues(move)
        if len(possible) == 0: #no possible moves here
            return False #backtrack
        madeMove = False #if this remains false after following loop, then no move passed forward checking
        for val in possible: #make move from possible values
            self.board.makeMove(move, val)
            badMove = False #used to find bad move during forward check
            for space in self.board.unSolved: #forward check placement
                if space[0] == move[0]: #same row
                    if len(self.board.possibleValues(space)) == 0:
                        badMove = True
                        break
                if space[1] == move[1]: #same column
                    if len(self.board.possibleValues(space)) == 0:
                        badMove = True
                        break
                if self.board.rcToBox(space[0], space[1]) == self.board.rcToBox(move[0], move[1]): #same box
                    if len(self.board.possibleValues(space)) == 0:
                        badMove = True
                        break
            if (badMove):
                self.board.removeMove(move, val) #undo placement
            else: #if the move passes forward checking
                if (len(self.board.unSolved) == 0): #no more unsolved = board is done
                    madeMove = True
                    break
                elif (self.solveRecurse(self.board.getMostConstrainedUnsolvedSpace()) == True):
                    madeMove = True
                    break
                else: #backtracking...
                    self.board.removeMove(move, val) #undo placement
        if not madeMove: #forward checking restricted any possible placement
            return False #backtrack
        return True #if nothing went wrong with the chosen move, it'll reach here
        


if __name__ == "__main__":

    #change this to the input file that you'd like to test
    s = Solver('testBoard_dastardly.csv')
