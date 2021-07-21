import random

#단위는 마이크로세컨드 단위로 입력.
aSlotTime = 9
aSIFSTime = 16
aDIFSTime = aSIFSTime + (2 * aSlotTime)

#2의 제곱 단위로 나타냄 (e.g. cwmin = 2^4)
cwmin = 4
cwmax = 10


def backoff(rtrycount):

    if rtrycount == 0:
        cw = 2^cwmin - 1
    else:
        pow = (cwmin+rtrycount)
        if pow > cwmax:
            pow = cwmax
        cw = 2^pow - 1
    
    bkcounter = random.randint(0, cw)
    return bkcounter * aSlotTime


