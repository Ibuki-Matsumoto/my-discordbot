import random


def diceroll(cnt, maxe):
    total = 0
    num_list = []
    for i in range(0, cnt):
        num = random.randint(1, maxe)
        num_list.append(num)

    total = sum(num_list)
    num_list.append(total)
    return num_list

