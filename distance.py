import math

#절댓값 거리 반환. p1 및 p2 는 각각 (x, y 좌표로 되어있는 튜플로 받음.) 
def calcdistance(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]

    x = math.pow(x, 2)
    y = math.pow(y, 2)

    return abs(math.sqrt(x+y))