from StateTree import *
def printBoard(board):
    '''
    prints the game board to the terminal given a 2d array of characters
    representing the game board
    '''
    j = 0
    for symArr in board:
        i = 0
        for sym in symArr:
            print(sym, end = '')
            if i != 2:
                print("|", end = '')
            i += 1
        if j != 2:
            print("\n-----")
        else:
            print()
        j += 1

def game():
    print("running...")
    #          0    1    2
    board = [[" ", " ", " "], # 0
             [" ", " ", " "], # 1
             [" ", " ", " "]] # 2
    p1 = Player("X", "Human Player")
    p2 = Player("O", "AI Player")
    curPlayer = p1
    gameStateTree = None

    print(f"{curPlayer.name} starts as {curPlayer.symbol}")

    depth = 0
    playing = True
    while playing:
        if gameStateTree is None:
            gameStateTree = StateTree(State(board, p1, p2, curPlayer))
            curState = gameStateTree.firstState
        
        # get user input, loop continues untuil a valid input is given
        while True:
            printBoard(board)
            if curPlayer is p1: # human player
                move = input('Enter move as "row, col": ')
                move = move.split(',')
            else: # computer player
                move = gameStateTree.getBestMove()
                # gets the index of the intended move in curState.next
                move = move[1]
                # gets the move in the form (row, col)
                move = curState.next[move].move
            
            # validate user input
            try:
                row = int(move[0])
                col = int(move[1])
            except:
                print("There seems to be something wrong with your input. Try again.")
                continue
            if row > 2 or col > 2:
                print("There seems to be something wrong with your input. Try again.")
                continue
            elif row < 0 or col < 0:
                print("There seems to be something wrong with your input. Try again.")
                continue
            print(f"move (row,col): ({row}, {col})")
            
            # makes the move the player wants or tells the user the spot is taken
            if (board[row][col] == " "):
                board[row][col] = curPlayer.symbol
                if gameStateTree is not None:
                    for state in curState.next:
                        if board == state.board:
                            curState = state
                
                if gameStateTree is not None:
                    gameStateTree.updateCurState(curState.move)
                break
            else:
                print("Pick again, that spot is taken.") 
        depth += 1

        # checks for the end of the game 
        isWin, winningPlayer = isWinner(board, p1, p2)
        isFull = gameStateTree.curState.isFull()

        # if the end of the game is reached
        if isWin or isFull:
            if winningPlayer is not None:
                print(f"Winner is {winningPlayer.name} as the symbol {winningPlayer.symbol}.")
            else:
                print("There was a tie.")
            printBoard(board)

            # tracks number of wins
            if winningPlayer is p1:
                    p1.addWin()
            elif winningPlayer is p2:
                p2.addWin()

            # asks the user if they would like to play again
            keepPlaying = input("do you want to keep playing? (y/n):")[0]

            # reset the game if the player wants to keep playing
            if keepPlaying == "y":
                print("resetting the game...")
                
                playing = True
                board = [[" ", " ", " "], 
                         [" ", " ", " "], 
                         [" ", " ", " "]]
                
                curPlayer = p1
                curState = gameStateTree.reset()
            # prints each players wins if the user is done playing
            else:
                print(f"{p1.name} had {p1.numWins} win(s).")
                print(f"{p2.name} had {p2.numWins} win(s).")
                break
        # updates the current player if the game is still going
        else:
            if curPlayer is p1:
                curPlayer = p2
            else:
                curPlayer = p1    

game()


