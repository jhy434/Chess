import random


class Agent2:
    color = 0

    def pickMove(self, moveList):
        index = random.randint(0, len(moveList) - 1)
        print("PickMove Agent2: ", moveList[index])
        return index
