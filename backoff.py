import random

#단위는 마이크로세컨드 단위로 입력.
aSlotTime = 9
aSIFSTime = 16
aDIFSTime = aSIFSTime + (2 * aSlotTime)

def backoff(cwmin, cwmax):
    bkcounter = random.randint(cwmin, cwmax)
    return bkcounter * aSlotTime

def sifs():
    return aSIFSTime

def difs():
    return aDIFSTime