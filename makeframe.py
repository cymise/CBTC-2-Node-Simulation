#calcduration은 바이트를 받아, 실제 시간으로 프레임 duration을 계산한다. 이후, 그것을 timestep으로 바꾼다.

tx_endtime = 0
isbreaked = False
txseq = 0 #전송 시퀀스를 구분함. 프레임 전송이 성공할 때마다 1씩 증가.
istxing = False #현재 전송중인지 표시하는 변수. 전송중이면 True이다.

def calcduration(byte):
    return 0

#def calc_eb_n0(signal, noise, bw):
    #시그널과 노이즈는 모두 dBm 단위로 주어져야함.
    

def framecheck():
    #아직은 프레임이 제대로 도착했는지 확인할 수 있는 알고리즘을 모르기 때문에, 일단은 False로 넘김.
    #프레임 체크를 위한 변수 1. 수신전력, 2. MCS, 3. 노이즈
    #필요한 알고리즘은 논문을 찾아서 채우기. + 기존 매트랩 무선랜 시뮬레이션 해석?
    return False

    #True = 프레임 깨짐!

def makeframe(byte, now):#외에 Duration 계산을 위한 정보가 들어가야 함!
    global tx_endtime
    global istxing
    istxing = True
    tx_endtime = calcduration(byte) + now
    return

def txframe(now): #now 외에 채널을 확인할 수 있는 정보가 들어가야함!
    global isbreaked
    global txseq
    global istxing

    if isbreaked == False: #프레임이 아직 깨지지 않았다면, 매 타임스탬프마다 프레임 확인.
        isbreaked = framecheck()

    if tx_endtime <= now: #아직 전송이 완료되지 않음.
        return 0
    elif isbreaked == False: #프레임이 정상적으로 전송됨.
        txseq += 1
        istxing = False
        return 1
    elif isbreaked == True: #프레임이 정상적으로 전송되지 않음.
        istxing = False
        return 2