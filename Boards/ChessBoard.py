class ChessBoard:
    boardStart = [[-2, -3, -4, -5, -6, -4, -3, -2],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 3, 4, 5, 6, 4, 3, 2]]

    currBoard = [[-2, -3, -4, -5, -6, -4, -3, -2],
                 [-1, -1, -1, -1, -1, -1, -1, -1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, -2, 0, 0, 0],
                 [1, 1, 1, 1, 0, 1, 1, 1],
                 [2, 3, 4, 5, 6, 4, 3, 2]]

    kingLessBoard = []
    # 0 = white, 1 = black
    currPlayerMove = 0
    # white = pos
    # black = neg

    dirDict = {
        (0, 1): "east",
        (0, -1): "west",
        (1, 0): "south",
        (-1, 0): "north",
        (1, 1): "southeast",
        (-1, 1): "northeast",
        (1, -1): "southwest",
        (-1, -1): "northwest",
    }

    knightDirDict = {
        (-2, -1): "north1",
        (-2, 1): "north2",
        (2, -1): "south1",
        (2, 1): "south2",
        (1, 2): "east1",
        (-1, 2): "east2",
        (1, -2): "west1",
        (-1, -2): "west2",
    }

    pieceDict = {
        1: "pawn",
        2: "rook",
        3: "knight",
        4: "bishop",
        5: "queen",
        6: "king"
    }

    whiteKingSideCastle = 0
    whiteQueenSideCastle = 0
    blackKingSideCastle = 0
    blackQueenSideCastle = 0
    whiteCheck = 0
    blackCheck = 0
    whiteKingLoc = (0, 0)
    blackKingLoc = (0, 0)

    # TODO HANDLE Check and checkmate

    def getPiece(self, row, col):
        print(self.currBoard[row][col])

    def getKingLoc(self):
        for i in range(8):
            for j in range(8):
                if self.currBoard[i][j] == 6:
                    self.whiteKingLoc = (i, j)
                if self.currBoard[i][j] == -6:
                    self.blackKingLoc = (i, j)

    def checkLocCheck(self, x, y):
        kingLoc = (x, y)

        locCheckDictLoc = {
            "north": 0,
            "south": 0,
            "east": 0,
            "west": 0,
            "northeast": 0,
            "northwest": 0,
            "southeast": 0,
            "southwest": 0,
        }
        dirList = list(self.dirDict.keys())
        dirListCopy = dirList.copy()
        for i in range(8):
            for a in dirList:
                checkLoc = (kingLoc[0] + a[0] * (i + 1),
                            kingLoc[1] + a[1] * (i + 1))
                if checkLoc[0] >= 0 and checkLoc[1] >= 0:
                    try:
                        piece = self.currBoard[checkLoc[0]][checkLoc[1]]
                        if piece != 0:
                            addToDict = True
                            if self.currPlayerMove == 0 and piece == 6:
                                addToDict = False
                            if self.currPlayerMove == 1 and piece == -6:
                                addToDict = False
                            if addToDict:
                                locCheckDictLoc[self.dirDict[a]] = (
                                    piece, checkLoc)
                                dirListCopy.remove(a)
                    except IndexError:
                        dirListCopy.remove(a)
                else:
                    dirListCopy.remove(a)
            dirList = dirListCopy.copy()
            if len(dirList) == 0:
                break
        #print("Done Searching around king loc")

        check = False
        for a in locCheckDictLoc.items():
            try:
                # print(a)
                # print(a[1])
                hostile = False
                piece = a[1][0]
                pieceLoc = a[1][1]
                if self.currPlayerMove == 0 and piece < 0:
                    hostile = True
                elif self.currPlayerMove == 1 and piece > 0:
                    hostile = True

                if hostile:
                    pawnCheck = False
                    if self.currPlayerMove == 0 and piece == -1 and pieceLoc[0] == kingLoc[0] - 1:
                        pawnCheck = True
                    if self.currPlayerMove == 1 and piece == 1 and pieceLoc[0] == kingLoc[0] + 1:
                        pawnCheck = True
                    if len(a[0]) > 5 and ((abs(piece) == 4 or abs(piece) == 5) or pawnCheck):
                        check = True
                    elif len(a[0]) <= 5 and (abs(piece) == 2 or abs(piece) == 5):
                        check = True

            except TypeError:
                pass

        for a in self.knightDirDict.keys():
            checkLoc = (kingLoc[0] + a[0],
                        kingLoc[1] + a[1])
            if checkLoc[0] >= 0 and checkLoc[1] >= 0:
                try:
                    piece = self.currBoard[checkLoc[0]][checkLoc[1]]
                    if self.currPlayerMove == 0 and piece == -3:
                        check = True
                    elif self.currPlayerMove == 1 and piece == 3:
                        check = True

                except IndexError:
                    continue

        if self.currPlayerMove == 0 and kingLoc == self.whiteKingLoc:
            self.whiteCheck = int(check)
        elif self.currPlayerMove == 1 and kingLoc == self.blackKingLoc:
            self.blackCheck = int(check)
        else:
            return check

    def move(self, row1, col1, row2, col2):
        self.currBoard[row2][col2] = self.currBoard[row1][col1]
        self.currBoard[row1][col1] = 0
        self.currPlayerMove = (self.currPlayerMove + 1) % 2

    def inputPieceToMove(self):
        print("Pls Input Desired Row: ")
        row = int(input())
        print("Pls Input Desired Col: ")
        col = int(input())
        return self.checkCorrectTurnAndIfKingIsInCheck(row, col)

    def checkCorrectTurnAndIfKingIsInCheck(self, row, col):
        validMove = False
        if self.currBoard[row][col] != 0:
            if self.currBoard[row][col] > 0 and self.currPlayerMove == 0:
                validMove = True
            if self.currBoard[row][col] < 0 and self.currPlayerMove == 1:
                validMove = True
            if self.currPlayerMove == 0 and self.whiteCheck == 1 and self.currBoard[row][col] != 6:
                validMove = False
                print("King is in check.")
            if self.currPlayerMove == 1 and self.blackCheck == 1 and self.currBoard[row][col] != -6:
                validMove = False
                print("King is in check.")
        if validMove:
            return row, col
        else:
            return -1, -1

    def displayChoicesGetPick(self, row, col):
        pick = ""
        try:
            moveStr = self.getPossibleMoves(row, col)
            if moveStr != "":
                moves = moveStr.split(";")
                count = 0
                for a in moves:
                    values = a.split(",")
                    if len(values) > 1:
                        print(count, ") Row: ", values[0], " Col: ", values[1])
                    count = count + 1
                print("Please input your choice or q to cancel:")
                pick = input()
                if pick.lower() == "q":
                    return -1, -1
                values = moves[int(pick)].split(",")

                if self.currBoard[row][col] == 2 and col == 7:
                    self.whiteKingSideCastle = 1
                elif self.currBoard[row][col] == 2 and col == 0:
                    self.whiteQueenSideCastle = 1
                elif self.currBoard[row][col] == -2 and col == 7:
                    self.blackKingSideCastle = 1
                elif self.currBoard[row][col] == -2 and col == 7:
                    self.blackQueenSideCastle = 1

                if self.currBoard[row][col] == 6:
                    self.whiteKingSideCastle = 1
                    self.whiteQueenSideCastle = 1
                elif self.currBoard[row][col] == -6:
                    self.blackQueenSideCastle = 1
                    self.blackKingSideCastle = 1

                if abs(self.currBoard[row][col]) == 6 and int(values[1]) == col + 2:
                    if self.currBoard[row][col] > 0:
                        self.currBoard[7][5] = self.currBoard[7][7]
                        self.currBoard[7][7] = 0
                    else:
                        self.currBoard[0][5] = self.currBoard[0][7]
                        self.currBoard[0][7] = 0
                elif abs(self.currBoard[row][col] == 6) and int(values[1]) == col - 2:
                    if self.currBoard[row][col] > 0:
                        self.currBoard[7][3] = self.currBoard[7][0]
                        self.currBoard[7][0] = 0
                    else:
                        self.currBoard[0][3] = self.currBoard[0][0]
                        self.currBoard[0][0] = 0

                return int(values[0]), int(values[1])
            else:
                if abs(self.currBoard[row][col]) == 6:
                    return -99, -99
                print("No Valid Moves")
                return -1, -1
        except ValueError:
            print("Invalid Input: ", pick)
            return -1, -1

    def getPossibleMoves(self, row, col):
        piece = self.currBoard[row][col]
        # print("Loc: ", row, ',', col)
        retVal = ""
        if piece == 0:
            print("Invalid Location No Piece Found Dumbass")
        else:
            if piece == 1 or piece == -1:
                # print("Found Pawn")
                retVal = self.pawnMoves(row, col, piece)
            elif piece == 2 or piece == -2:
                # print("Found Rook")
                retVal = self.rookMoves(row, col, piece)
            elif piece == 3 or piece == -3:
                # print("Found Knight")
                retVal = self.knightMoves(row, col, piece)
            elif piece == 4 or piece == -4:
                # print("Found Bishop")
                retVal = self.bishopMoves(row, col, piece)
            elif piece == 5 or piece == -5:
                # print("Found Queen")
                retVal = self.queenMoves(row, col, piece)
            elif piece == 6 or piece == -6:
                # print("Found King")
                retVal = self.kingMoves(row, col, piece)
        return retVal

    def getAllPossibleMoves(self):
        moveSet = []
        if self.currPlayerMove == 0:
            for i in range(8):
                for j in range(8):
                    if self.currBoard[i][j] > 0:
                        if len(self.getPossibleMoves(i, j)) > 0:
                            print(self.pieceDict[self.currBoard[i][j]], " : ", i,
                                  ",", j, " moves:\n", self.getPossibleMoves(i, j))
                            for a in self.getPossibleMoves(i, j).split(";"):
                                a = a.strip()
                                if len(a) > 1:
                                    moveRow = int(a[0])
                                    moveCol = int(a[2])
                                    element = (
                                        self.pieceDict[self.currBoard[i][j]], ((i, j), (moveRow, moveCol)))
                                    moveSet.append(element)
        else:
            for i in range(8):
                for j in range(8):
                    if self.currBoard[i][j] < 0:
                        if len(self.getPossibleMoves(i, j)) > 0:
                            print(self.pieceDict[abs(self.currBoard[i][j])], " : ", i,
                                  ",", j, " moves:\n", self.getPossibleMoves(i, j))
                            for a in self.getPossibleMoves(i, j).split(";"):
                                a = a.strip()
                                if len(a) > 1:
                                    moveRow = int(a[0])
                                    moveCol = int(a[2])
                                    element = (
                                        self.pieceDict[self.currBoard[i][j]], ((i, j), (moveRow, moveCol)))
                                    moveSet.append(element)
        return moveSet

    def isEnemy(self, piece1, piece2):
        if piece1 == 0 or piece2 == 0:
            return False
        if piece2/abs(piece2) == piece1/abs(piece1):
            return False
        return True

    def checkValidMove(self, row, col, piece, overtake):
        pieceAtLoc = self.currBoard[row][col]
        # nothing at loc then valid move
        # same piece at loc not valid move
        # move that can eat other piece and enemy at loc then valid
        # move that can't eat and enemy at loc then not valid
        if abs(piece) == 1:
            if overtake:
                if self.isEnemy(piece, pieceAtLoc):
                    return 1
                return 0
            else:
                if pieceAtLoc == 0:
                    return 1
                return 0
        if abs(piece) == 2:
            if self.isEnemy(piece, pieceAtLoc):
                return 2
            elif pieceAtLoc == 0:
                return 1
            else:
                return 0
        if abs(piece) == 3:
            if pieceAtLoc == 0 or self.isEnemy(piece, pieceAtLoc):
                return 1
            else:
                return 0
        if abs(piece) == 4:
            if self.isEnemy(piece, pieceAtLoc):
                return 2
            elif pieceAtLoc == 0:
                return 1
            else:
                return 0
        if abs(piece) == 5:
            if self.isEnemy(piece, pieceAtLoc):
                return 2
            elif pieceAtLoc == 0:
                return 1
            else:
                return 0
        if abs(piece) == 6:
            if pieceAtLoc == 0 or self.isEnemy(piece, pieceAtLoc):
                return 1
            else:
                return 0

    def pawnMoves(self, row, col, piece):
        moves = ""
        if piece == 1:
            if col + 1 <= 7 and self.checkValidMove(row - 1, col + 1, piece, True) == 1:
                moves += str(row - 1) + ',' + str(col + 1) + "; "
            if col - 1 >= 0 and self.checkValidMove(row - 1, col - 1, piece, True) == 1:
                moves += str(row - 1) + ',' + str(col - 1) + "; "
            if self.checkValidMove(row - 1, col, piece, False) == 1:
                moves += str(row - 1) + ',' + str(col) + "; "
                if row == 6 and self.checkValidMove(row - 2, col, piece, False) == 1:
                    moves += str(row - 2) + ',' + str(col) + "; "
        else:
            if col + 1 <= 7 and self.checkValidMove(row + 1, col + 1, piece, True):
                moves += str(row + 1) + ',' + str(col + 1) + "; "
            if col - 1 >= 0 and self.checkValidMove(row + 1, col - 1, piece, True):
                moves += str(row + 1) + ',' + str(col - 1) + "; "
            if self.checkValidMove(row + 1, col, piece, False):
                moves += str(row + 1) + ',' + str(col) + "; "
                if row == 1 and self.checkValidMove(row + 2, col, piece, False):
                    moves += str(row + 2) + ',' + str(col) + "; "
        return moves

    def rookMoves(self, row, col, piece):
        moves = ""
        # up
        for a in range(1, 8):
            if row - a >= 0 and self.checkValidMove(row - a, col, piece, True) != 0:
                moves += str(row - a) + ',' + str(col) + "; "
                if self.checkValidMove(row - a, col, piece, True) == 2:
                    break
            else:
                break
        # down
        for a in range(1, 8):
            if row + a <= 7 and self.checkValidMove(row + a, col, piece, True) != 0:
                moves += str(row + a) + ',' + str(col) + "; "
                if self.checkValidMove(row + a, col, piece, True) == 2:
                    break
            else:
                break
        # left
        for a in range(1, 8):
            if col - a >= 0 and self.checkValidMove(row, col - a, piece, True) != 0:
                moves += str(row) + ',' + str(col - a) + "; "
                if self.checkValidMove(row, col - a, piece, True) == 2:
                    break
            else:
                break
        # right
        for a in range(1, 8):
            if col + a <= 7 and self.checkValidMove(row, col + a, piece, True) != 0:
                moves += str(row) + ',' + str(col + a) + "; "
                if self.checkValidMove(row, col + a, piece, True) == 2:
                    break
            else:
                break
        return moves

    def knightMoves(self, row, col, piece):
        moves = ""
        if row - 1 >= 0 and col - 2 >= 0 and self.checkValidMove(row - 1, col - 2, piece, True):
            moves += str(row - 1) + ',' + str(col - 2) + "; "
        if row - 1 >= 0 and col + 2 <= 7 and self.checkValidMove(row - 1, col + 2, piece, True):
            moves += str(row - 1) + ',' + str(col + 2) + "; "
        if row + 1 <= 7 and col - 2 >= 0 and self.checkValidMove(row + 1, col - 2, piece, True):
            moves += str(row + 1) + ',' + str(col - 2) + "; "
        if row + 1 <= 7 and col + 2 <= 7 and self.checkValidMove(row + 1, col + 2, piece, True):
            moves += str(row + 1) + ',' + str(col + 2) + "; "
        if row - 2 >= 0 and col - 1 >= 0 and self.checkValidMove(row - 2, col - 1, piece, True):
            moves += str(row - 2) + ',' + str(col - 1) + "; "
        if row - 2 >= 0 and col + 1 <= 7 and self.checkValidMove(row - 2, col + 1, piece, True):
            moves += str(row - 2) + ',' + str(col + 1) + "; "
        if row + 2 <= 7 and col - 1 >= 0 and self.checkValidMove(row + 2, col - 1, piece, True):
            moves += str(row + 2) + ',' + str(col - 1) + "; "
        if row + 2 <= 7 and col + 1 <= 7 and self.checkValidMove(row + 2, col + 1, piece, True):
            moves += str(row + 2) + ',' + str(col + 1) + "; "
        return moves

    def bishopMoves(self, row, col, piece):
        moves = ""
        # up left
        for a in range(1, 8):
            if row - a >= 0 and col - a >= 0 and self.checkValidMove(row - a, col - a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row - a, col - a, piece, True) == 2:
                    break
            else:
                break

        # up right
        for a in range(1, 8):
            if row - a >= 0 and col + a <= 7 and self.checkValidMove(row - a, col + a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row - a, col + a, piece, True) == 2:
                    break
            else:
                break

        # down left
        for a in range(1, 8):
            if row + a <= 7 and col - a >= 0 and self.checkValidMove(row + a, col - a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row + a, col - a, piece, True) == 2:
                    break
            else:
                break

        # down right
        for a in range(1, 8):
            if row + a <= 7 and col + a <= 7 and self.checkValidMove(row + a, col + a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row + a, col + a, piece, True) == 2:
                    break
            else:
                break

        return moves

    def queenMoves(self, row, col, piece):
        moves = ""
        # up left
        for a in range(1, 8):
            if row - a >= 0 and col - a >= 0 and self.checkValidMove(row - a, col - a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row - a, col - a, piece, True) == 2:
                    break
            else:
                break

        # up right
        for a in range(1, 8):
            if row - a >= 0 and col + a <= 7 and self.checkValidMove(row - a, col + a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row - a, col + a, piece, True) == 2:
                    break
            else:
                break

        # down left
        for a in range(1, 8):
            if row + a <= 7 and col - a >= 0 and self.checkValidMove(row + a, col - a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row + a, col - a, piece, True) == 2:
                    break
            else:
                break

        # down right
        for a in range(1, 8):
            if row + a <= 7 and col + a <= 7 and self.checkValidMove(row + a, col + a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row + a, col + a, piece, True) == 2:
                    break
            else:
                break

        # up
        for a in range(1, 8):
            if row - a >= 0 and self.checkValidMove(row - a, col, piece, True) != 0:
                moves += str(row - a) + ',' + str(col) + "; "
                if self.checkValidMove(row - a, col, piece, True) == 2:
                    break
            else:
                break
        # down
        for a in range(1, 8):
            if row + a <= 7 and self.checkValidMove(row + a, col, piece, True) != 0:
                moves += str(row + a) + ',' + str(col) + "; "
                if self.checkValidMove(row + a, col, piece, True) == 2:
                    break
            else:
                break
        # left
        for a in range(1, 8):
            if col - a >= 0 and self.checkValidMove(row, col - a, piece, True) != 0:
                moves += str(row) + ',' + str(col - a) + "; "
                if self.checkValidMove(row, col - a, piece, True) == 2:
                    break
            else:
                break
        # right
        for a in range(1, 8):
            if col + a <= 7 and self.checkValidMove(row, col + a, piece, True) != 0:
                moves += str(row) + ',' + str(col + a) + "; "
                if self.checkValidMove(row, col + a, piece, True) == 2:
                    break
            else:
                break
        return moves

    def castleCheck(self, row, col, side, piece):
        if piece > 0 and side == "king" and self.currBoard[row][col + 1] == 0 and self.currBoard[row][col + 2] == 0:
            return True
        elif piece > 0 and side == "queen" and self.currBoard[row][col - 1] == 0 and self.currBoard[row][col - 2] == 0 and self.currBoard[row][col - 3] == 0:
            return True
        elif piece < 0 and side == "king" and self.currBoard[row][col + 1] == 0 and self.currBoard[row][col + 2] == 0:
            return True
        elif piece < 0 and side == "queen" and self.currBoard[row][col - 1] == 0 and self.currBoard[row][col - 2] == 0 and self.currBoard[row][col - 3] == 0:
            return True
        else:
            return False

    def kingMoves(self, row, col, piece):
        moves = ""
        if piece > 0 and self.whiteKingSideCastle == 0 and self.castleCheck(row, col, "king", piece):
            moves += str(row) + ',' + str(col + 2) + "; "
        if piece > 0 and self.whiteQueenSideCastle == 0 and self.castleCheck(row, col, "queen", piece):
            moves += str(row) + ',' + str(col - 2) + "; "
        if piece < 0 and self.blackKingSideCastle == 0 and self.castleCheck(row, col, "king", piece):
            moves += str(row) + ',' + str(col + 2) + "; "
        if piece < 0 and self.blackQueenSideCastle == 0 and self.castleCheck(row, col, "queen", piece):
            moves += str(row) + ',' + str(col - 2) + "; "
        if col + 1 <= 7 and self.checkValidMove(row, col + 1, piece, True) != 0 and not self.checkLocCheck(row, col+1):
            moves += str(row) + ',' + str(col + 1) + "; "
        if col - 1 >= 0 and self.checkValidMove(row, col - 1, piece, True) != 0 and not self.checkLocCheck(row, col-1):
            moves += str(row) + ',' + str(col - 1) + "; "
        if row + 1 <= 7 and self.checkValidMove(row + 1, col, piece, True) != 0 and not self.checkLocCheck(row+1, col):
            moves += str(row + 1) + ',' + str(col) + "; "
        if row - 1 >= 0 and self.checkValidMove(row - 1, col, piece, True) != 0 and not self.checkLocCheck(row-1, col):
            moves += str(row - 1) + ',' + str(col) + "; "
        if row + 1 <= 7 and col + 1 <= 7 and self.checkValidMove(row + 1, col + 1, piece, True) != 0 and not self.checkLocCheck(row+1, col+1):
            moves += str(row + 1) + ',' + str(col + 1) + "; "
        if row + 1 <= 7 and col - 1 >= 0 and self.checkValidMove(row + 1, col - 1, piece, True) != 0 and not self.checkLocCheck(row+1, col-1):
            moves += str(row + 1) + ',' + str(col - 1) + "; "
        if row - 1 >= 0 and col + 1 <= 7 and self.checkValidMove(row - 1, col + 1, piece, True) != 0 and not self.checkLocCheck(row-1, col+1):
            moves += str(row - 1) + ',' + str(col + 1) + "; "
        if row - 1 >= 0 and col - 1 >= 0 and self.checkValidMove(row - 1, col - 1, piece, True) != 0 and not self.checkLocCheck(row-1, col-1):
            moves += str(row - 1) + ',' + str(col - 1) + "; "
        return moves

    def printBoard(self):
        print()
        print("        0    1    2    3     4    5    6    7      Col ")
        print("      -----------------------------------------")
        count = 0
        for col in self.currBoard:
            print(" ", str(count), "  |", end='')
            for row in col:
                if row >= 0:
                    print(" ", row, "|", end='')
                else:
                    print("-", -1*row, "|", end='')
            print()
            print("      -----------------------------------------")
            count = count + 1
        print()
        print(" Row")
        print()
        print()
        print()
