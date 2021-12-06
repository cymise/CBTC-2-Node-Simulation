import math
import random
import ReadEngine

#calcduration은 바이트를 받아, 실제 시간으로 프레임 duration을 계산한다. 이후, 그것을 timestep으로 바꾼다.
GI = 0.8 #가드 인터벌, 마이크로세컨드 단위
SYMBOLTIME = 12.8 #심볼 타임, 마이크로세컨드 단위
STREAM = 2 #spatial stream 수
SUBCARRIERS = 996 #HE SU 80MHz일 때, 최대 996심볼

PRE_LEGACY = 20 #레거시 프리앰블, 마이크로세컨드 단위
PRE_HE_1 = 16 # HE-LTF를 제외한 프리앰블, 마이크로세컨드 단위
PRE_HE_LTF = 4 * STREAM # HE-LTF, 마이크로세컨드 단위. 공간스트림에 따라 자동으로 계산.

per_list_dir = "./snr-per/"
per_list = ["0-400", "0-14", "0-1000","1-400", "1-14", "1-1000","2-400", "2-14", "2-1000"] #mcs-bytes
per_table = {}
ap_snr = []
timestep_mantissa = 1
timestep = timestep_mantissa * math.pow(10, -6)


def txframe(bytes, mcs, step): #now 외에 채널을 확인할 수 있는 정보가 들어가야함!
    time = calcduration(bytes, mcs)
    tx_step = convert_to_step(time)
    snr = 0

    try:
        for i in range(step, step + tx_step):
            snr = snr + ap_snr[i]
        snr = snr/tx_step #전송 기간동안 SNR의 평균을 구함
    except:
        snr = ap_snr[step]
    
    per = snr_to_per(bytes, mcs, snr)
    result = random.choices((True, False), weights = (1 - per, per))[0]
    return result, tx_step, per
    #randaa = random.choices((True, False), weights = (1, 1))[0]
    #return randaa, 400, 0.5

#def check_result():

def calcduration(bytes, mcs):
    bps, cod = mcs_interpret(mcs)
    bits = bytes * 8
    spd = 996 * bps * cod * STREAM
    symbols = math.ceil(bits / spd)
    mpdu_airtime = math.ceil(symbols / (GI+SYMBOLTIME))
    duration = PRE_LEGACY + PRE_HE_1 + PRE_HE_LTF + mpdu_airtime

    return duration


def mcs_interpret(mcs):
    #bps = bit(s) per symbol
    #cod = coding rate
    if mcs == 0:
        bps = 1
        cod = 0.5
    elif mcs == 1:
        bps = 2
        cod = 0.5
    elif mcs == 2:
        bps = 2
        cod = 0.75
    elif mcs == 3:
        bps = 4
        cod = 0.5
    elif mcs == 4:
        bps = 4
        cod = 0.75
    elif mcs == 5:
        bps = 6
        cod = 0.67
    elif mcs == 6:
        bps = 6
        cod = 0.75
    elif mcs == 7:
        bps = 6
        cod = 0.83
    elif mcs == 8:
        bps = 8
        cod = 0.75
    elif mcs == 9:
        bps = 8
        cod = 0.83
    elif mcs == 10:
        bps = 10
        cod = 0.75
    elif mcs == 11:
        bps = 10
        cod = 0.83
    return bps, cod

def snr_to_per(bytes, mcs, snr):
    global per_table
    snr = round(snr, 1)
    file_name = str(mcs) + '-' + str(bytes)
    per = per_table[file_name]
    min_snr = min(per)
    max_snr = max(per)

    if snr < min_snr:
        snr = min_snr
    elif snr > max_snr:
        snr = max_snr
    
    
    return per[snr]

def load_per_table():
    global per_table
    global per_list
    global per_list_dir

    for file_name in per_list:
        file_dir = per_list_dir + file_name + ".txt"
        tempdiction = ReadEngine.Read_To_Diction(file_dir)
        per_table[file_name] = tempdiction

def convert_to_step(time): #마이크로세컨드 단위 시간을 받아 스텝으로 변환
    in_step = math.ceil(time / timestep_mantissa)
    return in_step

load_per_table()


