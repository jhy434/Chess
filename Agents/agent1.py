import random

from Evaluators.evaluator import Evaluator


class Agent1:
    color = 0

    pieceDict = {
        "pawn": 1,
        "rook": 2,
        "knight": 3,
        "bishop": 4,
        "queen": 5,
        "king": 6
    }

    def pickMove(self, moveList):
        choice = 0
        maxValue = 0
        maxValueList = []
        count = 0
        for a in moveList:
            score = Evaluator.pieceValueScore(
                self.pieceDict[a[0]], a[1][0][0], a[1][0][1], a[1][1][0], a[1][1][1])
            if score > maxValue:
                maxValueList = [count]
            elif score == maxValue:
                maxValueList.append(count)
            count = count + 1
        if len(maxValueList) > 1:
            index = random.randint(0, len(maxValueList) - 1)
            choice = maxValueList[index]
        else:
            choice = maxValueList[0]
        print("PickMove Agent1: ", moveList[choice])
        return choice
