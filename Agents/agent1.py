import random


class Agent1:
    color = 0

    def pickMove(self, moveList):
        index = random.randint(0, len(moveList) - 1)
        print("PickMove: ", moveList[index])
        return index
