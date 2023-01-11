class State:
    '''
    The State class represents one state of the TicTacToe game. 
    member variables:
        board - a 2d array filled with chars representing the game board 
        move - a tuple that represents where the most recent char was placed
        p1 and p2 - the two players playing the game
        curPlayer - the player who is going to take their turn next, either p1 or p2
        isWinner - a tuple with a boolean and index 0, True if  the board has a winner 
                   or False if there is no winner, and at index 1 either the winning 
                   player or None if there is no winner 
        value - 1 if p2 is the winner -1 if p1 is ther winner or 0 if there are no winners
        next - an array contaning the possible next states. next is None if the class is
               instanciated by itself, the array is created in StateTree.
    method:
        isFull() - returns True if the board is full, False otherwise 
    '''
    def __init__(self, board, p1, p2, curPlayer, move=None):
        self.move = move
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.curPlayer = curPlayer
        self.isWinner = isWinner(board, p1, p2)

        if self.isWinner[1] is p1:
            self.value = -1
        elif self.isWinner[1] is p2:
            self.value = 1
        else:
            self.value = 0

        self.next = None

    def isFull(self):
        for row in self.board:
            for symbol in row:
                if symbol == " ":
                    return False
        return True
    
class StateTree:
    '''
    The StateTree class creates a tree of all possible game states
    member variables:
        firstState - the first state passed at instantiation
        curState - used to keep tack of the game state as moves are made by 
                   each player
        p1 and p2 - the two players playing the game
    methods:
        updateCurState(move) - given move, a tuple with the players move in 
                               the form (row, column), changed curState to the 
                               apropriate state retursn a bool, True if the variable
                               was correctly updated and False otherwise. returns
                               None if curState.next is None
        getBestMove() - gets the best move possible at curState. returns the value
                        of the best move and the index of that move in state.next
        reset() - changes curState to the firstState
        _setNext() - a private method called in the constructor that gets all of 
                     the possible next states and puts them in the states .next field
        _getPossibleNext(state) - given a state returns an array of tuples containing 
                                  possible moves (row, column). This method is private 
                                  and is called in _setNext()

    '''
    def __init__(self, firstState):
        self.firstState = firstState
        self.curState = firstState
        self.p1 = firstState.p1
        self.p2 = firstState.p2
    
        self._setNext()

    def updateCurState(self, move):
        if self.curState.next is None:
            return None

        for state in self.curState.next:
            if state.move == move:
                self.curState = state
                return True
        
        return False

    def getBestMove(self, state=None, depth=0, isMaximizer=True):
        # for the initial call
        if state is None:
            state = self.curState

        # base case
        if state.isWinner[0] or state.next is None:
            return state.value*(9-depth), -1
        
        else:
            # gets the max value of a move if it is the AI's turn
            if isMaximizer:
                maxVal = -1000
                index = 0
                indexOfMove = 0
                for nextState in state.next:
                    value, indx = self.getBestMove(nextState, depth+1, not isMaximizer)
                    # a new maxVal is found
                    if value > maxVal:
                        maxVal = value
                        indexOfMove = index
                    index += 1
                return maxVal, indexOfMove
            # gets the min value of a move if its the player's turn
            else:
                minVal = 1000
                index = 0
                indexOfMove = 0
                for nextState in state.next:
                    value, indx = self.getBestMove(nextState, depth+1, not isMaximizer)
                    # a new minValue is found
                    if value < minVal:
                        minVal = value
                        indexOfMove = index
                    index += 1
                return minVal, indexOfMove
    
    def reset(self):
        self.curState = self.firstState
        return self.curState

    def _setNext(self, state=None):
        nextStateBoards = []
        if state is None:
            state = self.firstState
            settingFirst = True
        else:
            settingFirst = False
        
        possibleCoordinates = self._getPossibleNext(state)
        # no possible next board
        if possibleCoordinates == [] or state.isWinner[0]:
            state.next = None
            return
        # creates unique boards for each possible move
        for coordinate in possibleCoordinates:
            board = generateBoard(state.board, coordinate, state.curPlayer)
            nextStateBoards.append(board)
        
        # updates curPlayer
        if state.curPlayer is self.p1:
            cp = self.p2
        else:
            cp = self.p1

        # creates the states .next array and fills it with next states
        state.next = []
        i = 0
        for board in nextStateBoards:
            state.next.append(State(board, self.p1, self.p2, cp, possibleCoordinates[i]))
            i += 1
        
        # recursive call that sets the next states for each state in the current
        # states .next field
        for st in state.next:
            self._setNext(st)
        
        # ensures firstState is set to the correct state
        if settingFirst:
            self.firstState = state

        return

    def _getPossibleNext(self, state):
        retVal = []
        row = 0
        for spaceArr in state.board:
            col = 0
            for space in spaceArr:
                if space == " ":
                    retVal.append((row, col))
                col += 1
            row += 1
        return retVal

class Player():
    '''
    The Player class represents one player in the tic tac toe game
    member variables:
        symbol - the character that the player uses to take their turn 
        name - the name of the player
        numWins - the number of wins the player has
    methods:
        addWin() - increments numWins by 1
    '''
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.numWins = 0
    
    def addWin(self):
        self.numWins += 1

def generateBoard(previousBoard, coordinate, curPlayer):
    ''' 
    this method creates a new board given a previous board (previousBoard)
    the move that the player chose in the form (row, column) (coordinate)
    and the player that made the move (curPlayer)
    '''
    board = [[],[],[]]
    i = 0
    for row in previousBoard:
        j = 0
        for space in row:
            if (i,j) == coordinate:
                board[i].append(curPlayer.symbol)
            else:
                board[i].append(space)
            j += 1
        i += 1
        j = 0

    return board

def isWinner(board, p1, p2):
    '''
    returns a boolean, True if there is a winner and False otherwise, and 
    either the player who won or None if there is no winner
    '''
    p1Win = [p1.symbol, p1.symbol, p1.symbol]
    p2Win = [p2.symbol, p2.symbol, p2.symbol]

    toCheckHorizontal = []
    toCheckVertical = [[], [], []]
    toCheckDiagonal = [[], []]

    rowIndx = 0
    colIndx = 0
    for symbol_array in board:
        # chekcs for a win along the columns
        toCheckHorizontal = symbol_array
        if (toCheckHorizontal == p1Win):
            return True, p1
        elif (toCheckHorizontal == p2Win):
            return True, p2
        for symbol in symbol_array:
            # gets the three rows on the board to check later
            toCheckVertical[rowIndx].append(symbol)

            # gets the two diagonlas to cehck later
            if (rowIndx, colIndx) == (0,0): # top left
                toCheckDiagonal[0].append(symbol)
            elif (rowIndx, colIndx) == (2,0): # top right
                toCheckDiagonal[1].append(symbol)
            elif (rowIndx, colIndx) == (1,1): # middle
                toCheckDiagonal[0].append(symbol)
                toCheckDiagonal[1].append(symbol)
            elif (rowIndx, colIndx) == (2,2): # bottom right
                toCheckDiagonal[0].append(symbol)
            elif (rowIndx, colIndx) == (0,2): # bottom left
                toCheckDiagonal[1].append(symbol)

            rowIndx += 1
        colIndx += 1
        rowIndx = 0

    # checks for vertical win
    for inARow in toCheckVertical:
        if (inARow == p1Win):
            return True, p1
        elif (inARow == p2Win):
            return True, p2
    
    # checks for diagonal win
    for inARowV in toCheckDiagonal:
        if (inARowV == p1Win):
            return True, p1
        elif (inARowV == p2Win):
            return True, p2

    # no winners found
    return False, None