from ChessBoard import ChessBoard
from ChessBoardAuto import ChessBoardAuto
from agent1 import Agent1
from agent2 import Agent2


def playGame(board):
    board.printBoard()
    board.getKingLoc()

    if board.currPlayerMove == 0:
        print("White Move")
        board.checkLocCheck(board.whiteKingLoc[0], board.whiteKingLoc[1])
    else:
        print("Black Move")
        board.checkLocCheck(board.blackKingLoc[0], board.blackKingLoc[1])

    row1, col1 = board.inputPieceToMove()
    if row1 != -1:
        row2, col2 = board.displayChoicesGetPick(row1, col1)
        if row2 == -99:
            color = ""
            if board.currPlayerMove == 0:
                color = "Black"
            else:
                color = "White"
            print("\n--------------------------------------------------------")
            print("Good Game ", color, " Won!!!!!!!!!!!!!!")
            print("--------------------------------------------------------\n")
        elif row2 != -1:
            board.move(row1, col1, row2, col2)
            board.printBoard()
    else:
        print("ERROR Wrong piece selected")


def playAuto(board):
    AgentOne = Agent1()
    AgentTwo = Agent2()
    moves = 0
    gameOver = False
    while moves < 500 and not gameOver:
        moves = moves + 1
        if board.currPlayerMove == 0:
            moveList = board.getAllPossibleMoves()
            if moveList == -1 or len(moveList) == 0:
                print("Good Game, Agent Two, black won")
                board.printBoard()
                break
            else:
                moveIndex = AgentOne.pickMove(moveList)
                move = moveList[moveIndex]
                movePieceLoc = move[1][0]
                movePieceToLoc = move[1][1]
                board.move(movePieceLoc[0], movePieceLoc[1],
                           movePieceToLoc[0], movePieceToLoc[1])
                board.printBoard()
        else:
            moveList = board.getAllPossibleMoves()
            if moveList == -1 or len(moveList) == 0:
                print("Good Game, Agent One, white won")
                board.printBoard()
                break
            else:
                moveIndex = AgentTwo.pickMove(moveList)
                move = moveList[moveIndex]
                movePieceLoc = move[1][0]
                movePieceToLoc = move[1][1]
                board.move(movePieceLoc[0], movePieceLoc[1],
                           movePieceToLoc[0], movePieceToLoc[1])
                board.printBoard()
        gameOver = not board.checkBoardForKings()


def main():
    boardManual = ChessBoard()
    boardAuto = ChessBoardAuto()
    loop = True
    while loop:
        print()
        print('Type a Number and Press Enter:')
        print('1: Make Move Manually')
        print('2: Make Move Automatically')
        print('3: Get All Moves')
        print('4: test')
        print('6: Quit')

        result = input()
        if result == '1':
            playGame(boardManual)
        elif result == '2':
            playAuto(boardAuto)
        elif result == '3':
            boardAuto.getAllPossibleMoves()
        elif result == '4':
            boardAuto.printBoard()
            check = boardAuto.checkLocCheck(4, 2)
            print(check)
        else:
            print("Quitting")
            loop = False


if __name__ == "__main__":
    main()
