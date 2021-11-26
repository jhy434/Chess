class Evaluator:
    def pieceValueScore(piece, row1, col1, row2, col2):
        if piece == 1 and row1 == 1:
            return abs(piece) * 100
        if piece == -1 and row1 == 6:
            return abs(piece) * 100
        if abs(piece) == 1:
            return abs(piece)
        if abs(piece) == 2:
            return abs(piece)
        if abs(piece) == 3:
            return abs(piece)
        if abs(piece) == 4:
            return abs(piece)
        if abs(piece) == 5:
            return abs(piece)
        if abs(piece) == 6:
            return abs(piece)/abs(piece)
        return piece

    def score(self):
        return 0
