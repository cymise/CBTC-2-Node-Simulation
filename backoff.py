import random

#단위는 마이크로세컨드 단위로 입력.
aSlotTime = 9
aSIFSTime = 16
aDIFSTime = aSIFSTime + (2 * aSlotTime)

#2의 제곱 단위로 나타냄 (e.g. cwmin = 2^4)
cwmin = 4
cwmax = 10

iswaiting = False #initial
endtime = 0 #initial

def backoff(rtrycount, now):
    global iswaiting
    global endtime

    if rtrycount == 0:
        cw = 2^cwmin - 1
    else:
        pow = (cwmin+rtrycount)
        if pow > cwmax:
            pow = cwmax
        cw = 2^pow - 1
    
    bkcounter = random.randint(0, cw)
    iswaiting = True
    endtime = now + (bkcounter * aSlotTime)
    return

def sifs(now):
    global iswaiting
    global endtime

    iswaiting = True
    endtime = now + aSIFSTime
    return

def difs(now):
    global iswaiting
    global endtime

    iswaiting = True
    endtime = now + aDIFSTime
    return

def waiting(now):
    global iswaiting
    global endtime
    
    if endtime <= now: #아직 백오프 또는 ifs가 끝나지 않음
        return 0
    else:
        iswaiting = False #대기 끝
        return 1

