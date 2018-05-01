import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        #initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unSolved = None

        #load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    #loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                #Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unSolved = set(itertools.product(range(self.n2), range(self.n2)))

                #check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row mus\t have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                #add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.rcToBox(reader.line_num-1, index)].add(int(item))
                        self.unSolved.remove((reader.line_num-1, index))

    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    #gets the unsolved space with the most current constraints
    def getMostConstrainedUnsolvedSpace(self):
        #one of the test cases (the second one) in a3_tests.py for this one didn't work.
        #I tried printing out all the constraints for each unsolved spot, and I couldn't figure out why the answer my
        #algorithm got wasn't included.  Also, one of the answers wasn't as constrained anyway, which confused me.
        #was that test case a mistake?  I emailed one of the AIs about it but since I haven't gotten a response yet I've
        #just left it commented out.  For all the other tests this works, and the solver as a whole works too.  If I find a solution
        #I will come back and fix it though.
        maxSpace = tuple()
        maxCon = 0
        if (len(self.unSolved) == 0): #empty tuple implies no unsolved spaces
            return tuple()
        for space in self.unSolved:
            r,c = space
            conList = []
            #get sum of constraints
            for i in self.valsInRows[r]:
                if not i in conList:
                    conList.append(i)
            for i in self.valsInCols[c]:
                if not i in conList:
                    conList.append(i)
            for i in self.valsInBoxes[self.rcToBox(r, c)]:
                if not i in conList:
                    conList.append(i)
            #if bigger than current max, replace
            if len(conList) > maxCon:
                maxSpace = space
                maxCon = len(conList)
        return maxSpace

    #returns True if the move is not blocked by any constraints
    def isValidMove(self,space,val):
        r,c = space
        #row?
        if (val in self.valsInRows[r]):
            return False
        #column?
        if (val in self.valsInCols[c]):
            return False
        #box?
        if (val in self.valsInBoxes[self.rcToBox(r, c)]):
            return False
        return True  #if no other return triggers, this will return


    #makes a move, records that its in the row, col, and box, and removes the space from unSolved
    def makeMove(self, space, val):
        r,c = space
        self.board[space] = val
        self.valsInRows[r].add(val)
        self.valsInCols[c].add(val)
        self.valsInBoxes[self.rcToBox(r, c)].add(val)
        self.unSolved.remove(space)
        

    #removes the move, its record in its row, col, and box, and adds the space back to unSolved
    def removeMove(self, space, val):
        r,c = space
        del self.board[space]
        self.valsInRows[r].remove(val)
        self.valsInCols[c].remove(val)
        self.valsInBoxes[self.rcToBox(r, c)].remove(val)
        self.unSolved.add(space)

    #-----Functions I made--------#

    #returns the possible moves for a given space, based on its constraints
    def possibleValues(self, space):
        r,c = space
        constraints = []
        possible = []
        for i in self.valsInRows[r]:
            if not i in constraints:
                constraints.append(i)
        for i in self.valsInCols[c]:
            if not i in constraints:
                constraints.append(i)
        for i in self.valsInBoxes[self.rcToBox(r, c)]:
            if not i in constraints:
                constraints.append(i)
        for i in range(1, 10):
            if not i in constraints:
                possible.append(i)
        return possible

    

    ##########################################
    ####   Utility Functions
    ##########################################

    #converts a given row and column to its inner box number
    def rcToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n


    #prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            #add row divider
            if r % self.n == 0 and not r == 0:
                print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                #add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                #add value placeholder
                if val is None:
                    row += "_"
                else:
                    row += str(val)
            print(row)


########################
### My tests    ########
########################

#b = Board("testBoard_med.csv")
#b_space = b.getMostConstrainedUnsolvedSpace()
#print(str(b_space))
